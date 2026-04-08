from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import AISettings

bp = Blueprint('ai', __name__)

def get_ai_client():
    settings = AISettings.query.filter_by(is_enabled=True).first()
    if not settings or not settings.api_key:
        return None, None, None
    return settings.provider, settings.api_key, settings.model

@bp.route('/status', methods=['GET'])
@jwt_required()
def status():
    settings = AISettings.query.filter_by(is_enabled=True).first()
    return jsonify({'enabled': settings is not None and bool(settings.api_key)})

@bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    provider, api_key, model = get_ai_client()
    if not provider:
        return jsonify({'error': 'AI 服务未配置'}), 400
    
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    
    try:
        if provider == 'openai':
            return chat_openai(api_key, model, message, history)
        elif provider == 'anthropic':
            return chat_anthropic(api_key, model, message, history)
        elif provider == 'google':
            return chat_google(api_key, model, message, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def chat_openai(api_key, model, message, history):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": "你是一个游戏开发助手，帮助团队进行创意讨论、设计建议和技术问题解答。"}]
    messages.extend([{"role": h['role'], "content": h['content']} for h in history])
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model=model or "gpt-3.5-turbo", messages=messages, max_tokens=2000)
    return jsonify({'response': response.choices[0].message.content})

def chat_anthropic(api_key, model, message, history):
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    messages = [{"role": h['role'], "content": h['content']} for h in history]
    messages.append({"role": "user", "content": message})
    response = client.messages.create(
        model=model or "claude-3-sonnet-20240229", max_tokens=2000,
        system="你是一个游戏开发助手，帮助团队进行创意讨论、设计建议和技术问题解答。",
        messages=messages
    )
    return jsonify({'response': response.content[0].text})

def chat_google(api_key, model, message, history):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model_instance = genai.GenerativeModel(model or 'gemini-pro')
    chat_history = [{'role': 'user' if h['role'] == 'user' else 'model', 'parts': [h['content']]} for h in history]
    chat = model_instance.start_chat(history=chat_history)
    response = chat.send_message(message)
    return jsonify({'response': response.text})
