# NoteMind v0.2 第 01 课：MVP 定档与 Git 分支协作

> 状态：已验收，待提交定档
>
> 验收日期：2026-10-08

本文件是本课唯一的动态教程。课程按检查点推进，只记录核心讲解、实际结果、有复习价值的问题和易错点；全部验收后补全教程与总结并定档。

## 1. 本课目标与边界

完成本课后，学习者应当能够：

- 区分提交、分支、标签和 GitHub Release 的职责。
- 验证 `v0.1.0` 是否准确固定 MVP 提交。
- 从 `main` 创建短期分支，提交当前文档整理改动。
- 推送分支，通过 Pull Request 检查并合并改动。
- 同步并清理已经合并的短期分支。
- 说明为什么一个仓库可以同时保存稳定版本和持续开发历史。

本课只处理版本定档、课程文档和 Git 协作流程，不修改业务代码，不引入复杂分支模型。

## 2. 分工

- AI：解释概念和每条命令，检查仓库状态与实际输出，维护课程文档，指出风险和易错点。
- 学习者：亲手执行本课的 Git 状态检查、分支创建、暂存、提交、推送、Pull Request、合并与清理命令。
- GitHub 网页操作由学习者完成，AI 根据实际结果继续验收。

## 3. 检查点

- [x] A：理解版本对象并确认当前起点
- [x] B：验证并发布 `v0.1.0` 标签
- [x] C：创建短期文档分支
- [x] D：检查、暂存并提交文档整理
- [x] E：推送、创建 Pull Request 并合并
- [~] F：同步、清理、复习与课程定档

## 4. 检查点 A：版本对象与当前起点

### 四个对象分别解决什么问题

- **提交（commit）**：保存某一时刻已经暂存的项目快照，并通过父提交连接成历史。
- **分支（branch）**：指向某个提交的可移动名称；新提交产生后，当前分支会向前移动。
- **标签（tag）**：固定指向某个历史对象的版本名称；发布后通常不再移动。
- **GitHub Release**：基于标签增加面向使用者的版本说明、已知限制和下载入口，它不是新的代码快照。

当前实际状态：

- `main` 与 `origin/main` 都指向 `bcde272 docs: finalize lesson 17`。
- 本地已经存在附注标签 `v0.1.0`，标签说明为 `NoteMind MVP: complete learning edition`。
- `v0.1.0` 准确指向提交 `bcde272`，没有错误地指向本次课程目录整理。
- 工作区包含尚未提交的版本化课程目录、产品路线和教学规则调整。

### 当前要理解的关键关系

```text
v0.1.0（固定）
   ↓
bcde272  ← main / origin/main（当前尚未产生新提交）
   ↑
工作区中的文档整理（还不属于任何提交）
```

下一步先由学习者亲手查看这三个层次，再判断标签是否已经发布到远程。

### 实际结果

学习者已亲手执行状态、提交历史和标签检查并确认结果。AI 随后复核：`main` 与 `origin/main` 仍共同指向 `bcde272`，`v0.1.0` 是带说明的附注标签并准确指向该提交；版本化课程文档仍只在工作区中，没有进入 MVP 标签。

## 5. 检查点 B：验证并发布标签

本地标签和远程标签是两份引用。创建本地标签不会自动把它上传到 GitHub，普通的 `git push` 默认也不保证推送全部标签。因此必须先读取远程状态，再决定是否执行标签推送。

当前步骤只检查远程，不修改本地或 GitHub 内容。

### 实际结果

学习者执行远程标签查询并确认 GitHub 已存在 `v0.1.0`，其剥离后的目标为 `bcde272`。因此不需要重复推送标签；本地和远程已经共同保存 MVP 版本锚点。

## 6. 检查点 C：创建短期文档分支

当前文档改动还在工作区，`main` 尚未产生新提交。创建短期分支后，这些未提交改动会保留在工作区；接下来创建的提交将推动新分支，而不是直接推动 `main`。

本课使用 `docs/versioned-lessons`，因为当前改动只整理文档、课程目录和协作规则，不改变产品功能。

### 实际结果

