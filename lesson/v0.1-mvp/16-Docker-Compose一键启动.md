# 第 16 课：Docker Compose 一键启动

> 状态：已完成
>
> 验收日期：2026-10-06

本文件是本课唯一的动态教程。教学过程中只记录目标、核心讲解、实际结果、参考答案和易错点；完成实现、运行验收、Git 提交并由双方明确确认后再定档。

## 1. 本课目标与边界

完成本课后，学习者应当能够：

- 解释镜像、容器、构建上下文、端口映射、服务名和数据卷各自解决的问题。
- 为 FastAPI 后端和 Vue 前端分别构建最小生产镜像。
- 使用 Docker Compose 编排前端、后端和 PostgreSQL，并自动执行数据库迁移。
- 区分构建时配置、容器运行时配置和不应写入镜像的真实密钥。
- 使用一组命令启动、检查、停止完整项目，并确认数据库数据可持久化。

本课只解决本地或单机环境下的一键构建与启动，不引入 Kubernetes、CI/CD、云数据库、高可用或复杂反向代理配置；正式公网部署与项目复盘留到第 17 课。

## 2. 从第 15 课继承的现状

当前业务闭环已经具备注册、登录、笔记 CRUD、笔记切块、向量检索、RAG 回答、结构化引用、资料不足拒答和基础评测。

当前启动方式仍然依赖开发机环境：

- 后端依赖本机 Python 虚拟环境，通过 `fastapi dev app/main.py` 启动。
- 前端依赖本机 Node.js 和 `npm run dev` 启动。
- PostgreSQL 地址来自 `backend/.env`，当前示例使用宿主机地址 `127.0.0.1`。
- 前端请求地址与后端 CORS 允许来源仍然是开发端口。
- 仓库尚无 Dockerfile、Compose 文件或 `.dockerignore`。

AI 只读检查确认 Docker Compose CLI 可用；Docker 引擎当前不可连接，运行验收前需要先启动 Docker Desktop 或其他兼容引擎。

## 3. 分工

AI 负责：

- 维护课程文件，设计最小三服务架构和配置边界。
- 在真实文件中提供可运行骨架或少量 `TODO(learner)`。
- 检查 Dockerfile、Compose、环境变量和启动顺序，直接修复遗漏并解释原因。
- 提供构建、迁移、启动、日志、停止和数据持久化的验收步骤。

学习者负责：

- 理解镜像与容器、宿主机地址与 Compose 服务名的区别。
- 完成少量关键容器配置。
- 亲手执行核心 Compose 命令，查看服务状态与日志。
- 完成页面/API 验收、重启后的数据持久化检查和一个小修改。
- 核对 Git 差异并创建本课提交。

## 4. 检查点

- [x] A：理解容器化目标并确定三服务架构
- [x] B：构建 FastAPI 后端镜像并处理数据库迁移
- [x] C：构建 Vue 前端生产镜像并转发 API 请求
- [x] D：使用 Docker Compose 编排前端、后端和 PostgreSQL
- [x] E：完成构建、启动、业务闭环与数据持久化验收
- [x] F：完成小修改、复习、Git 提交和课程定档

## 5. 检查点 A：先画清楚一键启动的边界

本课计划的最小运行结构是：

```text
浏览器
  └─ http://127.0.0.1:8080
       └─ frontend（静态页面，并把 /api 请求转发给 backend）
            └─ backend:8000（FastAPI）
                 └─ db:5432（PostgreSQL）
```

Compose 中的每个服务拥有自己的网络环境。因此：

- 浏览器访问宿主机发布出来的端口，例如 `127.0.0.1:8080`。
- 前端容器转发请求时使用 Compose 服务名 `backend`。
- 后端容器连接数据库时使用 Compose 服务名 `db`，不能使用 `127.0.0.1`；容器中的 `127.0.0.1` 只代表该容器自己。
- PostgreSQL 数据目录使用命名卷保存，删除并重建容器后数据仍可保留。
- 真实 API Key 和 JWT 密钥只在运行时注入，不复制进镜像，也不提交到 Git。

