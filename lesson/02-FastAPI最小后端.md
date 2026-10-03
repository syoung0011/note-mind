# 第 2 课：FastAPI 最小后端

> 状态：进行中（等待学习者实现）

本文件是本课唯一的动态教程。每个阶段只记录核心讲解、实际结果和易错点，不保存逐轮问答流水；全部验收后补全总结并定档。

## 1. 本课目标与分工

完成本课后，学习者应当能够：

- 说明浏览器或客户端发出 HTTP 请求后，FastAPI 如何返回 JSON 响应。
- 解释虚拟环境、依赖、应用对象、路由和开发服务器分别负责什么。
- 亲手创建并启动一个最小 FastAPI 后端。
- 根据终端输出、接口响应和自动文档判断后端是否正常运行。

AI 负责制定检查点、解释概念、维护课程文件、检查实际代码并协助整改；学习者负责创建虚拟环境、安装依赖、编写最小应用、启动服务器并完成验收修改。

本课只建立可运行的后端骨架，不提前加入数据库、用户系统、跨域配置或复杂目录分层。

## 2. 核心流程

```text
客户端发送 GET /health
        ↓
开发服务器接收 HTTP 请求
        ↓
FastAPI 根据路径和方法找到处理函数
        ↓
处理函数返回 Python 字典
        ↓
FastAPI 将字典转换成 JSON 响应
```

- **HTTP 请求**：客户端向服务器表达“要访问哪个路径、使用什么方法、携带什么数据”。
- **路由**：HTTP 方法和 URL 路径到处理函数的映射，例如 `GET /health`。
- **应用对象**：保存路由、配置等信息的 FastAPI 实例，是后端应用的入口。
- **开发服务器**：监听本机端口，把收到的请求交给 FastAPI；开发模式支持代码变更后自动重载。
- **虚拟环境**：为当前项目保存独立的 Python 包，避免不同项目的依赖互相影响。

## 3. 本课预计文件

```text
note-mind/
├── .venv/                  本地虚拟环境，不提交 Git
├── backend/
│   ├── requirements.txt   后端直接依赖
│   └── app/
│       ├── __init__.py    将目录明确标记为 Python 包
│       └── main.py        FastAPI 应用入口和最小路由
└── lesson/
    └── 02-FastAPI最小后端.md
```

## 4. 检查点进度

- [x] A：确认 Python 环境、本课边界和请求流程
- [x] B：创建并激活项目虚拟环境
- [x] C：声明并安装 FastAPI 依赖
- [x] D：亲手创建应用对象和健康检查路由
- [x] E：启动开发服务器并检查接口和自动文档
- [ ] F：完成小修改、自查、总结和 Git 提交

## 5. 检查点 A：环境与方案

本检查点的环境探测由 AI 在项目根目录执行，属于安全的只读检查：

```powershell
python --version
py --version
python -m pip --version
```

- `python --version`：确认终端中 `python` 命令实际指向的 Python 版本。
- `py --version`：确认 Windows Python Launcher 可用及其默认版本。
- `python -m pip --version`：使用同一个 Python 解释器调用 pip，并显示 pip 版本及安装路径；这种写法比直接执行 `pip` 更容易确认二者属于同一套环境。

AI 检查结果：`python` 和 `py` 均为 Python 3.12.6；pip 为 26.1.2，检查时来自系统 Python 目录。项目根目录已经通过 `.gitignore` 忽略 `.venv/`。

这些命令只读取版本信息，不会创建文件或修改环境。检查点 B 创建并激活虚拟环境后，学习者会再次亲手执行 `python -m pip --version`；届时安装路径应由系统 Python 目录变为本项目的 `.venv`，用于验证环境切换确实生效。

本课使用 Python 自带的 `venv` 和 pip，减少额外工具带来的学习范围；安装 `fastapi[standard]`，使用 FastAPI 官方开发命令 `fastapi dev` 启动服务。

预计健康检查接口：

```text
GET /health → 200 OK → {"status": "ok"}
```

健康检查只回答“服务是否活着”，之后可以被开发者、测试或部署平台用于快速判断后端是否能响应。

