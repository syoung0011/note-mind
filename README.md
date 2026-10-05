# NoteMind

NoteMind 是一个面向个人学习场景的 AI 笔记应用。

用户可以注册、登录、创建笔记，并针对自己的笔记内容提问。系统会从笔记中检索相关片段，让大模型基于这些片段回答，并展示引用来源。

这个仓库同时承担两个目标：

1. 完成一个可以运行、演示和部署的 AI 应用。
2. 用 `lesson/` 记录从零开发的关键知识、命令、错误和验收过程。

## 学习进度

课程状态只在 [lesson/README.md](lesson/README.md) 中维护，避免多处记录不一致。

## 使用 Docker Compose 启动

前置条件：已安装并启动 Docker Desktop，或具备兼容的 Docker Engine 与 Docker Compose。

在项目根目录创建 Compose 使用的数据库环境文件：

```powershell
Copy-Item .env.example .env
```

编辑根目录 `.env`，设置本地 PostgreSQL 数据库名称、用户名和密码。然后根据后端模板创建运行配置：

```powershell
Copy-Item backend\.env.example backend\.env
```

编辑 `backend/.env`，至少设置安全的 `JWT_SECRET_KEY`，并填写实际使用的模型服务地址、API Key、Embedding 模型和聊天模型。真实 `.env` 文件已被 Git 忽略，不应提交。

在项目根目录构建并后台启动完整项目：

```powershell
docker compose up --build -d
docker compose ps
```

启动成功后可以访问：

- 前端：<http://127.0.0.1:8080>
- 后端 Swagger：<http://127.0.0.1:8000/docs>
- 后端健康检查：<http://127.0.0.1:8000/health>

查看某个服务的日志：

```powershell
docker compose logs backend --tail 100
```

停止并删除容器与项目网络，同时保留 PostgreSQL 数据卷：

```powershell
docker compose down
```

`docker compose down -v` 会额外删除数据库命名卷并清空容器数据库数据，只应在明确需要重置数据时使用。

## 目录

```text
note-mind/
├── backend/       FastAPI 后端（对应课程开始时创建）
├── frontend/      Vue 3 前端（对应课程开始时创建）
├── docs/          产品需求、学习规则和待办事项
├── lesson/        每一课的学习记录
├── .gitignore      Git 忽略规则（第 1 课创建）
└── README.md
```

## 开发原则

- 先完成业务闭环，再根据实际问题优化。
- 每次只学习当前功能需要的知识。
- 每节课采用“分析与分工 → 学习者实现 → AI 检查整改 → 验收总结”的流程。
- 未完成验收、总结和 Git 提交，不进入下一课。
- AI 可以帮助执行，但重要命令和原理必须记录下来。