学习者已创建并切换到 `docs/versioned-lessons`。AI 复核确认 `HEAD` 仍从 `bcde272` 起步，所有未提交文档改动完整保留在工作区，`main` 与 `origin/main` 尚未移动。

## 7. 检查点 D：检查、暂存并提交文档整理

提交前先分三层检查：`git status` 判断文件范围，`git diff --stat` 判断改动规模，`git diff` 阅读实际内容。只有确认没有混入业务代码、环境文件或无关改动后，才能暂存。

学习者已检查改动规模和四个已有文档的正文差异并确认范围符合预期。AI 复核 `git diff --check` 未发现空白错误；当前变化只涉及根 README、`docs/` 和 `lesson/`，没有业务代码或环境文件。

### 暂存结果

学习者使用明确路径暂存 `README.md`、`docs/` 和 `lesson/`。Git 将 17 个旧课程全部识别为重命名，重命名文件均为 0 行内容变化；暂存统计为 25 个文件、310 行新增、35 行删除。`git diff --cached --check` 无输出，暂存后没有遗漏的工作区改动。

暂存检查完成后，AI 又将本段实际结果写入课程文件，因此该文件出现了新的工作区版本。提交前必须再次暂存它，否则提交只会保存上一次 `git add` 时的旧快照。

## 8. 重要问题记录

### 为什么有了版本目录还需要 Git 标签？

版本目录只是在最新代码中整理课程资料；标签会固定整个仓库当时的代码、配置和文档。即使以后移动文件、重写页面，`v0.1.0` 仍能还原完整 MVP。

### 为什么不直接复制或重新克隆一个项目？

同一个仓库的提交历史、分支和标签已经能够同时保存旧版本与新开发。复制项目会产生两份需要维护的历史，不利于追踪功能从哪里演变而来。

## 9. 检查点 E：推送与 Pull Request

学习者重新暂存课程记录后，创建了提交 `0cf019c docs: organize lessons by release`，最终包含 25 个文件、316 行新增、35 行删除；17 个旧课程均为 100% 重命名。随后首次推送并建立上游关系，创建 PR #1，以 `main` 为 base、`docs/versioned-lessons` 为 compare。

PR 是一次将来源分支改动合入目标分支的审查请求。描述应说明修改目的和真实验证结果；没有执行的测试不能写成已通过。

本课采用 Create a merge commit：保留来源分支提交，并创建有两个父提交的合并提交。实际合并提交为 `4a352da`。Squash and merge 会把 PR 改动压成一个新提交；Rebase and merge 会重放来源提交以形成线性历史。企业项目应遵循团队约定，不存在所有项目统一使用的方式。

## 10. 检查点 F：同步与清理

学习者执行 fetch、切换到 main、快进同步，并删除已合并的本地与远程文档分支。AI 复核和学习者终端输出均确认：只剩 `main` 和 `origin/main`，两者指向 `4a352da`，工作区干净。标签 `v0.1.0` 保持指向 `bcde272`。

```text
bcde272 ───────── 4a352da ← main / origin/main
    └── 0cf019c ──┘
    ↑
 v0.1.0
```

删除分支只删除一个引用名称。来源提交已经被 main 的历史保留，因此删除短期分支不会删除主线中的文件和提交。

本课已验证标签发布，尚未验收 GitHub Release 的创建。标签已能固定代码版本；Release 可在需要面向用户发布说明时单独补充，不能把标签推送记为 Release 已发布。

## 11. 完整教程：命令与判断方法

以下命令均在项目根目录 `D:\Program Files (x86)\PycharmProjects\note-learn\note-mind` 执行。它们记录本课实际流程，用于复习，不应从头无条件重复执行。

### A：确认当前起点

```powershell
git status --short --branch
git log --oneline --decorate -3
git show --no-patch --decorate v0.1.0
```

- status 的 `--short` 用两列状态显示暂存区与工作区变化，`--branch` 显示当前分支和上游状态。
- log 的 `--oneline` 每提交显示一行，`--decorate` 显示引用名称，`-3` 限制最近三条。
- show 查看指定标签；`--no-patch` 不展开文件差异。附注标签应显示说明及目标提交。
- 成功判断：标签指向 MVP 提交 bcde272，能够区分提交历史与尚未提交的工作区变化。

