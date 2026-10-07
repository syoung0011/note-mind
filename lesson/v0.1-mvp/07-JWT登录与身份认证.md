# 第 7 课：JWT 登录与身份认证

> 状态：已完成
>
> 验收日期：2026-10-04

本文件是本课唯一的动态教程。每个阶段只记录目标、核心讲解、实际结果和易错点；全部验收后再补全完整教程、课程总结并定档。

## 1. 本课目标与边界

完成本课后，学习者应当能够：

- 说明登录与注册的区别，以及登录请求经过的主要层。
- 使用保存的 Argon2id 哈希校验密码，始终返回统一的登录失败信息。
- 说明 JWT 的载荷、签名和过期时间分别解决什么问题。
- 签发带 `sub` 和 `exp` 的访问令牌，并通过 Bearer Token 识别当前用户。
- 使用受保护的 `GET /api/auth/me` 验证有效、缺失、伪造和过期令牌。
- 说明第一版无状态 JWT 的退出登录方式和限制。

本课只实现后端登录、JWT 签发、当前用户依赖和 `/api/auth/me`。不实现前端登录页面、路由保护、刷新令牌、服务端令牌黑名单、角色权限和第三方 OAuth 登录。

第一版的“退出登录”由客户端删除保存的访问令牌完成；签发后尚未过期的令牌不会被服务端主动撤销。需要即时撤销时必须额外设计黑名单、令牌版本或会话存储，超出本课范围。

## 2. 核心链路

```text
POST /api/auth/login
        ↓
规范化用户名并查询 users
        ↓
用 Argon2id 校验明文密码与 password_hash
        ↓
签发带 sub、exp 的 JWT
        ↓
返回 access_token 与 token_type=bearer

GET /api/auth/me
        ↓
读取 Authorization: Bearer <token>
        ↓
验证签名、算法和过期时间
        ↓
读取 sub 并查询当前用户
        ↓
返回 UserPublic（不含 password_hash）
```

JWT 是“已签名”而不是“已加密”：客户端可以读取载荷，因此令牌中不能放密码、密码哈希或其他敏感信息。签名用于发现篡改，`exp` 用于限制有效期，`sub` 用于标识令牌对应的主体。本项目计划把稳定的用户 `id` 字符串写入 `sub`，再从数据库加载当前用户。

## 3. AI 与学习者分工

AI 负责：

- 解释密码校验、JWT、Bearer Token、FastAPI 依赖注入和统一 `401` 响应。
- 在真实项目文件中提供最小样例或带少量 `TODO(learner)` 的骨架。
- 审阅密钥配置、算法固定、过期时间、异常处理和响应过滤。
- 检查实际代码与验收结果，并维护本课教程。

学习者优先体验：

- 生成自己的 JWT 签名密钥并写入被 Git 忽略的 `backend/.env`。
- 完成密码校验、登录查询和令牌签发的核心连接代码。
- 启动后端，在 `/docs` 登录并使用 Authorize 调用受保护接口。
- 亲手验证正确密码、错误密码、缺失令牌和无效令牌。
- 完成一个小修改，检查 Git 差异并创建本课提交。

单独说“继续”只推进一个检查点；需要 AI 代做当前步骤时，可以明确说“给答案”或“帮我实现”。

## 4. 预计修改

```text
backend/requirements.txt          增加 PyJWT 依赖
backend/.env.example              记录 JWT 配置项名称，不放真实密钥
backend/app/config.py             加载签名密钥、算法和过期时间
backend/app/security.py           校验密码、签发和解析访问令牌
backend/app/schemas/              定义登录令牌响应模型
backend/app/routers/auth.py       增加登录和当前用户接口
lesson/07-JWT登录与身份认证.md    本课动态教程
lesson/README.md                  课程状态
```

本课不需要修改数据库结构，因此正常情况下不创建 Alembic 迁移。

## 5. 检查点进度

