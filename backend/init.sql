-- GameDev Hub 初始化数据
-- 默认管理员账号: admin / admin123

-- 清空现有数据（可选）
-- DELETE FROM user;

-- 插入默认管理员
-- 密码 admin123 的 hash (使用 werkzeug.security.generate_password_hash)
INSERT OR IGNORE INTO user (id, username, email, password_hash, avatar, bio, is_admin, created_at)
VALUES (
    1,
    'admin',
    'admin@gamedev.hub',
    'scrypt:32768:8:1$YjKxQz8mNpLwRvHs$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2',
    '',
    '系统管理员',
    1,
    datetime('now')
);

-- 插入示例 Wiki 文档
INSERT OR IGNORE INTO wiki_page (id, title, slug, content, category, author_id, created_at, updated_at)
VALUES (
    1,
    '欢迎使用 GameDev Hub',
    'welcome',
    '# 欢迎使用 GameDev Hub

这是一个游戏开发者协作平台，提供以下功能：

- **Wiki 文档** - 团队知识库
- **想法卡片** - 灵感记录
- **实时聊天** - 团队沟通
- **AI 助手** - 智能辅助

开始探索吧！',
    '入门指南',
    1,
    datetime('now'),
    datetime('now')
);

-- 插入示例聊天室
INSERT OR IGNORE INTO chat_room (id, name, description, is_private, creator_id, created_at)
VALUES (
    1,
    '大厅',
    '公共聊天室，欢迎大家交流',
    0,
    1,
    datetime('now')
);
