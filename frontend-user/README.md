# GameDev Hub - 用户端

Vue 3 前端应用

## 访问地址

- Docker: http://localhost:8081
- 开发: http://localhost:5173

## 技术栈

- Vue 3 + Composition API
- Vite 5.x
- Pinia 状态管理
- Vue Router 4
- Tailwind CSS
- Socket.IO Client
- Axios

## 安装

```bash
npm install
```

## 开发

```bash
npm run dev
```

## 构建

```bash
npm run build
```

## 目录结构

```
src/
├── views/              # 页面组件
│   ├── admin/         # 管理后台
│   ├── chat/          # 聊天模块
│   ├── ideas/         # 想法模块
│   └── wiki/          # Wiki 模块
├── stores/            # Pinia 状态
│   └── auth.js        # 认证状态
├── api.js             # API 封装
├── router.js          # 路由配置
├── App.vue            # 根组件
├── main.js            # 入口文件
└── style.css          # 全局样式
```

## 功能模块

- 用户认证（登录/注册）
- Wiki 文档管理
- 想法卡片
- 实时聊天（群聊/私聊）
- AI 助手对话
- 管理后台（用户管理、AI 配置）
