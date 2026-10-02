# 第 1 课：Git 与项目起点

> 状态：进行中——等待学习者实现
>
> 当前检查点：E——创建并验证第一个提交

本文件是本课唯一的动态教程。每个阶段只记录核心讲解、实际结果和易错点，不保存逐轮问答流水；全部验收后补全总结并定档。

## 1. 本课目标与分工

完成本课后，学习者应当能够说明 NoteMind MVP 的核心流程，区分普通文件夹与 Git 仓库，理解工作区、暂存区和提交，并独立完成第一次提交。

AI 负责维护教程、解释概念、检查实际状态和整改问题；学习者负责创建 `.gitignore`，亲手执行 Git 初始化、暂存、检查和提交命令。

## 2. 检查点进度

- [x] A：确认当前目录、文件和 MVP 起点
- [x] B：理解忽略规则并亲手创建 `.gitignore`
- [x] C：初始化 Git 仓库并认识工作区
- [x] D：选择改动进入暂存区并检查差异
- [ ] E：创建并验证第一个提交
- [ ] F：完成自查、小练习、总结与定档

## 3. 检查点 A：项目起点与 MVP

项目最初只有 `README.md`、`docs/` 和 `lesson/`，没有 `.git/`，因此只是普通文件夹，不是 Git 仓库。

NoteMind MVP 的核心用户流程是：

```text
注册 → 登录 → 创建笔记 → 建立知识索引 → 提问 → 获得带引用的回答
```

易错点：不要把“完善项目结构”等开发动作当成用户获得价值的产品流程。

## 4. 检查点 B：`.gitignore`

学习者创建了 `.gitignore`，AI 检查整改后的规则为：

```gitignore
.env
.venv/
__pycache__/
node_modules/
dist/
.idea/
.vscode/
```

`.gitignore` 让匹配规则的未跟踪文件默认不进入版本管理。它不会删除文件，也不能自动停止跟踪已经提交过的文件。

易错点：Vue/Vite 默认构建目录是 `dist/`；VS Code 配置目录是 `.vscode/`；`.env` 是环境配置文件，不是依赖包。

## 5. 检查点 C：初始化 Git

已执行：

```powershell
git init
git branch -M main
git status
```

结果：`.git/` 已创建，当前分支为 `main`，仓库尚无提交。

- `.git/` 保存仓库元数据、配置和提交历史。
- `.gitignore` 是工作区中的普通规则文件。
- `Untracked files` 指尚未通过 `git add` 纳入 Git 索引的文件，与创建时间无关。

易错点：删除 `.git/` 会丢失本地版本历史，但不会直接删除工作区中的项目文件。

## 6. 检查点 D：暂存并检查

已执行：

```powershell
git add README.md .gitignore docs lesson
git status
git diff --cached --stat
git diff --cached -- .gitignore
```

```text
工作区 --git add--> 暂存区 --git commit--> 本地提交历史
```

结果：7 个文件进入暂存区，仓库提交数仍为 0。暂存区保存下一次本地提交准备记录的文件版本，与远程上传无关。

易错点：

- `git add` 保存执行当时的快照；之后继续修改文件，需要再次暂存。
- LF/CRLF 信息是 Windows 换行提醒，不代表暂存失败。
- Git 差异进入分页器时可按 `q` 退出，或使用 `git --no-pager diff ...`。

## 7. 检查点 E：创建并验证第一个提交

当前课程文件和学习规则在首次暂存后又被更新，因此提交前需要重新暂存。下一步将检查最终暂存内容、创建提交并验证仓库状态。

在项目根目录执行：

```powershell
git add README.md .gitignore docs lesson
git status
git diff --cached --stat
git commit -m "chore: initialize NoteMind project"
git status
git log --oneline -1
```

- 再次 `git add`：更新暂存区中的文档快照。
- `git commit`：将暂存区保存为本地提交；`chore` 表示项目准备工作，不是用户功能。
- 验证成功：提交命令显示提交编号，随后工作区干净，`git log` 显示刚创建的提交。

易错点：提交只包含暂存区中的版本；`git commit` 仍然不会上传远程仓库。如果 Git 提示缺少用户名或邮箱，应按提示配置自己的真实身份后重试，不要随意填写。

## 8. 完整教程

当前第 3～7 节构成本课教程主体，检查点 E 和最终验收完成后定档。

## 9. 课程总结

待最终验收通过后填写。
