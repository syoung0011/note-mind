# 第 5 课：PostgreSQL 与数据持久化

> 状态：已完成
>
> 验收日期：2026-10-04

本文件是本课唯一的动态教程。每个阶段只记录核心讲解、实际结果和易错点，不保存逐轮问答流水；全部验收后补全总结并定档。

## 1. 本课目标与边界

完成本课后，学习者应当能够：

- 说明应用进程、数据库服务、数据库和数据表之间的关系。
- 使用 Docker 启动 PostgreSQL，并通过命名卷让数据脱离容器生命周期保存。
- 理解连接字符串中的主机、端口、数据库、用户和密码。
- 让 FastAPI 通过 SQLAlchemy 连接 PostgreSQL。
- 使用 Alembic 创建并执行第一份数据库迁移。
- 验证数据库结构和演示数据在服务重启后仍然存在。

本课只建立数据库运行环境、连接层和迁移基础，不实现注册接口、密码哈希、登录、笔记 CRUD 或前端数据库页面。`users`、`notes` 和 `note_chunks` 的具体业务字段留到对应功能课程设计，避免过早扩大数据模型。

## 2. AI 与学习者分工

AI 负责：

- 检查上一课定档状态、本机数据库工具和端口占用情况。
- 给出最小完整样例，解释容器、卷、连接、会话与迁移的职责。
- 检查并整改配置和代码，协助定位容器、端口、认证和迁移错误。
- 维护本课教程，在验收后整理参考答案、完整教程和课程总结。

学习者优先体验：

- 启动 Docker Desktop，并亲手创建和检查 PostgreSQL 容器。
- 安装本课 Python 依赖，配置本地连接信息。
- 根据样例完成数据库连接与迁移骨架。
- 亲手执行迁移、重启与持久化验收。
- 检查 Git 差异并创建本课提交。

单独说“继续”只推进一个检查点；需要 AI 代做当前步骤时，可以明确说“给答案”或“帮我实现”。学习者说“确认”时，表示当前操作或代码已经完成且符合给出的验收标准，可以直接记录并推进，不要求机械复制完整输出。

## 3. 核心链路

```text
FastAPI 业务代码
      ↓ SQLAlchemy Session
psycopg 数据库驱动
      ↓ TCP 127.0.0.1:5432
PostgreSQL 容器
      ↓ 写入
Docker 命名卷 notemind_postgres_data
```

- **PostgreSQL**：独立运行的关系型数据库服务，不是 FastAPI 内部的一段代码。
- **数据库驱动**：Python 与 PostgreSQL 通信的底层适配器，本课选择 psycopg。
- **SQLAlchemy**：在 Python 中管理连接、会话和模型的工具。
- **Alembic**：按版本记录并执行数据库结构变化，避免靠手工改表维持环境。
- **命名卷**：由 Docker 管理的数据目录；删除并重建容器时，只要卷仍保留，数据库文件就仍可复用。

## 4. 本课预计修改

```text
backend/requirements.txt              增加数据库、驱动、迁移和配置依赖
backend/app/config.py                 读取数据库连接配置
backend/app/database.py               创建 SQLAlchemy 引擎和会话工厂
backend/alembic.ini                   Alembic 配置入口
backend/alembic/                      数据库迁移环境与版本文件
backend/.env.example                  记录不含真实秘密的配置样例
lesson/05-PostgreSQL与数据持久化.md   动态课程教程
lesson/README.md                      课程状态
```

实际文件会随着检查点验证调整，不为演示创建无业务价值的长期数据表。

## 5. 检查点进度

- [x] A：确认课程衔接、数据库工具和实施边界
- [x] B：启动 PostgreSQL 容器并理解端口、用户、数据库和命名卷
- [x] C：安装依赖并配置数据库连接
- [x] D：建立 SQLAlchemy 连接层并完成连接检查
- [x] E：初始化 Alembic 并执行第一份迁移
- [x] F：完成重启持久化验收和一个小修改
- [x] G：补全总结、检查差异、提交并定档

## 6. 检查点 A：环境与方案

AI 在项目根目录进行了只读检查：

```powershell
docker --version
psql --version
Get-Service -Name '*postgres*'
Get-NetTCPConnection -LocalPort 5432 -State Listen
docker info --format 'ServerVersion={{.ServerVersion}}'
```

实际结果：

- 已安装 Docker CLI `29.8.0`，但 Docker Desktop 的 Linux 引擎尚未启动。
- 本机没有可用的 `psql` 命令，也没有 PostgreSQL Windows 服务。
- 5432 端口当前没有程序监听。
- 项目虚拟环境使用 Python `3.12.6`。

因此本课选择 PostgreSQL 容器加 Docker 命名卷：避免额外安装本机数据库，同时保留真实的网络连接、认证和磁盘持久化体验。第 16 课再把手工容器命令整理成 Docker Compose 一键启动，不在本课提前完成交付配置。

