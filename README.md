# GameDev Hub

游戏开发者协作平台

## How to Run

```bash
cd gamedev-hub
docker-compose up --build -d
```

## Services

| 服务 | 端口 | 访问地址 |
|------|------|----------|
| 用户端 (frontend-user) | 8081 | http://localhost:8081 |
| 后端 API (backend) | 5001 | http://localhost:5001/api |

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

## 题目内容

我现在在和朋友开发游戏，所以我想建立一个网站供我们书写创意和交流项目要求：网站包含以下功能：0.账户系统1.类wiki功能，支持markdown，供我们写下创意2.交流功能，应当支持在线群聊及在线私聊，并额外实现适当内容（如想法卡片，写下即时想法）3.尝试实现ai助理内容，支持管理员通过设置api允许智能体服务（claude、gemini、gpt等）有任何疑问可以提问我使用python


构建一个游戏开发者协作平台，包含以下功能模块：

1. **用户系统** - 注册、登录、个人资料管理
2. **Wiki 文档** - 团队知识库，支持 Markdown 编辑
3. **想法卡片** - 灵感记录与分享
4. **实时聊天** - 群聊和私聊功能
5. **AI 助手** - 集成 OpenAI/Anthropic/Google AI
6. **管理后台** - 用户管理、AI 配置

---

## 项目结构

```
gamedev-hub/
├── docker-compose.yml
├── .gitignore
├── README.md
├── backend/                # 后端服务
│   ├── Dockerfile
│   ├── app/
│   │   ├── api/           # API 路由
│   │   └── models.py      # 数据模型
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
└── frontend-user/          # 用户端前端
    ├── Dockerfile
    ├── nginx.conf
    ├── src/
    │   ├── views/         # 页面组件
    │   ├── stores/        # Pinia 状态
    │   └── router.js      # 路由配置
    └── package.json
```

## 技术栈

### 前端
- Vue 3 + Vite
- Pinia 状态管理
- Vue Router
- Tailwind CSS
- Socket.IO Client

### 后端
- Flask 3.x
- Flask-JWT-Extended
- Flask-SocketIO
- Flask-SQLAlchemy
- SQLite

## 功能特性

- 🎮 现代化深色主题 UI
- 📝 Markdown 文档编辑与预览
- 💬 WebSocket 实时聊天
- 🤖 多 AI 服务商支持
- 👥 用户权限管理
- 📱 响应式移动端适配

## 本地开发

后端：
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python reset_db.py
python run.py
```

前端：
```bash
cd frontend-user
npm install
npm run dev
```

## API 文档

详见 [backend/README.md](backend/README.md)