本课选择前端统一暴露一个入口并转发 `/api`，浏览器不需要直接访问后端端口。这样既减少浏览器端环境地址配置，也避免生产运行时依赖开发服务器的 CORS 行为。后端端口仍可按验收需要发布到宿主机，以便访问 Swagger 和健康检查。

进入检查点 B 前，请先口头思考：

1. 为什么后端容器连接数据库时不能继续使用 `127.0.0.1`？
2. 镜像和容器分别更像“可重复使用的模板”还是“模板的一次运行实例”？
3. 为什么数据库需要数据卷，而前端构建产物通常不需要数据卷？

这些问题不要求书面作答。下一检查点会先给出参考答案，再创建后端镜像与迁移启动骨架。

### 检查点 A 参考答案

1. 容器拥有自己的网络环境，容器中的 `127.0.0.1` 只指向该容器自己，不是数据库容器；同一个 Compose 网络中的后端应使用数据库服务名 `db`。
2. 镜像是包含应用及运行依赖的只读模板；容器是镜像的一次可启动、停止和删除的运行实例，同一镜像可以创建多个容器。
3. PostgreSQL 数据会在运行期间持续变化，必须放在独立数据卷中才能跨容器重建保留；前端静态文件来自源码构建，可以随镜像重新生成，不属于运行时数据。

易错点：端口映射解决宿主机访问容器的问题；Compose 服务名解决容器之间互相寻址的问题，两者用途不同。

## 6. 检查点 B：后端镜像与迁移启动顺序

后端镜像使用 `python:3.12-slim` 作为基础环境，工作目录固定为 `/app`。构建时先复制并安装 `requirements.txt`，再复制 Alembic 配置、迁移文件和应用代码。这样只修改业务源码时，Docker 通常可以复用依赖安装层，减少重复下载。

`backend/.dockerignore` 排除了真实 `.env`、本地虚拟环境、Python 缓存和离线示例：

- 真实密钥不能进入构建上下文或镜像层。
- 本地 `.venv` 与容器操作系统可能不兼容，而且镜像会自行安装依赖。
- 缓存和本课运行不需要的示例只会增大构建上下文。

容器中的 FastAPI 必须监听 `0.0.0.0`。如果仍监听默认的 `127.0.0.1`，服务只接受容器内部回环访问，即使发布端口，宿主机也无法访问。

应用启动前需要执行 `python -m alembic upgrade head`，保证数据库结构已经迁移到最新版本。两个命令使用 `&&` 连接：迁移成功才启动服务；迁移失败时容器应退出并在日志中暴露问题，不能带着未知数据库结构继续运行。

AI 已创建：

- `backend/Dockerfile`：后端生产镜像骨架，只留下启动命令待完成。
- `backend/.dockerignore`：限制构建上下文并排除真实环境变量。

学习者需要完成 `backend/Dockerfile` 中唯一的 `TODO(learner)`：把迁移命令和 FastAPI 启动命令写入 `CMD` 的第三个字符串，并使用 `&&` 连接。保留 JSON 数组外层以及 `sh`、`-c` 两个元素。

完成后回复“确认”。AI 会读取实际文件，检查命令顺序、监听地址和 JSON 格式，删除教学注释；随后再安排后端镜像的实际构建验证。当前 Docker 引擎不可连接时，先完成代码检查，不把无法构建误判为 Dockerfile 错误。

### 学习者实现评阅

学习者正确使用 `sh -c` 将迁移和服务启动放进同一个容器启动命令，并以 `&&` 连接。迁移命令位于前面，因此迁移失败时不会继续启动应用；FastAPI 使用 `0.0.0.0:8000`，能够接收从容器外部到达的连接。JSON 数组格式正确。AI 未修改核心实现，只删除了已经完成的教学注释。

下一步需要实际构建后端镜像，验证基础镜像、依赖安装和文件复制均可完成。构建动作需要可连接的 Docker 引擎。

学习者确认已在 `backend` 目录亲手执行 `docker build -t notemind-backend .`，构建成功，并可通过镜像列表确认 `notemind-backend`。这证明基础镜像拉取、Python 依赖安装、Alembic 与应用文件复制均能完成。此时没有单独运行容器，因为启动命令依赖尚未由 Compose 提供的数据库服务。