易错点：安装了 `docker.exe` 不代表 Docker 引擎已经运行；客户端命令必须能连接引擎后，才能创建容器。

## 7. 检查点 B：启动 PostgreSQL

先启动 Docker Desktop，等待界面显示引擎已运行。随后在项目根目录执行：

```powershell
docker info --format 'ServerVersion={{.ServerVersion}}'
```

成功标志：输出非空的服务端版本，不再出现 `failed to connect to the docker API`。

学习者启动 Docker Desktop 后，在项目根目录亲手执行了该命令，实际输出为：

```text
ServerVersion=29.8.0
```

这证明 Docker CLI 已经成功连接 Docker 引擎。接下来创建 PostgreSQL 容器；容器使用固定的 PostgreSQL 17 镜像，并通过命名卷保存数据库文件。

学习者随后创建了 `notemind-postgres` 容器，并通过下面的命令检查运行状态：

```powershell
docker ps --filter 'name=notemind-postgres'
```

实际结果显示容器基于 `postgres:17`，状态为 `Up`，本机 IPv4 和 IPv6 的 5432 端口均已映射到容器的 5432 端口。这证明容器进程和端口映射已经建立，但还需要数据库就绪检查来证明 PostgreSQL 可以接受连接。

AI 随后代为执行以下只读检查，并向学习者说明了命令与用途：

```powershell
docker exec notemind-postgres pg_isready -U notemind -d notemind
docker exec notemind-postgres psql -U notemind -d notemind -c "SELECT current_database(), current_user;"
docker inspect notemind-postgres --format 'Mount={{range .Mounts}}{{.Name}} -> {{.Destination}}{{end}}'
```

实际结果：PostgreSQL 返回 `accepting connections`；SQL 查询确认当前数据库和用户均为 `notemind`；容器检查确认命名卷 `notemind_postgres_data` 挂载到 `/var/lib/postgresql/data`。检查点 B 验收通过。

易错点：容器显示 `Up` 只说明主进程存活；`pg_isready` 才检查数据库是否接受连接，而成功执行 SQL 才进一步证明用户、数据库和权限组合可用。

## 8. 检查点 C：依赖与连接配置

本检查点只准备 Python 依赖和本地配置，不创建业务数据表：

- `SQLAlchemy` 管理 Python 侧的连接、会话和后续数据模型。
- `psycopg` 是 SQLAlchemy 与 PostgreSQL 通信使用的驱动。
- `Alembic` 记录和执行后续数据库结构变更。
- `pydantic-settings` 从环境变量或 `.env` 文件读取配置。

连接字符串使用以下结构：

```text
postgresql+psycopg://用户名:密码@主机:端口/数据库名
```

本地开发对应为：

```text
postgresql+psycopg://notemind:notemind_dev@127.0.0.1:5432/notemind
```

真实 `.env` 已被 Git 忽略；`backend/.env.example` 只保存可复制的开发配置格式，不能存放生产密码。

学习者完成并确认了本检查点：

- `backend/requirements.txt` 已声明 SQLAlchemy、psycopg、Alembic 和 pydantic-settings，并成功安装、导入。
- `backend/.env.example` 使用 `change_me` 展示连接字符串格式。
- `backend/.env` 保存本机实际连接字符串。
- AI 只读核对确认 `backend/.env` 存在，并被 `.gitignore` 中的 `.env` 规则正确忽略，不会出现在 Git 状态中。

易错点：包名 `SQLAlchemy` 与 Python 导入名 `sqlalchemy` 大小写不同；连接字符串中的 `postgresql+psycopg` 同时声明了数据库类型和驱动。

## 9. 检查点 D：SQLAlchemy 连接层

连接配置和数据库对象分成两个文件：`config.py` 只负责把外部配置转换成 Python 对象；`database.py` 只负责用这份配置创建 SQLAlchemy 引擎、会话工厂和模型基类。这样业务模块不需要重复读取环境变量或自行拼接连接。

从本检查点开始，AI 将代码骨架直接创建在真实文件中，聊天只说明需要填写的 `TODO(learner)` 和验收命令。学习者确认完成后，AI 先审阅文件，再补全整改并清理教学注释。

AI 创建了 `backend/app/config.py` 和 `backend/app/database.py` 骨架。学习者正确识别了配置编码和 `with SessionLocal()` 管理会话的方向；审阅时发现 `.env` 路径遗漏、`env_file_encoding` 参数名遗漏、`utf-8` 与 `yield` 拼写错误，以及 `yield` 后仍保留 `NotImplementedError`。AI 随后补全实现并清理教学 TODO。

AI 在 `backend/` 目录执行：