- [x] A：确认课程衔接、现有认证基础和本课边界
- [x] B：理解 JWT、确定接口契约并配置依赖与密钥
- [x] C：实现密码校验与登录签发访问令牌
- [x] D：实现当前用户依赖与 `/api/auth/me`
- [x] E：完成有效、错误、缺失、伪造和过期场景验收
- [x] F：完成小修改、复习、Git 提交和课程定档

## 6. 检查点 A：课程衔接与现状

第 6 课已经验收并提交，当前工作区干净。现有后端已经具备 `users` 表、SQLAlchemy 会话、注册输入与公开响应模型、Argon2id 密码哈希和 `POST /api/auth/register`，因此本课可以在不修改数据库结构的前提下完成登录和身份识别。

当前 `security.py` 只能生成密码哈希，还不能验证密码或处理 JWT；配置只包含数据库连接；认证路由只有注册接口；项目也尚未声明 PyJWT 依赖。这些正是后续检查点需要补齐的最小范围。

本课采用 FastAPI 官方安全教程使用的 PyJWT、`pwdlib`、OAuth2 Password 表单和 Bearer Token 组合。登录地址仍使用产品需求中的 `/api/auth/login`，并把它配置为 OpenAPI 的 token URL，使 `/docs` 的 Authorize 功能能够复用同一接口。

参考资料：

