# NoteMind

NoteMind 是一个面向个人学习场景的 AI 笔记应用。

用户可以注册、登录、创建笔记，并针对自己的笔记内容提问。系统会从笔记中检索相关片段，让大模型基于这些片段回答，并展示引用来源。

这个仓库同时承担两个目标：

1. 完成一个可以运行、演示和部署的 AI 应用。
2. 用 `lesson/` 记录从零开发的关键知识、命令、错误和验收过程。

## 学习进度

课程状态只在 [lesson/README.md](lesson/README.md) 中维护，避免多处记录不一致。

课程 MVP 已完成，当前进入按版本推进的产品迭代阶段。短期目标、优先级和后续方向见 [产品迭代路线](docs/product-roadmap.md)。

## v0.2.0 产品化版本说明

发布状态：功能已合并并通过学习者回归验收，版本标签和 GitHub Release 待创建。

相较于 v0.1.0，本版本补齐了前端注册入口、统一应用布局及认证反馈，将笔记页面整理为列表、编辑和 AI 问答工作台。支持创建、更新和删除的成功提示，区分列表加载失败与真实空状态，并提供重新加载入口；窄屏按顺序显示各区域。

验证结果：学习者确认后端自动化测试、前端生产构建、Compose 配置检查和浏览器回归通过，覆盖注册登录、身份恢复、退出、笔记 CRUD、错误恢复、AI 回答引用与窄屏布局。该结果针对本地验收环境，不代表线上部署已升级。

已知边界：切换笔记会放弃未保存的草稿；AI 检索当前用户全部已保存笔记，不限于选中笔记；已有回答不会随笔记编辑或删除自动刷新；未提供对话历史和流式输出。认证请求尚无显式超时，依赖服务未正常响应时可能长时间等待。启动前需确认所需 Docker 容器已运行；当前 `/health` 不验证数据库连接。

标签固定代码快照，GitHub Release 提供版本说明，两者不会自动完成部署。启动和部署方式继续沿用下面的说明。

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
├── lesson/        按产品版本整理的课程与学习记录
├── .gitignore      Git 忽略规则（第 1 课创建）
└── README.md
```

## 开发原则

- 先完成业务闭环，再根据实际问题优化。
- 每次只学习当前功能需要的知识。
- 每节课采用“分析与分工 → 学习者实现 → AI 检查整改 → 验收总结”的流程。
- 未完成验收、总结和 Git 提交，不进入下一课。
- AI 可以帮助执行，但重要命令和原理必须记录下来。

## 在线演示

- 前端：<https://notemind-web-syoung0011.onrender.com>
- API 文档：<https://notemind-api-syoung0011.onrender.com/docs>
- 健康检查：<https://notemind-api-syoung0011.onrender.com/health>

Render 免费 Web Service 闲置后会休眠，首次访问可能需要等待约一分钟。免费 PostgreSQL 会在创建 30 天后过期，这套环境仅用于学习和短期演示，不保存重要数据。

## 交付前检查

在 `backend` 目录执行后端测试：

```powershell
pip install -r requirements-dev.txt
python -m pytest -q
```

在 `frontend` 目录执行生产构建：

```powershell
npm ci
npm run build
```

在项目根目录检查 Compose 配置：

```powershell
docker compose config --quiet
```

当前基础自动化测试覆盖健康检查、注册登录、跨用户笔记隔离和 RAG 检索阈值。真实模型调用、浏览器流程和部署环境仍需人工验收。

## 部署方式

### Render

根目录 `render.yaml` 声明静态前端、Docker 后端和托管 PostgreSQL。将仓库连接到 Render Blueprint，并只在 Render Environment 中填写真实的 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL`。

粘贴环境变量时应删除首尾空格和换行。模型服务地址中混入换行会让创建笔记时的 Embedding 请求报 `InvalidURL`。

### Linux 服务器

Ubuntu 服务器可以直接使用根目录 `compose.yaml`。复制两个环境模板并填写真实配置：

```bash
cp .env.example .env
cp backend/.env.example backend/.env
chmod 600 .env backend/.env
sudo docker compose up --build -d
sudo docker compose ps
```

中国大陆云服务器无法稳定访问 Docker Hub、PyPI 或 npm 时，可以在根目录 `.env` 中设置对应镜像地址；这些地址会作为构建参数传入，不影响其他环境使用默认官方源。

公网只需开放前端的 80/443 端口。后端宿主机端口只绑定 `127.0.0.1:8000`，PostgreSQL 不发布宿主机端口。没有 HTTPS 时只能用于临时技术验收，不应输入真实或复用密码。