```powershell
..\.venv\Scripts\python.exe -m compileall -q app
..\.venv\Scripts\python.exe -c "from sqlalchemy import text; from app.database import engine; connection = engine.connect(); print(connection.execute(text('SELECT current_database(), current_user')).one()); connection.close()"
```

编译检查无错误，真实查询返回 `('notemind', 'notemind')`，证明 `.env` 配置、psycopg 驱动、SQLAlchemy 引擎和 PostgreSQL 服务已经连通。

易错点：`encoding` 不是 `SettingsConfigDict` 在这里需要的参数名；应使用 `env_file_encoding`。生成器必须写作 `yield`，并且成功交出会话后不能继续执行占位用的 `NotImplementedError`。

## 10. 检查点 E：Alembic 迁移基础

数据库迁移把结构变化保存成可排序、可重复执行的版本文件。应用模型描述“希望数据库长什么样”，迁移负责把现有数据库从旧结构安全地变成新结构；只修改 Python 模型不会自动修改 PostgreSQL。

本检查点先初始化 Alembic、接入现有数据库配置并执行一份空的基线迁移，不提前设计 `users`、`notes` 或 `note_chunks` 字段。第一张业务表留到对应功能课程创建。

AI 只读检查确认项目安装了 Alembic `1.20.0`，并且 `backend/` 尚无 Alembic 配置和迁移目录。

学习者在 `backend/` 目录亲手执行：

```powershell
..\.venv\Scripts\python.exe -m alembic init alembic
```

Alembic 成功生成 `alembic.ini`、迁移环境、版本目录和迁移模板。AI 审阅后将默认模板改为复用应用现有的 `engine` 与 `Base`，并清空 `alembic.ini` 中的占位连接串，避免把实际密码重复写入可提交文件。骨架留下两个 `TODO(learner)`，分别用于接入模型元数据和在线迁移引擎。

学习者正确填写了 `connectable = engine`；元数据最初填写为 `Base`，AI 审阅后修正为 `Base.metadata`，因为 Alembic 需要的是模型所注册的表结构集合，而不是声明式基类对象。两条 TODO 与代码发生换行粘连，AI 一并清理并恢复文件格式。

AI 在 `backend/` 目录执行编译检查和只读状态检查：

```powershell
..\.venv\Scripts\python.exe -m compileall -q app alembic
..\.venv\Scripts\python.exe -m alembic current
```

编译无错误；Alembic 成功识别 PostgreSQL，并启用事务型 DDL。当前未显示版本号是预期结果，因为数据库还没有执行任何迁移。

学习者随后在 `backend/` 目录生成空基线迁移：

```powershell
..\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "create baseline"
```

生成文件为 `a17589deca92_create_baseline.py`。AI 审阅确认 `down_revision` 为 `None`，表示它是迁移链起点；`upgrade()` 和 `downgrade()` 都是空操作，没有意外创建或删除业务表。虽然不创建业务表，执行它后 PostgreSQL 会通过 `alembic_version` 表持久记录当前结构版本。

学习者执行 `alembic upgrade head`，并确认 `alembic current` 与 PostgreSQL 中的 `alembic_version` 表均记录版本 `a17589deca92`。这证明迁移执行链路和数据库结构版本记录已经可用，检查点 E 验收通过。

## 11. 检查点 F：命名卷持久化验收

仅停止并重新启动同一个容器，数据也可能仍保存在容器自身的可写层，不能充分证明命名卷有效。本检查点会删除容器但保留 `notemind_postgres_data` 卷，再用完全相同的卷重建容器；如果 `alembic_version` 仍存在，才能证明数据独立于旧容器保存。

本检查点只删除明确命名的 `notemind-postgres` 容器，不执行 `docker volume rm`，也不删除命名卷。

学习者先核对容器确实挂载 `notemind_postgres_data`，再停止并删除 `notemind-postgres` 容器，最后使用同名卷重建 PostgreSQL。数据库恢复就绪后，`alembic_version` 仍返回 `a17589deca92`，证明迁移版本数据保存在命名卷中，而不是依赖已经删除的旧容器。

持久化验收后安排一个小修改：为 SQLAlchemy 引擎启用连接存活检查。数据库重启后，长时间运行的应用连接池里可能还保留已经失效的连接；取出连接前探测可以让 SQLAlchemy 丢弃失效连接并重新连接。

学习者正确加入 `pool_pre_ping=True`。AI 审阅后清理教学 TODO，并在 `backend/` 目录完成最终技术检查：

```powershell
..\.venv\Scripts\python.exe -m compileall -q app alembic
..\.venv\Scripts\python.exe -m pip check
..\.venv\Scripts\python.exe -c "from sqlalchemy import text; from app.database import engine; connection = engine.connect(); print(connection.execute(text('SELECT current_database(), current_user')).one()); connection.close()"
..\.venv\Scripts\python.exe -m alembic current
```