- [FastAPI：OAuth2、Bearer 与 JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [PyJWT 使用文档](https://pyjwt.readthedocs.io/en/stable/usage.html)

易错点：

- JWT 载荷只是 Base64URL 编码，不是加密内容。
- 解码时必须固定允许的算法，不能相信令牌头部自己声明的任意算法。
- JWT 密钥必须来自环境变量，不能提交真实密钥，也不能复制教程中的示例密钥。
- “用户名不存在”和“密码错误”应返回相同的 `401` 信息，避免帮助攻击者枚举账号。
- `401` 响应应带 `WWW-Authenticate: Bearer`，告诉客户端当前接口需要 Bearer 身份凭证。
- 仅成功解码令牌还不够；仍需查询数据库，确认 `sub` 指向的用户真实存在。

## 7. 检查点 B：JWT、接口契约与安全配置

JWT 通常写成由两个点分隔的三段字符串：

```text
header.payload.signature
```

- `header`：说明令牌类型和签名算法。
- `payload`：保存声明；本项目使用 `sub` 保存用户 ID，使用 `exp` 保存过期时间。
- `signature`：服务端用密钥生成，用于发现 header 或 payload 是否被篡改。

前两段可以被客户端解码查看，因此 JWT 的安全性不依赖“别人看不懂”，而依赖密钥没有泄露、服务端固定验证算法、签名有效且令牌没有过期。

本课确定的接口契约如下：

```text
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=alice&password=example-password

成功：200 OK
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}

GET /api/auth/me
Authorization: Bearer <jwt>

成功：200 OK
{
  "id": 1,
  "username": "alice",
  "created_at": "..."
}
```

登录采用 OAuth2 Password 表单而不是 JSON，是为了让 FastAPI 的 `OAuth2PasswordBearer`、OpenAPI 和 `/docs` 的 Authorize 操作形成一条标准链路。这里使用 OAuth2 的密码流工具并不表示项目接入了第三方 OAuth 平台。

失败规则：

- 用户名不存在或密码错误：统一返回 `401 Incorrect username or password`。
- 缺少、篡改、过期或找不到对应用户的令牌：统一返回 `401 Could not validate credentials`。
- 两类 `401` 都返回 `WWW-Authenticate: Bearer`。

配置约定：

- `JWT_SECRET_KEY`：必须由学习者随机生成，只写入 `backend/.env`，没有代码默认值。
- `JWT_ALGORITHM`：第一版固定为 `HS256`。
- `ACCESS_TOKEN_EXPIRE_MINUTES`：第一版使用 30 分钟。

AI 已完成非敏感骨架：依赖清单加入 `PyJWT`，`.env.example` 加入配置项示例，`Settings` 声明三个 JWT 配置字段。真实 `.env` 尚未由 AI 读取或修改。

### 7.1 学习者实践

在项目根目录安装依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

用途：按照依赖清单安装 PyJWT。成功标志是命令正常结束，随后下面的检查能显示 PyJWT 版本：

```powershell
.\.venv\Scripts\python.exe -m pip show PyJWT
```

仍在项目根目录生成 32 字节随机密钥：

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

该命令只输出随机文本，不修改文件。把输出复制到 `backend/.env`，并补充以下三行；不要把真实值发到聊天中：

```dotenv
JWT_SECRET_KEY=这里替换为刚生成的随机值
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

不要覆盖 `.env` 中现有的 `DATABASE_URL`。完成后只需回复“确认”；AI 将检查配置项名称和依赖状态，但不会显示或记录真实密钥。

易错点：`.env.example` 只放占位值，不能把真实密钥复制进去；JWT 密钥与数据库密码用途不同，不能共用；`token_type` 的标准响应值是小写 `bearer`，请求头方案通常写作 `Bearer`。

学习者完成依赖安装和真实环境配置后，AI 进行了不显示密钥内容的核验：PyJWT 版本为 2.15.1；签名密钥存在且长度为 64 个字符；算法为 `HS256`；过期时间为 30 分钟；`backend/.env` 仍被 `.gitignore` 忽略且未被 Git 跟踪。检查点 B 验收通过。

## 8. 检查点 C：密码校验与登录签发

AI 已在 `security.py` 中提供两个完整工具样例：

- `verify_password` 使用与注册相同的 `PasswordHash` 实例，将本次明文密码与数据库哈希进行校验。
- `create_access_token` 使用 UTC 当前时间加配置的分钟数生成 `exp`，把传入主体写入 `sub`，再用固定配置的算法和密钥签名。

还增加了 `DUMMY_PASSWORD_HASH`。如果用户名不存在，登录流程仍对这个固定用途的哈希执行一次昂贵的 Argon2 校验，使“用户不存在”和“密码错误”的处理耗时更接近，降低通过响应时间枚举用户名的风险。

`Token` 是登录成功的公开响应模型，只包含 `access_token` 和 `token_type`。登录路由已经接收 `OAuth2PasswordRequestForm` 与数据库会话，但核心流程保留为 `TODO(learner)`，当前会明确返回 `501`。

### 8.1 学习者实践

请在 `backend/app/routers/auth.py` 的 `login_for_access_token` 中完成四个步骤：

1. 将表单用户名执行 `strip().lower()`，使用 `select(User).where(...)` 查询用户。
2. 用户不存在时，先用表单密码校验 `DUMMY_PASSWORD_HASH`，再抛出统一的 `401`。
3. 用户存在但 `verify_password(form_data.password, user.password_hash)` 为假时，抛出同一个 `401`。
4. 使用 `create_access_token(str(user.id))` 签发令牌，返回 `Token(access_token=..., token_type="bearer")`。

你需要从 `app.security` 导入 `DUMMY_PASSWORD_HASH`、`verify_password` 和 `create_access_token`。两个失败分支应使用完全相同的异常：

```python
HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
```

完成后删除 `TODO(learner)` 和临时 `501`。本检查点暂不启动服务；回复“确认”后，AI 会先读取实际实现、修正问题并用不依赖 HTTP 服务的检查验证密码校验和令牌载荷，再进入检查点 D。

易错点：不能直接比较明文密码和哈希字符串；不能把用户名或密码写入令牌；`sub` 按 JWT 约定应是字符串；用户名必须与注册时采用同样的规范化规则。

学习者完成了登录流程的主要结构：查询用户、验证真实密码、失败时返回统一 `401`，以及使用用户 ID 签发令牌。AI 审阅后整改了三个问题：

- 查询前补充 `strip().lower()`，保持登录与注册的用户名规则一致。
- 将“用户不存在”和“密码错误”拆成两个分支，确保前者确实执行 `DUMMY_PASSWORD_HASH` 校验；写成 `user is None or ...` 会因短路而跳过右侧表达式。
- `Token` 是 Pydantic 模型，必须使用字段名构造，不能像普通位置参数函数一样传入两个值。

整改后，检查点 C 的代码结构满足登录签发要求。

## 9. 检查点 D：当前用户依赖与 `/api/auth/me`

登录成功只代表客户端拿到了令牌。受保护接口还需要完成反方向的数据流：从请求头提取 Bearer Token，验证 JWT，再根据 `sub` 查询数据库用户。

本检查点将使用 FastAPI 依赖链：

```text
/api/auth/me
    → Depends(get_current_user)
        → Depends(oauth2_scheme) 提取 Bearer Token
        → Depends(get_db) 提供数据库会话
        → jwt.decode 验证签名、算法和 exp
        → 使用 sub 查询 User.id
    → UserPublic 过滤并返回公开字段
```

`OAuth2PasswordBearer` 只负责从请求头取出令牌，并在缺少 Bearer 凭证时生成认证错误；它不会自动验证 JWT，也不会自动查询用户。真正的身份确认由 `get_current_user` 完成。

AI 已创建依赖骨架和完整的 `/api/auth/me` 路由。路由本身只声明 `Depends(get_current_user)` 并返回得到的用户，FastAPI 会先执行整个依赖链；只要依赖抛出异常，路由函数就不会执行。

### 9.1 学习者实践

请在 `backend/app/routers/auth.py` 的 `get_current_user` 中完成四个步骤：

1. 在 `try` 中调用：

   ```python
   payload = jwt.decode(
       token,
       settings.jwt_secret_key,
       algorithms=[settings.jwt_algorithm],
   )
   ```

2. 读取 `subject = payload.get("sub")`，并用 `user_id = int(subject)` 转成数据库主键。
3. 捕获 `(InvalidTokenError, TypeError, ValueError)`，统一 `raise credentials_exception`。
4. 使用 `user = db.get(User, user_id)` 查询用户；不存在时抛出同一个异常，存在时返回 `user`。

完成后删除 `TODO(learner)` 和末尾的临时 `raise credentials_exception`。不要把算法写成从令牌 header 动态读取；`algorithms=[settings.jwt_algorithm]` 表示服务端只接受自己配置的算法。

暂时仍不启动服务。完成后回复“确认”，AI 会审阅实际代码，并离线验证有效、篡改和过期令牌，再进入真实 HTTP 验收。

易错点：`jwt.decode` 会同时验证签名和 `exp`；`payload.get("sub")` 可能缺失或类型错误，不能直接信任；令牌中的用户 ID 即使格式正确，对应用户也可能已被删除，所以必须再次查询数据库。

学习者完成了“解码令牌、读取 `sub`、查询用户、返回用户”的主流程，说明已经理解当前用户依赖的调用顺序。AI 审阅后整改了以下认证边界：

- 原实现 `jwt.decode(token)` 没有传入签名密钥和固定算法，既不能按 PyJWT 当前接口正确完成验证，也没有表达服务端只信任自身算法配置的安全要求。
- 原实现直接使用 `["sub"]` 和 `int(...)`，没有把无效签名、过期、缺少 `sub` 和错误类型统一转换为认证失败。
- 原实现创建了 `credentials_exception` 却没有复用；用户不存在时返回了空 `detail` 且缺少 `WWW-Authenticate`。整改后所有无效凭证统一返回同一个 `401`。
- 用户按主键加载改用 `db.get(User, user_id)`，更直接表达“按主键取得一个用户”；原来的 `select` 查询本身也能工作，并非逻辑错误。

整改后的依赖使用密钥和固定算法解码，在 `try` 中解析主体，将 `InvalidTokenError`、`TypeError` 和 `ValueError` 统一转换为 `credentials_exception`，随后查询数据库并确认用户仍然存在。检查点 D 完成。

## 10. 检查点 E：真实 HTTP 验收

本检查点将启动真实 FastAPI 服务并使用已注册账号验证：

1. 正确用户名和密码返回 `200`、`access_token` 与 `token_type=bearer`。
2. 错误密码与不存在用户名均返回相同的 `401 Incorrect username or password`。
3. 有效 Bearer Token 调用 `/api/auth/me` 返回对应公开用户，不包含 `password_hash`。
4. 缺少、无效、篡改和过期令牌均返回 `401`，并带 `WWW-Authenticate: Bearer`。
5. `/docs` 的 Authorize 操作能够通过 `/api/auth/login` 获取并携带令牌。

进入实际服务验收前，AI 先通过离线测试覆盖有效、篡改、过期、缺少主体和用户不存在分支；真实 HTTP 启动和页面操作仍由学习者完成。

AI 的离线检查确认：有效令牌能够取得用户；篡改、过期、缺少 `sub` 和用户不存在均返回带 `WWW-Authenticate: Bearer` 的 `401`；OpenAPI 中已经包含登录、当前用户接口及 Bearer 安全声明。

学习者随后启动真实 FastAPI 服务并确认检查点 E 的验收结果：正确凭证能够登录并取得 Bearer Token，错误密码返回统一 `401`，Swagger UI 的 Authorize 可以携带令牌调用 `/api/auth/me`，公开响应不包含密码哈希，退出授权后缺少凭证以及手工提供无效令牌均返回 `401`。检查点 E 验收通过。

## 11. 检查点 F：小修改、复习与定档

当前登录接口运行时会返回 `401`，但路由装饰器尚未像注册接口的 `409` 一样显式记录该业务响应。本课的小修改是在登录接口的 OpenAPI 定义中补充：

```python
responses={
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Incorrect username or password",
    },
},
```

请把它加入 `@router.post("/login", ...)`。这不会改变运行逻辑，只让 `/docs` 提前告诉接口使用者登录可能返回 `401`。

完成后回复“确认”。AI 将评阅这次小修改，执行最终编译、依赖、OpenAPI 与 Git 差异检查，然后给出复习参考答案和由学习者亲手执行的提交命令。

学习者在正确的登录路由装饰器中加入了 `401` 响应说明，修改范围准确，没有改变运行逻辑。AI 仅将单行字典整理为与现有注册路由一致的多行格式，提高可读性；业务内容未改变。

## 12. 复习问题与参考答案

1. **注册和登录有什么区别？** 注册验证新账号数据、生成密码哈希并创建用户；登录查询已有用户、验证明文密码与保存的哈希，成功后签发访问令牌。
2. **JWT 为什么不是加密？** header 和 payload 可以被客户端解码查看；签名只能证明内容未被篡改且由持有密钥的一方签发，所以令牌中不能放密码等秘密。
3. **`sub` 和 `exp` 分别表示什么？** `sub` 标识令牌主体，本项目保存字符串形式的用户 ID；`exp` 是过期时间，限制令牌有效期。
4. **为什么解码时要显式传入 `algorithms=[settings.jwt_algorithm]`？** 服务端必须固定自己允许的算法，不能相信不可信令牌自己声明的任意算法。
5. **为什么解码成功后还要查询数据库？** 令牌只能证明签发时的身份信息；用户可能已被删除，后续笔记接口也需要真实用户对象来实现数据隔离。
6. **`OAuth2PasswordBearer` 做了什么？** 它从 `Authorization: Bearer <token>` 中提取令牌并为 OpenAPI 声明安全方案，但不负责验证 JWT 或查询用户。
7. **第一版如何退出登录？** 客户端删除保存的访问令牌；没有黑名单时，已经签发且未过期的令牌不能被服务端即时撤销。

小练习已完成：为登录接口的 OpenAPI 定义显式补充 `401` 响应说明。

## 13. 完整教程

本课从第 6 课的用户注册基础继续。配置层新增 JWT 签名密钥、固定算法和访问令牌有效期；真实密钥只保存在被 Git 忽略的 `.env`，`.env.example` 只记录配置项名称和占位值。项目加入 PyJWT，继续复用 `pwdlib` 的 Argon2id 密码哈希能力。

登录接口采用 OAuth2 Password 表单。收到请求后，用户名使用与注册相同的 `strip().lower()` 规则规范化，再查询 `users` 表。用户不存在时仍执行一次假哈希校验，降低响应时间差异造成的用户名枚举风险；用户存在时验证真实密码。两种失败统一返回带 `WWW-Authenticate: Bearer` 的 `401`。

登录成功后，服务端把字符串形式的用户 ID 放入 JWT 的 `sub`，把 UTC 当前时间加 30 分钟写入 `exp`，使用环境密钥和固定的 HS256 算法签名，然后返回 `access_token` 和 `token_type=bearer`。

受保护接口通过 `OAuth2PasswordBearer` 提取请求头中的令牌，再由 `get_current_user` 使用固定算法验证签名和过期时间。依赖把 `sub` 转为用户主键并重新查询数据库；无效、过期、主体格式错误或用户不存在都统一返回认证失败。`/api/auth/me` 依赖该结果，并使用 `UserPublic` 保证响应不泄露密码哈希。

学习者通过真实 FastAPI 服务和 Swagger UI 验证了登录、错误密码、Authorize、当前用户、退出授权和无效令牌。AI 还离线验证了篡改、过期、缺少主体和用户不存在的分支。

### 13.1 重要命令

在项目根目录安装本课依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

它安装依赖清单中的 PyJWT；`pip show PyJWT` 能显示包名和版本时表示成功。

在项目根目录生成随机签名密钥：

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

它只输出一个 32 字节随机值，需要由学习者复制到 `backend/.env` 的 `JWT_SECRET_KEY`；不能提交或发送该真实值。

在项目根目录启动开发服务：

```powershell
.\.venv\Scripts\fastapi.exe dev .\backend\app\main.py
```

终端显示监听 `http://127.0.0.1:8000` 且 `/docs` 可以打开时表示成功；验收完成后按 `Ctrl+C` 停止服务。

## 14. 课程总结

- 使用 Argon2id 验证密码，并统一处理账号不存在与密码错误。
- 使用 PyJWT 签发包含 `sub` 和 `exp` 的 HS256 访问令牌。
- 将 JWT 密钥放入环境变量，避免真实秘密进入版本管理。
- 使用 OAuth2 Password 表单和 Bearer Token 建立 FastAPI/OpenAPI 认证链路。
- 实现可复用的 `get_current_user` 依赖和受保护的 `/api/auth/me`。
- 验证了有效、错误、缺失、篡改、过期和用户不存在等认证分支。
- 明确了无状态 JWT 的客户端退出方式及无法即时撤销的限制。
- 为登录接口补充了 OpenAPI `401` 响应说明。

## 15. 验收与定档

功能实现、真实 HTTP 验收和小修改已经完成。最终技术检查结果：Python 编译通过，`pip check` 未发现依赖冲突，OpenAPI 登录响应包含 `200`、`401`、`422`，`/api/auth/me` 包含 OAuth2 Bearer 安全声明，`git diff --check` 未发现空白错误；真实 `.env` 仍被忽略且未被 Git 跟踪。

学习者亲手检查 Git 差异并创建提交 `ef723cc feat: add JWT authentication`。该提交包含 JWT 配置、安全工具、登录与当前用户接口、响应模型、依赖、课程记录和协作规则调整；真实 `backend/.env` 未被跟踪，提交后工作区干净。

学习者已于 2026-10-04 明确确认所有验收与提交步骤完成，本课验收通过，教程和课程总结现已定档。

下一课准确会话名称：`NoteMind 第08课：创建与查询笔记`。