## 6. 检查点 B：创建虚拟环境

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip --version
```

- 第一条命令创建项目专用的 `.venv/`，会写入 Python 解释器和包管理工具。
- 第二条命令只对当前 PowerShell 会话启用该环境。
- 第三条命令用于验证；成功时输出路径应位于当前项目的 `.venv` 中。

如果 PowerShell 因执行策略拒绝激活，先不要修改全局安全设置，把完整报错交给 AI 检查。

学习者实际执行成功，验证输出为：

```text
pip 24.2 from D:\Program Files (x86)\PycharmProjects\note-learn\note-mind\.venv\Lib\site-packages\pip (python 3.12)
```

路径位于项目 `.venv` 内，证明激活后的 `python -m pip` 使用虚拟环境，而不是系统 Python 的 pip。虚拟环境中的 pip 24.2 与系统环境中的 pip 26.1.2 相互独立，版本不同不代表激活失败。

AI 随后使用虚拟环境解释器再次核对 Python 和 pip，并执行：

```powershell
git check-ignore -v .venv
```

结果显示 `.gitignore` 第 2 行的 `.venv/` 规则已命中，因此虚拟环境不会作为未跟踪文件进入 Git。

## 7. 检查点 C：声明并安装依赖

学习者创建了 `backend/requirements.txt`：

```text
fastapi[standard]
```

随后在已激活虚拟环境的项目根目录执行：

```powershell
python -m pip install -r .\backend\requirements.txt
python -m pip show fastapi
```

- `requirements.txt` 声明项目的直接依赖，其他环境可以根据它重复安装。
- `pip install -r` 读取依赖文件并将包安装到当前 Python 环境。
- `python -m pip` 明确使用当前 `python` 对应的 pip，减少命令指向错误环境的可能。
- `fastapi[standard]` 包含 FastAPI 及其常用标准依赖，本课会使用其中的开发服务器命令。

实际结果：FastAPI 0.142.2 已安装，`Location` 位于项目 `.venv\Lib\site-packages`。AI 同时核对了依赖文件内容与虚拟环境中的安装结果，检查点通过。

易错点：依赖文件只是在文本中声明需求，不等于已经安装；安装成功也不等于依赖已经写入文件，两者都需要检查。

## 8. 检查点 D：创建最小应用

学习者将在 `backend/app/` 中亲手创建 `__init__.py` 和 `main.py`，实现 FastAPI 应用对象与 `GET /health` 路由。

代码中的关键关系：

```text
FastAPI 类 --实例化--> app 应用对象
@app.get("/health") --注册--> health_check 函数
收到 GET /health --调用--> health_check --返回--> JSON 响应
```

本检查点完成后由 AI 检查实际文件，再进入服务器启动与请求验收。

学习者实际创建的 `main.py` 为：

```python
from fastapi import FastAPI

app = FastAPI(title="NoteMind API")

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

学习者使用了 `async def`，与任务示例中的普通 `def` 不同，但 FastAPI 同时支持两者，本接口可以正常工作。当前函数没有等待数据库或网络 I/O，本课不展开异步并发细节。

AI 在项目根目录使用虚拟环境解释器执行只读导入检查：

```powershell
.\.venv\Scripts\python.exe -c "from fastapi import FastAPI; from backend.app.main import app; print(FastAPI.__name__); print(app.title)"
```

结果输出 `FastAPI` 和 `NoteMind API`，证明依赖可以导入、模块语法有效且应用对象已经创建。

实际踩坑：在 Cursor 中输入导入语句时没有出现普通代码补全。代码本身和虚拟环境导入均正常，因此优先检查 Python 扩展、当前文件语言模式、所选解释器及语言服务，而不是修改业务代码。检查发现 Cursor 同时启用了 Anysphere Python 与 Pylance 两套语言服务，两者会冲突；学习者已按提示处理 Pylance，并保留 Anysphere Python、Microsoft Python 和 Python Debugger。

继续课程前，AI 再次执行只读检查并打印应用的已注册路由；结果包含 FastAPI 自动生成的 `/openapi.json`、`/docs`、`/redoc`，以及学习者创建的 `GET /health`，说明应用结构仍然有效。

## 9. 检查点 E：启动与验证服务

学习者将在已激活虚拟环境的项目根目录启动开发服务器：

```powershell
fastapi dev .\backend\app\main.py
```

- `fastapi dev` 启动只用于本地开发的服务器，并监听代码变化后自动重载。
- 文件路径告诉命令从哪里导入 FastAPI 应用对象。
- 成功时终端应显示应用启动完成以及 `http://127.0.0.1:8000`。
- 服务器持续占用当前终端属于正常现象；按 `Ctrl+C` 才会停止。

服务运行期间，需要验证：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