结果：代码编译通过，依赖没有冲突，SQL 查询返回 `('notemind', 'notemind')`，Alembic 当前版本为 `a17589deca92 (head)`。检查点 F 验收通过。

## 12. 复习问题、参考答案与小练习

1. **为什么 PostgreSQL 不是 FastAPI 内部的一部分？** PostgreSQL 是独立运行的数据库服务；FastAPI 通过驱动和网络连接访问它，两者可以分别启动、停止和部署。
2. **容器与命名卷分别保存什么？** 容器提供 PostgreSQL 进程及其运行环境；命名卷保存数据库文件。删除容器但保留并重新挂载命名卷，数据仍可恢复。
3. **SQLAlchemy、psycopg 和 Alembic 各负责什么？** SQLAlchemy 管理引擎、会话和模型；psycopg 负责底层 PostgreSQL 通信；Alembic 版本化管理数据库结构变化。
4. **为什么 `target_metadata` 是 `Base.metadata` 而不是 `Base`？** Alembic 需要模型注册形成的表结构集合来比较数据库，而 `Base` 只是模型继承的声明式基类。
5. **修改模型后为什么还需要迁移？** Python 模型只描述目标结构，不会自动修改已有数据库；迁移文件保存并执行从旧结构到新结构的变化。
6. **`pool_pre_ping=True` 解决什么问题？** 从连接池取出连接前检查它是否仍可用，减少数据库重启后复用失效连接导致的首次请求错误。

小练习已经完成：学习者为 SQLAlchemy 引擎启用连接存活检查，并通过真实连接与迁移状态检查验证修改。

易错点：`docker ps`、`pg_isready` 和执行 SQL 验证的是不同层次；`.env.example` 可以提交配置格式，真实 `.env` 不能提交；Alembic 生成迁移并不等于执行迁移；删除容器与删除命名卷是两个不同操作。

## 13. 完整教程

本课先确认本机没有 PostgreSQL 服务，但已有 Docker CLI。学习者启动 Docker Desktop 后，用 `postgres:17` 创建 `notemind-postgres` 容器，把本机 5432 端口映射到容器，并将数据库目录挂载到 `notemind_postgres_data` 命名卷。通过 `pg_isready` 与 SQL 查询分别验证服务就绪以及用户、数据库和权限组合正确。

后端随后加入 SQLAlchemy、psycopg、Alembic 和 pydantic-settings。真实连接字符串保存在被 Git 忽略的 `backend/.env`，可提交的 `backend/.env.example` 只展示配置格式。`config.py` 负责把外部配置读入 Python；`database.py` 创建引擎、会话工厂、模型基类和自动关闭会话的依赖生成器。

Alembic 初始化后，`env.py` 复用应用的 `engine`，并把 `Base.metadata` 交给自动生成流程。学习者生成并执行空基线迁移 `a17589deca92`；它没有提前创建业务表，只通过 `alembic_version` 建立结构版本起点。以后新增用户、笔记和切块模型时，将在新的迁移文件中表达真实结构变化。

最后，学习者删除旧容器并使用同一个命名卷重建 PostgreSQL。迁移版本仍然存在，证明数据独立于旧容器持久保存。为应对数据库重启造成的失效池连接，SQLAlchemy 引擎加入 `pool_pre_ping=True`，并再次通过编译、依赖、真实查询与迁移状态检查。

## 14. 课程总结

- 使用 PostgreSQL 17 容器建立了真实数据库服务，并理解端口映射、初始化账号和数据库。
- 使用 Docker 命名卷保存数据库文件，通过删除和重建容器验证数据持久化。
- 使用 `.env` 与 pydantic-settings 管理数据库连接信息，确认真实配置不会进入 Git。
- 使用 SQLAlchemy 和 psycopg 建立引擎、会话工厂、模型基类与会话生命周期。
- 初始化 Alembic，接入应用配置和模型元数据，生成并执行第一份基线迁移。
- 理解 Python 模型、迁移版本和 PostgreSQL 实际结构之间的关系。
- 启用连接池存活检查，并通过完整技术检查确认数据库基础层可用。
- 本课没有提前创建业务表；第 06 课将围绕真实用户注册需求设计第一张业务表。

## 15. 验收与定档

技术实现、数据库持久化、迁移和小修改已经通过验收。学习者亲手检查 Git 差异并创建提交 `3e3c338 feat: add PostgreSQL persistence foundation`；提交级检查无空白错误，真实 `.env` 未被跟踪，工作区在提交后保持干净。

学习者已于 2026-10-04 明确确认“本课验收通过”，本课教程和课程总结现已定档。

下一课准确会话名称：`NoteMind 第06课：用户注册`。
