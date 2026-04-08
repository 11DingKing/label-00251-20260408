from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import WikiPage, WikiRevision, User
import markdown
import bleach
import re

bp = Blueprint('wiki', __name__)

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

def render_markdown(content):
    html = markdown.markdown(content, extensions=['fenced_code', 'tables', 'toc', 'nl2br'])
    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 
                   'code', 'pre', 'blockquote', 'a', 'em', 'strong', 'table', 
                   'thead', 'tbody', 'tr', 'th', 'td', 'br', 'hr', 'img']
    return bleach.clean(html, tags=allowed_tags, attributes={'a': ['href'], 'img': ['src', 'alt']})

@bp.route('', methods=['GET'])
@jwt_required()
def list_pages():
    pages = WikiPage.query.order_by(WikiPage.updated_at.desc()).all()
    categories = list(set(p.category for p in pages))
    return jsonify({'pages': [p.to_dict() for p in pages], 'categories': categories})

@bp.route('', methods=['POST'])
@jwt_required()
def create_page():
    data = request.json
    slug = slugify(data['title'])
    base_slug = slug
    counter = 1
    while WikiPage.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    page = WikiPage(
        title=data['title'], slug=slug, content=data.get('content', ''),
        category=data.get('category', '未分类'), author_id=int(get_jwt_identity())
    )
    db.session.add(page)
    db.session.commit()
    return jsonify(page.to_dict()), 201

@bp.route('/<slug>', methods=['GET'])
@jwt_required()
def get_page(slug):
    page = WikiPage.query.filter_by(slug=slug).first_or_404()
    data = page.to_dict()
    data['html'] = render_markdown(page.content)
    return jsonify(data)

@bp.route('/<slug>', methods=['PUT'])
@jwt_required()
def update_page(slug):
    page = WikiPage.query.filter_by(slug=slug).first_or_404()
    data = request.json
    
    revision = WikiRevision(content=page.content, page_id=page.id, editor_id=int(get_jwt_identity()))
    db.session.add(revision)
    
    page.title = data.get('title', page.title)
    page.content = data.get('content', page.content)
    page.category = data.get('category', page.category)
    db.session.commit()
    return jsonify(page.to_dict())

@bp.route('/<slug>', methods=['DELETE'])
@jwt_required()
def delete_page(slug):
    page = WikiPage.query.filter_by(slug=slug).first_or_404()
    user = User.query.get(int(get_jwt_identity()))
    if page.author_id != user.id and not user.is_admin:
        return jsonify({'error': '无权删除'}), 403
    db.session.delete(page)
    db.session.commit()
    return '', 204

@bp.route('/preview', methods=['POST'])
@jwt_required()
def preview():
    return jsonify({'html': render_markdown(request.json.get('content', ''))})

@bp.route('/search', methods=['GET'])
@jwt_required()
def search():
    q = request.args.get('q', '')
    pages = WikiPage.query.filter(
        (WikiPage.title.contains(q)) | (WikiPage.content.contains(q))
    ).all() if q else []
    return jsonify([p.to_dict() for p in pages])
