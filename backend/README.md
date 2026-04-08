# GameDev Hub - 后端

Flask 后端服务

## 技术栈

- Flask 3.x
- Flask-JWT-Extended (JWT 认证)
- Flask-SocketIO (WebSocket)
- Flask-SQLAlchemy (ORM)
- SQLite (数据库)

## 安装

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 运行

开发模式：
```bash
python run.py
```

生产模式：
```bash
pip install gunicorn eventlet
gunicorn -k eventlet -w 1 -b 0.0.0.0:5001 run:app
```

服务运行在 http://localhost:5001

## 初始化数据库

重置数据库并创建默认数据：

```bash
python reset_db.py
```

这会创建：
- 默认管理员账号 `admin` / `admin123`
- 示例 Wiki 文档
- 默认聊天室

> ⚠️ 请在生产环境中及时修改默认密码

## API 接口

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录
- `GET /api/auth/me` - 获取当前用户

### Wiki
- `GET /api/wiki` - 文档列表
- `POST /api/wiki` - 创建文档
- `GET /api/wiki/<slug>` - 获取文档
- `PUT /api/wiki/<slug>` - 更新文档
- `DELETE /api/wiki/<slug>` - 删除文档

### 想法
- `GET /api/ideas` - 想法列表
- `POST /api/ideas` - 创建想法
- `POST /api/ideas/quick` - 快速记录
- `GET /api/ideas/<id>` - 获取想法
- `PUT /api/ideas/<id>` - 更新想法
- `DELETE /api/ideas/<id>` - 删除想法

### 聊天
- `GET /api/chat/rooms` - 聊天室列表
- `POST /api/chat/rooms` - 创建聊天室
- `GET /api/chat/rooms/<id>` - 聊天室详情
- `GET /api/chat/private/<user_id>` - 私聊消息

### AI
- `GET /api/ai/status` - AI 状态
- `POST /api/ai/chat` - AI 对话

### 管理 (需管理员权限)
- `GET /api/admin/users` - 用户列表
- `PUT /api/admin/users/<id>` - 更新用户
- `DELETE /api/admin/users/<id>` - 删除用户
- `GET /api/admin/ai` - AI 设置
- `PUT /api/admin/ai/<provider>` - 更新 AI 设置

## 数据库

SQLite 数据库文件位于 `instance/gamedev_hub.db`

### 设置管理员

首次启动自动创建 `admin` 账号。手动设置其他用户为管理员：

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='用户名').first()
    user.is_admin = True
    db.session.commit()
```

## 环境变量

可在 `config.py` 中配置：
- `SECRET_KEY` - JWT 密钥
- `SQLALCHEMY_DATABASE_URI` - 数据库连接