`/health` 应返回状态码 200 和 `{"status":"ok"}`；`/docs` 应显示标题为 `NoteMind API` 的 Swagger UI，并列出 `GET /health`。

还需要在第二个 PowerShell 终端执行：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

浏览器验证适合人工查看，命令行验证则便于今后写脚本和自动化检查。实际输出和验收结论将在学习者执行后补充。

学习者表示继续课程后，AI 尝试访问 `/health` 和 `/openapi.json`，当时服务已经停止，因此无法从当前运行状态补验此前结果。服务经 `Ctrl+C` 停止后无法连接是正常现象；检查点 E 暂不标记完成，待小修改后重新启动并一次性验收。

小修改后，学习者重新启动服务器并保持运行。AI 随后进行了独立验收：

```text
GET /       → 200 → {"message":"Welcome to NoteMind API"}
GET /health → 200 → {"status":"ok"}
OpenAPI title: NoteMind API
OpenAPI paths: /, /health
```

实际踩坑：当前 PowerShell 宿主中的 `Invoke-WebRequest` 读取响应时出现空引用异常，但 `Invoke-RestMethod`、`curl.exe` 和 OpenAPI 请求均成功。更换验证工具后证明这是客户端命令问题，不是 FastAPI 服务故障。

## 10. 检查点 F：独立完成一个小修改

学习者需要参照现有 `/health` 路由，自行增加根路径接口，目标行为为：

```text
GET / → 200 OK → {"message": "Welcome to NoteMind API"}
```

本任务用于验证学习者能否独立复用“装饰器注册路由、函数返回字典、FastAPI 转换 JSON”的流程。修改后重新启动服务，同时验证 `/`、`/health` 和 `/docs`，即可一并完成检查点 E 与本检查点的运行部分。

学习者已独立增加 `GET /`，并通过命令行及 OpenAPI 验证。AI 还执行了：

```powershell
.\.venv\Scripts\python.exe -m compileall -q backend
git diff --check
```

结果均通过，说明 Python 文件可以编译，当前 Git 差异没有空白错误。功能部分已完成；本检查点还需完成自查、总结和 Git 提交后才能整体勾选。

## 11. 复习问题与参考答案

请先口头回答，再对照参考答案：

1. 虚拟环境解决了什么问题？
2. `app` 应用对象和开发服务器分别负责什么？
3. `@app.get("/health")` 做了什么？
4. 处理函数返回 Python 字典后，客户端为什么会收到 JSON？
5. 怎样分别从运行、修改和排错三个角度证明本课掌握了？

参考答案：

1. 为当前项目提供独立的 Python 解释器和依赖目录，避免不同项目或系统环境的包版本互相影响。
2. `app` 保存路由和应用配置；开发服务器监听端口、接收 HTTP 请求并把请求交给 FastAPI 应用。
3. 它将 HTTP `GET` 方法和 `/health` 路径映射到下面的处理函数。
4. FastAPI 接收处理函数的返回值，并自动把可序列化的 Python 数据转换为 JSON HTTP 响应。
5. 运行：能启动并访问接口；修改：能独立增加根路由；排错：能根据依赖位置、终端日志、状态码和 OpenAPI 判断问题位于环境、编辑器、服务器还是路由。

易错点：终端激活虚拟环境不代表编辑器语言服务一定选择了同一解释器；编辑器没有补全也不等于 Python 代码无法运行。应分别检查终端环境、编辑器解释器和语言服务。

## 12. 完整教程

第 5～10 节按照实际顺序记录了环境检查、虚拟环境、依赖安装、最小应用、服务器启动、接口验证和独立小修改，可以作为本课的完整复习路径。

## 13. 课程总结

- 创建并验证了项目专用 `.venv`，理解了系统环境与项目环境的区别。
- 使用 `requirements.txt` 声明依赖，并将 FastAPI 0.142.2 安装到虚拟环境。
- 创建了 FastAPI 应用对象以及 `GET /health`、`GET /` 两个路由。
- 理解了“HTTP 请求 → 开发服务器 → FastAPI 路由 → 处理函数 → JSON 响应”的最小流程。
- 使用浏览器、Swagger UI、PowerShell、`curl.exe` 和 OpenAPI 进行了多角度验证。
- 排查了 Cursor 中 Anysphere Python 与 Pylance 的语言服务冲突。
- 独立完成了根路由小修改，并通过 Python 编译和 Git 差异检查。
- 本课尚待代码格式小整改、最终 Git 提交和双方确认后定档。