### B：查询远程标签

```powershell
git ls-remote --tags origin "v0.1.0*"
```

ls-remote 直接读取远程引用，`--tags` 只查标签，origin 是远程名称，带引号的模式匹配版本引用。附注标签通常有两行：标签对象本身，以及以 `^{}` 结尾的最终提交引用。后一行应指向 bcde272。

本课标签已经存在，无需重复创建或推送。仅在标签确实不存在时，才使用下面的命令固定指定提交并发布：

```powershell
git tag -a v0.1.0 bcde272 -m "NoteMind MVP: complete learning edition"
git push origin v0.1.0
```

tag 的 `-a` 创建附注标签，明确给出 bcde272 防止误标当前最新提交，`-m` 提供说明；push 只推送指定标签。标签名已存在时会拒绝创建，不能为重复练习而删除或强制移动已发布标签。这两条没有在本课重复执行。

### C：创建短期分支

```powershell
git switch -c docs/versioned-lessons
git status --short --branch
```

switch 的 `-c` 创建并切换到从当前提交出发的新分支。未提交改动保留在工作区，后续新提交推动这个分支。成功判断：当前分支名称改变，文档改动仍在。分支已存在时不能重复使用 `-c`。

### D：检查、暂存与提交

```powershell
git --no-pager diff --stat
git --no-pager diff -- README.md docs/backlog.md docs/learning-rules.md lesson/README.md
git add README.md docs lesson
git status --short
git --no-pager diff --cached --stat
git diff --cached --check
```

- `--no-pager` 直接输出，避免进入分页器；`--stat` 看改动规模，`--` 后的路径限定正文检查范围。
- 普通 diff 比较工作区与暂存区，不显示未跟踪新文件。目录移动尚未暂存时可能展示大量删除，应结合 status 和新路径检查。
- add 按明确范围保存当前快照，包含目录里的新增、修改和删除。它不提交也不上传。
- `--cached` 比较暂存区与 HEAD，即下一次提交候选；`--check` 检查常见空白错误，没有输出通常表示通过。
- 成功判断：17 个课程显示 R，暂存范围没有业务代码或环境文件，格式检查通过。

AI 补充课程记录后，文件状态变成 AM：第一列 A 表示暂存新增，第二列 M 表示工作区相对暂存区又有变化。需要再次执行：

```powershell
git add lesson/v0.2-product/01-MVP定档与Git分支协作.md
git commit -m "docs: organize lessons by release"
git status --short --branch
git log -1 --oneline --decorate
```

重新 add 更新快照；commit 把暂存区写入本地历史，`-m` 指定有目的的说明。`docs:` 表示文档变更，后面的内容说明结果。成功判断：出现新提交编号，工作区干净，当前分支指向新提交而 main 尚未移动。

### E：首次推送与合并

```powershell
git push -u origin docs/versioned-lessons
git status --short --branch
```

push 上传当前分支的提交与引用；`-u` 建立本地分支与远程同名分支的上游关系，以后通常可直接执行 git push。成功判断：显示新远程分支和上游设置，status 显示两个分支的跟踪关系。

在 GitHub 创建 PR：base 为 main，compare 为 docs/versioned-lessons。检查 Files changed 后，选择 Create a merge commit 完成合并。成功判断：PR 显示 Merged；这只更新 GitHub 主线，本地 main 仍需同步。

### F：同步与分支清理

```powershell
git status --short --branch
git fetch origin
git switch main
git pull --ff-only
git log --graph --oneline --decorate -6
```

- 先确认工作区干净。fetch 下载远程提交并更新 origin/main，但不切换分支或更新工作区。
- switch main 切换到本地主线。pull 的 `--ff-only` 只允许将本地引用快进到上游位置，出现分叉时会停止，需先查原因。
- 远程有合并提交不妨碍本地快进：本地接收已经存在的历史，无需再次执行合并。
- log 的 `--graph` 展示父子关系。成功判断：main 与 origin/main 指向同一个合并提交，MVP 标签保持不动。

