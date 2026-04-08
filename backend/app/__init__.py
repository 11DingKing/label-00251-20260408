from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    
    from app.api import auth, wiki, chat, ideas, ai_assistant, admin
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(wiki.bp, url_prefix='/api/wiki')
    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    app.register_blueprint(ideas.bp, url_prefix='/api/ideas')
    app.register_blueprint(ai_assistant.bp, url_prefix='/api/ai')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    
    with app.app_context():
        db.create_all()
    
    return app
