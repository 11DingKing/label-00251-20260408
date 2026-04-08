from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    avatar = db.Column(db.String(256), default='')
    bio = db.Column(db.Text, default='')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id, 'username': self.username, 'email': self.email,
            'avatar': self.avatar, 'bio': self.bio, 'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }

class WikiPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, default='')
    category = db.Column(db.String(100), default='未分类')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='wiki_pages')
    
    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'slug': self.slug,
            'content': self.content, 'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': self.author.to_dict() if self.author else None
        }

class WikiRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    page_id = db.Column(db.Integer, db.ForeignKey('wiki_page.id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page = db.relationship('WikiPage', backref='revisions')
    editor = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'page_id': self.page_id,
            'editor': self.editor.to_dict() if self.editor else None
        }

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'description': self.description,
            'is_private': self.is_private, 'created_at': self.created_at.isoformat(),
            'creator': self.creator.to_dict() if self.creator else None
        }

class ChatRoomMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User')
    room = db.relationship('ChatRoom', backref='members')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author = db.relationship('User', foreign_keys=[author_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    room = db.relationship('ChatRoom', backref='messages')
    
    def to_dict(self):
        return {
            'id': self.id, 'content': self.content,
            'created_at': self.created_at.isoformat(),
            'author': self.author.to_dict() if self.author else None,
            'room_id': self.room_id, 'recipient_id': self.recipient_id
        }

class IdeaCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(20), default='blue')
    tags = db.Column(db.String(500), default='')
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='ideas')
    
    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'content': self.content,
            'color': self.color, 'tags': self.tags, 'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': self.author.to_dict() if self.author else None
        }

class IdeaComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea_card.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea = db.relationship('IdeaCard', backref='comments')
    author = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id, 'content': self.content,
            'created_at': self.created_at.isoformat(),
            'author': self.author.to_dict() if self.author else None
        }

class AISettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(500), default='')
    model = db.Column(db.String(100), default='')
    is_enabled = db.Column(db.Boolean, default=False)