```powershell
git branch -d docs/versioned-lessons
git push origin --delete docs/versioned-lessons
git fetch --prune origin
git branch -a
git status --short --branch
```

- branch 的 `-d` 删除已合并的本地分支，并在检查不通过时拒绝；不要机械改成强制删除的 `-D`。
- push 的 `--delete` 删除指定远程分支；若已在网页删除，应跳过该条。
- fetch 的 `--prune` 清理远程已不存在的跟踪引用；branch 的 `-a` 查看本地及远程跟踪分支。
- 成功判断：文档分支消失，只剩 main 与 origin/main，工作区干净且同步。

## 12. 常见错误与实际踩坑

- LF/CRLF 提醒通常是 Windows 换行提示，不代表暂存失败。
- Git 索引只读导致 AI 的 git mv 失败后，AI 在工作区移动文件；学习者随后暂存，Git 仍将全部旧课程识别为 100% 重命名。
- 暂存不是实时同步；课程记录在 add 后更新，必须再次 add。
- PowerShell 出现 `>>` 表示等待补全输入。本次学习者用 Ctrl+C 取消，再重新执行完整 status 命令，正常得到 main...origin/main；取消这次输入没有影响仓库。
- 删除本地分支、删除 GitHub 分支和清理远程跟踪引用是不同操作，应按实际状态处理。

## 13. 复习与小练习

先自行复述，再对照答案，不强制逐题发送文字。

1. 创建分支是否会复制整个项目？参考答案：分支主要是提交引用，工作区在切换后展示对应快照。
2. 为什么 add 后修改文件还要再次 add？参考答案：暂存区保存执行 add 当时的快照。
3. fetch、pull、push 分别做什么？参考答案：fetch 取得远程历史并更新跟踪引用；pull 将上游变化整合到当前分支；push 更新远程引用并发送所需提交。
4. 为什么合并后还要同步本地 main？参考答案：GitHub 与本地分别保存引用，网页操作不会自动更新本地。
5. 删除已合并分支会丢失文件吗？参考答案：main 已保留提交与快照，删除来源分支只是移除名称。
6. main 更新后标签会跟着移动吗？参考答案：标签固定原对象，正常发布流程不移动它。

小练习：不用执行命令，说明下一课开发前端应用骨架时，从同步的 main 开始应经过哪些步骤，并解释每步目的。应覆盖：建分支 → 实现与验收 → 审 diff → 暂存提交 → 首次推送绑定上游 → PR 检查合并 → 同步 main → 清理分支。

## 14. 课程总结与验收状态

本课实际完成了 MVP 标签核验、版本化课程整理、短期分支创建、差异审查、快照更新、提交、首次推送、PR #1 合并、本地主线同步及分支清理。实现提交为 0cf019c，合并提交为 4a352da。

AI 负责维护文档和只读复核；学习者亲手完成 Git 与 GitHub 操作。业务代码没有变化，因此本课没有运行业务测试；验证范围为文档差异、重命名完整性、空白检查和 Git 历史关系。

学习者已完成自查并明确确认“本课验收通过”，双方确认本课验收通过。版本课程索引已标记验收完成；当前仅剩收尾文档提交与推送，完成后进入下一课。检查点 F 保留进行中，直到收尾提交核验完成。

### 收尾提交

本次实现已经通过 PR #1 合并并清理分支。收尾只补充该课的完整教程与验收状态，由学习者在同步的 main 上完成一次文档提交；这是本课定档的简化处理，下一课业务开发继续使用短期功能分支。

在项目根目录执行：

```powershell
git diff --check
git --no-pager diff --stat
git add lesson/v0.2-product
git diff --cached --check
git commit -m "docs: finalize v0.2 lesson 01"
git push
git status --short --branch
```

先检查工作区格式和改动范围，再暂存该版本课程目录，复核暂存区格式。commit 保存教程与验收记录；push 使用 main 已有的 origin/main 上游关系发布提交。最后应显示 main...origin/main 且没有文件列表。若远程拒绝直接推送主线，应保留提交并按仓库保护规则改用 PR，不强制推送。

下一课准确会话名称：`NoteMind v0.2 第02课：前端应用骨架`。
