#!/usr/bin/env python
"""重置数据库并初始化默认数据"""
import os

# 删除旧数据库
db_path = 'instance/gamedev_hub.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print('✓ 已删除旧数据库')

# 确保 instance 目录存在
os.makedirs('instance', exist_ok=True)

# 创建新数据库和默认管理员
from app import create_app, db
from app.models import User, WikiPage, ChatRoom

app = create_app()
with app.app_context():
    db.create_all()
    print('✓ 已创建数据库表')
    
    # 检查是否已存在管理员
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@gamedev.hub',
            bio='系统管理员',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 创建示例 Wiki
        wiki = WikiPage(
            title='欢迎使用 GameDev Hub',
            slug='welcome',
            content='''# 欢迎使用 GameDev Hub

这是一个游戏开发者协作平台，提供以下功能：

- **Wiki 文档** - 团队知识库
- **想法卡片** - 灵感记录
- **实时聊天** - 团队沟通
- **AI 助手** - 智能辅助

开始探索吧！''',
            category='入门指南',
            author=admin
        )
        db.session.add(wiki)
        
        # 创建默认聊天室
        room = ChatRoom(
            name='大厅',
            description='公共聊天室，欢迎大家交流',
            creator=admin
        )
        db.session.add(room)
        
        db.session.commit()
        print('✓ 已创建默认数据')
        print('')
        print('默认管理员账号:')
        print('  用户名: admin')
        print('  密码: admin123')
    else:
        print('✓ 管理员已存在，跳过初始化')
