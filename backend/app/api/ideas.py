from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import IdeaCard, IdeaComment, User

bp = Blueprint('ideas', __name__)

@bp.route('', methods=['GET'])
@jwt_required()
def list_ideas():
    tag = request.args.get('tag')
    query = IdeaCard.query
    if tag:
        query = query.filter(IdeaCard.tags.contains(tag))
    ideas = query.order_by(IdeaCard.is_pinned.desc(), IdeaCard.created_at.desc()).all()
    all_tags = set()
    for idea in IdeaCard.query.all():
        if idea.tags:
            all_tags.update(t.strip() for t in idea.tags.split(',') if t.strip())
    return jsonify({'ideas': [i.to_dict() for i in ideas], 'tags': sorted(all_tags)})

@bp.route('', methods=['POST'])
@jwt_required()
def create_idea():
    data = request.json
    idea = IdeaCard(
        title=data['title'], content=data['content'],
        color=data.get('color', 'blue'), tags=data.get('tags', ''),
        author_id=int(get_jwt_identity())
    )
    db.session.add(idea)
    db.session.commit()
    return jsonify(idea.to_dict()), 201

@bp.route('/<int:idea_id>', methods=['GET'])
@jwt_required()
def get_idea(idea_id):
    idea = IdeaCard.query.get_or_404(idea_id)
    comments = [c.to_dict() for c in idea.comments]
    data = idea.to_dict()
    data['comments'] = comments
    return jsonify(data)

@bp.route('/<int:idea_id>', methods=['PUT'])
@jwt_required()
def update_idea(idea_id):
    idea = IdeaCard.query.get_or_404(idea_id)
    user = User.query.get(int(get_jwt_identity()))
    if idea.author_id != user.id and not user.is_admin:
        return jsonify({'error': '无权编辑'}), 403
    
    data = request.json
    idea.title = data.get('title', idea.title)
    idea.content = data.get('content', idea.content)
    idea.color = data.get('color', idea.color)
    idea.tags = data.get('tags', idea.tags)
    db.session.commit()
    return jsonify(idea.to_dict())

@bp.route('/<int:idea_id>', methods=['DELETE'])
@jwt_required()
def delete_idea(idea_id):
    idea = IdeaCard.query.get_or_404(idea_id)
    user = User.query.get(int(get_jwt_identity()))
    if idea.author_id != user.id and not user.is_admin:
        return jsonify({'error': '无权删除'}), 403
    db.session.delete(idea)
    db.session.commit()
    return '', 204

@bp.route('/<int:idea_id>/pin', methods=['POST'])
@jwt_required()
def pin_idea(idea_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user.is_admin:
        return jsonify({'error': '需要管理员权限'}), 403
    idea = IdeaCard.query.get_or_404(idea_id)
    idea.is_pinned = not idea.is_pinned
    db.session.commit()
    return jsonify(idea.to_dict())

@bp.route('/<int:idea_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(idea_id):
    IdeaCard.query.get_or_404(idea_id)
    data = request.json
    comment = IdeaComment(content=data['content'], idea_id=idea_id, author_id=int(get_jwt_identity()))
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@bp.route('/quick', methods=['POST'])
@jwt_required()
def quick_idea():
    data = request.json
    idea = IdeaCard(
        title=data.get('title', '快速想法'), content=data.get('content', ''),
        color=data.get('color', 'yellow'), author_id=int(get_jwt_identity())
    )
    db.session.add(idea)
    db.session.commit()
    return jsonify(idea.to_dict()), 201