## 7. 检查点 C：Vue 多阶段构建与 Nginx 反向代理

前端镜像使用两个阶段：

1. `node:24-alpine` 构建阶段通过 `npm ci` 按锁文件安装依赖，并执行 `npm run build` 生成 `dist/`。
2. `nginx:1.27-alpine` 运行阶段只复制 Nginx 配置和最终静态文件，不携带 Node.js、源码或构建依赖。

这种多阶段构建把“生成静态文件的工具”和“线上提供静态文件的程序”分开，使最终镜像更小、运行内容更少。`npm ci` 要求锁文件与 `package.json` 一致，适合可重复的镜像构建。

浏览器现在使用相对地址 `/api/...`，不再把 `127.0.0.1:8000` 写进前端源码。Nginx 负责：

- 返回 Vue 构建后的静态文件。
- 把 `/api/` 请求转发到 Compose 网络中的后端服务。
- 使用 `try_files ... /index.html` 支持 Vue Router 的 history 路由刷新。

AI 已创建 `frontend/Dockerfile`、`frontend/.dockerignore` 和 `frontend/nginx.conf`，并将认证与笔记请求改为同源相对地址。

学习者需要完成 `frontend/nginx.conf` 中唯一的 `TODO(learner)`：在 `proxy_pass` 中填写 Compose 服务名 `backend` 和容器端口 `8000`。保留 `http://` 和结尾分号，不要写宿主机的 `127.0.0.1`。

完成后回复“确认”。AI 会读取实际配置，检查服务名、端口和 URI 转发语义，删除教学注释，再安排前端镜像构建验证。

### 学习者实现评阅

学习者正确填写 `proxy_pass http://backend:8000;`。代理目标使用 Compose 服务名和容器内部端口，没有误用宿主机回环地址。目标 URL 末尾没有 `/`，因此 Nginx 会保留原始 `/api/...` 请求路径，能够匹配 FastAPI 现有路由；若写成 `http://backend:8000/`，匹配到的 `/api/` 前缀会被替换，反而导致路径不一致。AI 未修改核心配置，只删除了教学注释。

下一步需要实际构建前端镜像，验证锁文件依赖安装、Vue 生产构建、跨阶段复制和 Nginx 配置加载均可完成。

学习者确认已在 `frontend` 目录亲手执行 `docker build -t notemind-frontend .`，构建成功，并可通过镜像列表确认 `notemind-frontend`。这证明锁文件依赖安装、Vue 生产构建、跨阶段复制和 Nginx 运行镜像均可完成。

## 8. 检查点 D：Compose 编排三项服务

根目录的 `compose.yaml` 定义三个服务：

- `db` 使用 PostgreSQL 17，并把数据库目录挂载到命名卷 `postgres_data`。
- `backend` 从 `backend/` 构建，读取已有 `backend/.env` 中的 JWT 与模型配置，同时覆盖 `DATABASE_URL` 以连接容器数据库。
- `frontend` 从 `frontend/` 构建，将宿主机 `8080` 映射到 Nginx 的 `80` 端口。

数据库健康检查使用容器自带的 `pg_isready`。后端只有在数据库健康后才启动，随后先执行 Alembic 迁移；前端则等待后端 `/health` 检查通过。这里的 `depends_on` 负责启动阶段的依赖条件，不代表服务今后永远不会中断，也不能替代应用自身的错误处理。

根目录 `.env` 由 Compose 自动读取，只保存本地 PostgreSQL 的库名、用户名和密码。仓库只提交 `.env.example`，真实 `.env` 已被根目录 `.gitignore` 排除。后端原有 `backend/.env` 继续保存 JWT 与模型服务密钥，也不会进入 Git 或镜像。

AI 已创建：

- `compose.yaml`：三服务编排、健康检查、端口映射和数据卷。
- 根目录 `.env.example`：Compose 所需的本地数据库变量模板。

学习者需要完成 `compose.yaml` 中唯一的 `TODO(learner)`：把 `DATABASE_URL` 里的 `@host:5432` 改成数据库的 Compose 服务名。不要改成 `localhost`、`127.0.0.1`、镜像名或容器随机名称。

