from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from flask_socketio import emit, join_room, leave_room
from app import db, socketio
from app.models import ChatRoom, ChatRoomMember, Message, User

bp = Blueprint('chat', __name__)

@bp.route('/rooms', methods=['GET'])
@jwt_required()
def list_rooms():
    user_id = int(get_jwt_identity())
    public = ChatRoom.query.filter_by(is_private=False).all()
    my_rooms = ChatRoom.query.join(ChatRoomMember).filter(ChatRoomMember.user_id == user_id).all()
    return jsonify({'public': [r.to_dict() for r in public], 'my_rooms': [r.to_dict() for r in my_rooms]})

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    data = request.json
    user_id = int(get_jwt_identity())
    room = ChatRoom(name=data['name'], description=data.get('description', ''),
                    is_private=data.get('is_private', False), creator_id=user_id)
    db.session.add(room)
    db.session.flush()
    member = ChatRoomMember(room_id=room.id, user_id=user_id)
    db.session.add(member)
    db.session.commit()
    return jsonify(room.to_dict()), 201

@bp.route('/rooms/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.created_at.desc()).limit(100).all()
    members = [m.user.to_dict() for m in room.members]
    return jsonify({'room': room.to_dict(), 'messages': [m.to_dict() for m in reversed(messages)], 'members': members})

@bp.route('/rooms/<int:room_id>/join', methods=['POST'])
@jwt_required()
def join_room_api(room_id):
    user_id = int(get_jwt_identity())
    if not ChatRoomMember.query.filter_by(room_id=room_id, user_id=user_id).first():
        db.session.add(ChatRoomMember(room_id=room_id, user_id=user_id))
        db.session.commit()
    return '', 204

@bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.filter(User.id != int(get_jwt_identity())).all()
    return jsonify([u.to_dict() for u in users])

@bp.route('/private/<int:user_id>', methods=['GET'])
@jwt_required()
def get_private_messages(user_id):
    me = int(get_jwt_identity())
    messages = Message.query.filter(
        ((Message.author_id == me) & (Message.recipient_id == user_id)) |
        ((Message.author_id == user_id) & (Message.recipient_id == me))
    ).order_by(Message.created_at.desc()).limit(100).all()
    other = User.query.get_or_404(user_id)
    return jsonify({'messages': [m.to_dict() for m in reversed(messages)], 'user': other.to_dict()})

# WebSocket events
@socketio.on('join')
def on_join(data):
    room = data.get('room')
    join_room(room)
    emit('status', {'msg': '用户加入了聊天室'}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data.get('room')
    leave_room(room)

@socketio.on('message')
def on_message(data):
    token = data.get('token')
    if not token:
        return
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
    except:
        return
    
    room_id = data.get('room_id')
    content = data.get('content')
    if room_id and content:
        msg = Message(content=content, author_id=user_id, room_id=room_id)
        db.session.add(msg)
        db.session.commit()
        emit('new_message', msg.to_dict(), room=f'room_{room_id}')

@socketio.on('private_message')
def on_private_message(data):
    token = data.get('token')
    if not token:
        return
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
    except:
        return
    
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    if recipient_id and content:
        msg = Message(content=content, author_id=user_id, recipient_id=recipient_id)
        db.session.add(msg)
        db.session.commit()
        emit('new_private_message', msg.to_dict(), room=f'user_{recipient_id}')
        emit('new_private_message', msg.to_dict(), room=f'user_{user_id}')

@socketio.on('connect')
def on_connect():
    pass

@socketio.on('auth')
def on_auth(data):
    token = data.get('token')
    if token:
        try:
            decoded = decode_token(token)
            user_id = decoded['sub']
            join_room(f'user_{user_id}')
        except:
            pass
