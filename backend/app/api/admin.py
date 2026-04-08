from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app import db
from app.models import User, AISettings, WikiPage, IdeaCard, ChatRoom

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))
        if not user or not user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated

@bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def stats():
    return jsonify({
        'users': User.query.count(),
        'wiki_pages': WikiPage.query.count(),
        'ideas': IdeaCard.query.count(),
        'chat_rooms': ChatRoom.query.count()
    })

@bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    return jsonify([u.to_dict() for u in User.query.all()])

@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@jwt_required()
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != int(get_jwt_identity()):
        user.is_admin = not user.is_admin
        db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != int(get_jwt_identity()):
        db.session.delete(user)
        db.session.commit()
    return '', 204

@bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被使用'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': '邮箱已被使用'}), 400
        user.email = data['email']
    
    if data.get('password'):
        user.set_password(data['password'])
    
    if 'is_admin' in data and user.id != int(get_jwt_identity()):
        user.is_admin = data['is_admin']
    
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/ai-settings', methods=['GET'])
@jwt_required()
@admin_required
def get_ai_settings():
    providers = ['openai', 'anthropic', 'google']
    settings = {s.provider: {'api_key': s.api_key, 'model': s.model, 'is_enabled': s.is_enabled} 
                for s in AISettings.query.all()}
    for p in providers:
        if p not in settings:
            s = AISettings(provider=p)
            db.session.add(s)
            settings[p] = {'api_key': '', 'model': '', 'is_enabled': False}
    db.session.commit()
    return jsonify(settings)

@bp.route('/ai-settings', methods=['POST'])
@jwt_required()
@admin_required
def update_ai_settings():
    data = request.json
    provider = data['provider']
    setting = AISettings.query.filter_by(provider=provider).first()
    if not setting:
        setting = AISettings(provider=provider)
        db.session.add(setting)
    
    setting.api_key = data.get('api_key', '')
    setting.model = data.get('model', '')
    
    if data.get('is_enabled'):
        for s in AISettings.query.all():
            s.is_enabled = (s.provider == provider)
    else:
        setting.is_enabled = False
    
    db.session.commit()
    return jsonify({'success': True})