完成后回复“确认”。AI 会读取并评阅配置、删除教学注释，然后先使用 `docker compose config` 检查变量替换后的最终配置，再进入完整启动验收。

### 学习者实现评阅

学习者最初填写了 `postgres:17-alpine`。这是 `db` 服务使用的镜像名，其中 `postgres` 是镜像仓库名，`17-alpine` 是镜像标签；它不是 Compose 网络中的服务主机名。AI 已将连接地址整改为 `@db:5432` 并删除教学注释。Compose 会在默认网络中为服务名 `db` 提供 DNS 解析，因此后端可以稳定连接数据库容器，而不依赖随机生成的容器名称或 IP。

AI 检查时确认根目录真实 `.env` 尚不存在。下一步需要根据 `.env.example` 创建它，Compose 才能完成变量插值。真实文件继续由 `.gitignore` 排除，不能提交。

学习者已根据模板创建根目录 `.env` 并设置本地数据库变量。AI 只检查变量名，确认 `POSTGRES_DB`、`POSTGRES_USER` 和 `POSTGRES_PASSWORD` 均存在；`git check-ignore` 确认该真实文件由根目录 `.gitignore` 排除，没有读取、展示或提交变量值。

学习者确认在项目根目录亲手执行 `docker compose config --quiet`，配置解析与变量校验无错误；`docker compose config --services` 依次显示 `db`、`backend`、`frontend`，`docker compose config --volumes` 显示 `postgres_data`。这证明服务、变量引用和数据卷声明能够被 Compose 正确解析。检查点 D 完成。

## 9. 检查点 E：完整启动与持久化验收

首次启动使用 `docker compose up --build -d`：

- `--build` 在启动前按照当前源码重新构建本项目的后端与前端镜像。
- `-d` 让容器在后台运行，终端返回后可继续执行状态和日志检查。
- Compose 自动创建项目网络和命名卷，再根据健康条件依次启动数据库、后端和前端。
- 后端容器每次启动都会执行 `alembic upgrade head`；该命令只应用尚未执行的迁移，已在最新版本时不会重复建表。

启动后不能只凭“命令没有报错”判断成功，需要使用 `docker compose ps` 确认三个服务均在运行，且带健康检查的 `db`、`backend` 最终为 healthy。若服务退出或长期处于 unhealthy，应使用 `docker compose logs <服务名>` 检查最小范围日志，不能反复盲目重启。

学习者确认已在项目根目录亲手执行 `docker compose up --build -d` 和 `docker compose ps`。三个服务均正常运行，`db` 与 `backend` 健康检查通过，前端与后端端口映射符合预期。这证明 Compose 能创建网络和数据卷、启动 PostgreSQL、执行 Alembic 迁移并依次启动应用服务。

下一步从用户入口进行烟雾测试。由于当前前端只提供登录和笔记 CRUD，没有注册页面，而新建的 Compose 数据卷是空数据库，因此先在后端 Swagger 注册测试账号，再通过前端登录和创建笔记。这个过程同时验证后端接口、数据库写入、Nginx `/api` 代理和浏览器端业务流程。

学习者确认完成入口与基础业务烟雾测试：后端 `/health` 返回正常状态；通过 Swagger 注册新账号得到 HTTP 201；通过 `http://127.0.0.1:8080` 登录成功，并创建“Compose 验收笔记”。笔记出现在列表中，浏览器经 Nginx `/api` 代理访问后端时没有网络或 CORS 错误。

接下来验证命名卷持久化。`docker compose down` 会停止并删除本项目容器和默认网络，但默认保留命名卷；再次 `up -d` 会创建新容器并重新挂载同一个 `postgres_data`。只有重新登录后仍能看到原账号和笔记，才能证明数据没有只存在于已删除容器的可写层。

易错点：不要在本次验证中使用 `docker compose down -v`。`-v` 会额外删除 Compose 声明的命名卷，属于清空当前容器数据库数据的操作。

学习者确认亲手执行 `docker compose down` 后重新执行 `docker compose up -d`，新容器健康启动；使用原账号重新登录后，“Compose 验收笔记”仍然存在。这证明数据位于 `postgres_data` 命名卷，而不是只保存在旧数据库容器的可写层。

下一步通过容器中的真实 `/api/chat` 完成正反例验证。相关问题应调用 Embedding、检索和聊天模型并返回引用；无关问题应被最低相关度门槛拒绝并返回空引用。该验证也确认 `backend/.env` 中的模型配置和密钥是在运行时注入，而不是依赖宿主机启动的 Python 进程。

学习者确认通过容器中的真实 `/api/chat` 完成正反例验收：相关问题正确回答入口端口和数据卷信息，并返回标题、原文均匹配“Compose 验收笔记”的非空引用；无关实时天气问题返回统一资料不足提示和空引用，后端没有异常退出。这证明模型配置运行时注入、Embedding、检索、阈值、聊天模型、引用与拒答链路均可在 Compose 环境运行。检查点 E 完成。

## 10. 检查点 F：文档、小修改与定档

AI 已根据本课实际验证结果补充根目录 `README.md`，记录环境文件准备、完整启动、入口地址、状态检查、日志查看、普通停止以及删除数据卷的区别。

小修改目标：把 `compose.yaml` 中前端宿主机端口从固定的 `8080` 改为可配置形式，同时保留 `8080` 作为没有设置变量时的默认值。请只修改 `frontend.ports` 中的宿主机端口部分，目标语义为：读取 `FRONTEND_PORT`，没有设置时使用 `8080`，容器内部端口仍为 `80`。

完成后回复“确认”。AI 会读取并评阅修改，将对应变量加入 `.env.example`，再安排配置重建和入口验证。

### 小修改评阅

学习者正确将前端端口映射改为 `${FRONTEND_PORT:-8080}:80`。`${...:-...}` 表示变量未设置或为空时使用默认值；宿主机端口现在可以按环境覆盖，容器内 Nginx 仍监听固定的 `80`。YAML 字符串保留双引号，格式正确。AI 未修改学习者实现，只在根目录 `.env.example` 中补充 `FRONTEND_PORT=8080`，让可配置项在公开模板中可发现。

下一步需要重新解析 Compose 配置并应用变更。由于当前真实 `.env` 没有 `FRONTEND_PORT`，应走默认值并继续从宿主机 `8080` 访问前端。

学习者确认亲手执行 `docker compose config --quiet`、`docker compose up -d` 和 `docker compose ps`，配置与服务状态正常；未设置 `FRONTEND_PORT` 时默认端口 `8080` 生效，前端仍可打开并登录。小修改通过运行验收。

## 11. 复习问题与参考答案

1. **镜像和容器有什么区别？** 镜像是包含应用与依赖的只读模板；容器是镜像的一次运行实例，可以启动、停止和删除，同一镜像可以创建多个容器。
2. **为什么后端使用 `db` 而不是 `127.0.0.1` 连接 PostgreSQL？** 每个容器有独立网络环境，容器中的回环地址只代表自身；Compose 默认网络会把服务名 `db` 解析到数据库容器。
3. **为什么 Dockerfile 先复制依赖清单，再复制源码？** Docker 可以在依赖清单没有变化时复用依赖安装层，只改业务代码不必重新下载全部依赖。
4. **为什么前端使用多阶段构建？** Node 阶段负责生成静态文件，最终 Nginx 阶段只保留运行所需内容，避免把源码、Node.js 和构建依赖带入运行镜像。
5. **为什么前端请求改成相对地址 `/api`？** 浏览器只访问统一的前端来源，由 Nginx 在容器网络内转发到后端，避免把环境相关的后端地址固化进前端构建产物，也不依赖跨域请求。
6. **`depends_on` 与健康检查分别做什么？** 健康检查定义如何判断服务是否可用；带条件的 `depends_on` 让依赖服务在启动阶段等待该状态，但不能保证运行期间服务永不故障。
7. **`docker compose down` 和 `docker compose down -v` 有什么区别？** 前者删除容器和项目网络但默认保留命名卷；后者还删除命名卷，会清空当前容器数据库数据。
8. **为什么真实 `.env` 不能复制进镜像或提交 Git？** 镜像层和版本历史都可能被其他人读取，密钥一旦进入其中，仅删除当前文件不能可靠消除泄露；真实配置应在运行时注入。

## 12. 当前实际修改文件

- `backend/Dockerfile`：安装后端依赖，复制应用与迁移文件，迁移成功后启动 FastAPI。
- `backend/.dockerignore`：排除真实环境变量、虚拟环境、缓存和非运行示例。
- `frontend/Dockerfile`：使用 Node 构建 Vue，再由 Nginx 提供静态文件。
- `frontend/nginx.conf`：提供 SPA 回退，并把 `/api/` 原路径转发给 `backend:8000`。
- `frontend/.dockerignore`：排除本地依赖、构建结果、日志和编辑器配置。
- `frontend/src/services/auth.js`、`frontend/src/services/notes.js`：使用同源相对 API 地址。
- `compose.yaml`：编排 PostgreSQL、后端和前端，声明健康检查、启动依赖、端口与数据卷。
- `.env.example`：提供 Compose 数据库变量和前端端口模板。
- `README.md`：记录一键启动、入口、日志和停止方法。
- `lesson/README.md` 与本课程文件：维护课程状态、过程与验收结果。

## 13. 本课重要命令

单独验证镜像时，分别在 `backend` 和 `frontend` 目录执行：

```powershell
docker build -t notemind-backend .
docker build -t notemind-frontend .
```

其余命令均在项目根目录执行：

```powershell
Copy-Item .env.example .env
docker compose config --quiet
docker compose config --services
docker compose config --volumes
docker compose up --build -d
docker compose ps
docker compose logs backend --tail 100
docker compose down
docker compose up -d
```

- `docker build`：单独验证 Dockerfile、依赖安装与构建产物。
- `config`：在不启动服务前验证 Compose 解析、变量、服务和数据卷。
- `up --build -d`：构建镜像并在后台启动完整项目。
- `ps` 与 `logs`：检查服务状态并定位具体服务错误。
- `down`：删除容器和网络但保留数据卷；重新 `up` 用于验证数据持久化。

## 14. 完整教程与课程总结

本课把原本依赖开发机 Python、Node.js 和数据库环境的三个启动过程，收敛为根目录的一组 Compose 命令。后端镜像安装 Python 依赖并包含 Alembic 迁移，容器启动时先升级数据库结构，成功后才让 FastAPI 监听所有容器网络接口。数据库健康检查避免后端在 PostgreSQL 尚未可用时过早启动。

前端采用多阶段构建：Node 阶段按锁文件安装依赖并生成 Vue 静态文件，最终 Nginx 镜像只负责提供页面和转发 API。浏览器使用同源 `/api` 地址，Nginx 通过 Compose 服务名访问后端；Vue Router 的 history 路由则由 `try_files` 回退到 `index.html`。

Compose 使用 `db`、`backend`、`frontend` 三个服务，命名卷 `postgres_data` 保存数据库数据。真实 PostgreSQL 变量、JWT 和模型密钥均在运行时从被 Git 忽略的环境文件注入，没有复制进镜像。前端宿主机端口支持通过 `FRONTEND_PORT` 覆盖，默认仍为 `8080`。

学习者亲手完成后端启动命令、Nginx 代理目标、数据库服务寻址和可配置前端端口；其中曾把镜像名误作数据库主机名，整改后明确了镜像标识与 Compose 服务名的区别。学习者还完成镜像构建、Compose 配置检查、完整启动、健康状态、注册登录、笔记创建、容器重建后的数据持久化，以及 RAG 正常回答和拒答验收。当前实现与运行结果已通过最终差异审查，等待 Git 提交与课程定档。

学习者核对最终暂存差异并创建提交 `1545f84 feat: add Docker Compose startup`。AI 复核确认该提交包含预期的 12 个文件，没有包含根目录 `.env`、`backend/.env` 或其他真实密钥文件，提交后工作区干净。双方明确确认本课全部实现与验收结果，第 16 课正式定档。

下一课准确会话名称：`NoteMind 第17课：测试、部署与项目复盘`
