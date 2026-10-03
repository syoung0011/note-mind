# 第 3 课：Vue 最小前端

> 状态：已完成
>
> 验收日期：2026-10-03

本文件是本课唯一的动态教程。每个阶段只记录核心讲解、实际结果和易错点，不保存逐轮问答流水；全部验收后补全总结并定档。

## 1. 本课目标与边界

完成本课后，学习者应当能够：

- 说明浏览器、Vite 开发服务器、Vue 应用和组件之间的关系。
- 解释 `package.json`、`src/main.js` 和 `src/App.vue` 的基本职责。
- 使用 Vue 官方脚手架创建并启动最小前端。
- 独立修改页面内容，并通过浏览器与生产构建验证结果。

本课只建立可运行的 Vue 3 前端并理解最小渲染流程，不连接 FastAPI，不加入路由、Pinia、TypeScript、测试框架或复杂样式。前后端通信留到第 4 课。

## 2. AI 与学习者分工

AI 负责：

- 检查环境与上一课状态。
- 解释脚手架选项、项目结构和页面渲染流程。
- 维护本课程文件，检查生成的代码并协助整改。
- 在学习者运行后独立核对页面和构建结果。
- 对首次出现的 Vue 写法提供最小样例或带 `TODO(learner)` 注释的模板；学习者选择跳过时直接补全并继续。

学习者优先体验：

- 亲手执行 Vue 项目初始化和依赖安装命令。
- 查看生成文件并创建 NoteMind 最小首页。
- 启动开发服务器，完成浏览器验收和一个小修改。
- 亲手执行构建与 Git 提交。

以上练习用于帮助理解，不是阻塞关卡。学习者可以要求查看答案或继续，AI 会补全缺失实现并如实记录实际分工；最终仍以文件、运行结果、构建和 Git 状态完成为验收依据。

## 3. 核心流程

```text
浏览器访问本地地址
        ↓
Vite 开发服务器返回前端资源
        ↓
浏览器执行 src/main.js
        ↓
Vue 创建应用并挂载到页面节点
        ↓
App.vue 渲染为用户看到的界面
```

- **Node.js**：让前端开发工具可以在本机运行；最终页面中的 JavaScript 仍由浏览器执行。
- **npm**：根据 `package.json` 管理依赖并运行项目脚本。
- **脚手架**：按照一套模板生成项目起点，减少手工配置，但生成后仍需理解关键文件。
- **Vite**：提供本地开发服务器和生产构建能力。
- **Vue 应用**：管理组件和响应式界面，并挂载到 HTML 中的指定节点。
- **单文件组件**：将组件的模板、逻辑和样式组织在一个 `.vue` 文件中。

## 4. 本课预计文件

```text
note-mind/
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       └── assets/
└── lesson/
    └── 03-Vue最小前端.md
```

脚手架的实际版本可能生成少量其他文件；检查后再决定保留或删除，不预先照抄固定目录。

## 5. 检查点进度

- [x] A：确认课程衔接、Node.js 环境和技术方案
- [x] B：使用官方脚手架创建最小 Vue 项目
- [x] C：安装依赖并认识关键文件
- [x] D：使用样例完成 NoteMind 最小首页
- [x] E：启动开发服务器并完成 HTTP 验收
- [x] F：完成小修改、生产构建、自查和 Git 提交

## 6. 检查点 A：环境与方案

AI 在项目根目录执行了只读检查：

```powershell
node --version
npm --version
```

实际结果：Node.js 为 `v24.12.0`，npm 为 `11.7.0`。Vue 官方当前快速上手要求 Node.js `^22.18.0 || >=24.12.0`，因此本机版本满足要求。

本课采用 Vue 官方推荐的 `create-vue` 创建基于 Vite 的 Vue 3 项目。为了保持学习范围有限，所有可选功能先选 `No`；需要路由、状态管理和测试时，再在对应课程中引入。

易错点：旧教程中的 Vue CLI 已处于维护模式；新项目应使用 `create-vue`，不要把 `vue create` 和 `npm create vue@latest` 混为同一套工具。

## 7. 检查点 B：创建项目

请学习者在项目根目录亲手执行：

```powershell
npm create vue@latest frontend
```

命令作用：

- npm 临时获取并运行 Vue 官方脚手架 `create-vue`。
- `frontend` 是要创建的目录名。
- 命令会写入前端项目骨架，但此时依赖通常尚未安装。

出现选项时，本课统一选择：

```text
TypeScript: No
JSX: No
Vue Router: No
Pinia: No
Vitest: No
End-to-End Testing: No
ESLint: No
Prettier: No
Vue DevTools: No
```

选择这些答案不是否定工具价值，而是先只学习 Vue、组件和开发服务器。命令结束后看到项目创建成功提示，并且根目录出现 `frontend/`，即可把完整终端输出发给 AI 检查。

学习者已在项目根目录执行该命令。当前版本的 `create-vue@3.24.0` 将多个可选功能合并为多选界面；学习者选择了 JavaScript、附加功能 `none`、试验特性 `none`，并保留官方示例代码，结果符合本课边界。

AI 检查结果：

- `frontend/` 已生成，包含 `package.json`、`index.html`、`vite.config.js`、`src/main.js`、`src/App.vue` 和示例组件。
- `package.json` 声明了 Vue `^3.5.42`、Vite `^8.2.2` 及 `dev`、`build`、`preview` 三个脚本。
- `src/main.js` 使用 `createApp(App).mount('#app')` 将根组件挂载到 `index.html` 的 `#app` 节点。
- `frontend/.git` 不存在，说明没有误建嵌套仓库。
- 脚手架提示中的 `git init` 不执行，因为整个 NoteMind 已由项目根目录的 Git 仓库管理。

npm 显示的新版本通知只是一条工具升级提示，不影响初始化结果，本课不升级 npm。

## 8. 检查点 C：安装依赖与入口关系

学习者在 `frontend/` 目录亲手执行：

```powershell
npm install
npm list --depth=0
```

实际结果：npm 成功安装 120 个包，没有出现 `npm ERR!`；直接依赖检查显示 Vue `3.5.43`、Vite `8.3.2`、`@vitejs/plugin-vue` `6.0.9` 和 `vite-plugin-vue-devtools` `8.2.1`。

`npm install` 根据 `package.json` 的版本范围解析并下载依赖，同时生成 `package-lock.json`。`package.json` 表达项目允许使用的依赖范围和可执行脚本；`package-lock.json` 保存本次解析出的精确依赖树，让其他环境更容易得到一致安装结果；`node_modules/` 保存本机安装结果，可以根据前两个文件重新生成，因此不提交 Git。

AI 检查确认：`package-lock.json` 已生成；`frontend/.gitignore` 正确忽略 `node_modules/` 和 `dist/`。

终端提示符仍显示 `(.venv)`，只表示上一课的 Python 虚拟环境仍处于激活状态。npm 使用 Node.js 的依赖系统，两者可以同时存在，不代表前端包被安装进 Python 虚拟环境。

最小页面的入口关系是：

```text
index.html 中的 <div id="app"></div>
        ↑ 挂载位置
src/main.js 调用 createApp(App).mount('#app')
        ↑ 导入根组件
src/App.vue 定义实际显示的模板、逻辑和局部样式
```

- `index.html` 是浏览器最先取得的 HTML 外壳，并通过 `<script type="module" src="/src/main.js">` 加载入口脚本。
- `main.js` 导入全局样式和根组件 `App.vue`，创建 Vue 应用，再把它挂载到 `id="app"` 的 HTML 节点。
- `App.vue` 是当前组件树的根组件；其中的 `<template>` 描述页面结构，`<script setup>` 放置组件逻辑，`<style scoped>` 放置只作用于当前组件的样式。

## 9. 检查点 D：用样例学习根组件

根据新的协作约定，AI 先将 `src/App.vue` 整理为一个可运行的最小样例，并使用 `TODO(learner)` 标出可以由学习者模仿修改的位置。样例通过三个 JavaScript 字符串变量保存内容，在模板中用双大括号插值显示，并用局部样式完成居中、间距和颜色设置。

学习者可以把三个变量改为本课目标内容：

```text
标题：NoteMind
说明：基于个人笔记进行检索与问答
状态：前端已启动
```

也可以直接要求 AI 继续，由 AI 补全这些内容并进入运行验收。无论由谁修改，完成后都会删除临时教学注释，并通过开发服务器和生产构建验证实际结果。

学习者按照样例将三个变量改为 `NoteMind`、`基于个人笔记进行检索与问答` 和 `前端已启动`。学习者随后选择“继续”，AI 删除了临时教学注释，并把 `index.html` 的浏览器标签标题从 `Vite App` 改为 `NoteMind`。页面结构、变量插值和局部样式均保持为可复习的最小实现。

## 10. 检查点 E：开发服务器与构建验收

AI 先执行生产构建：

```powershell
cd frontend
npm run build
```

Vite `8.3.2` 成功转换 13 个模块并生成 `dist/`，证明 Vue 单文件组件、模板和样式能够被正常编译。`dist/` 是可重新生成的生产构建产物，已被 `frontend/.gitignore` 忽略。

AI 随后短暂启动开发服务器：

```powershell
npm run dev -- --host 127.0.0.1
```

受限执行环境首次阻止 Vite 创建子进程并返回 `spawn EPERM`；在获准的受限环境外重跑后，Vite 显示 `ready`，本地地址为 `http://127.0.0.1:5173/`，HTTP 检查正常完成，随后服务器已停止。这个错误来自命令执行权限，不是 Vue 代码或依赖错误。

浏览器访问时，`index.html` 只提供 `#app` 挂载点和入口脚本；浏览器执行 JavaScript 后，Vue 才把 `App.vue` 的标题、说明和状态渲染到页面中。因此“服务器返回 HTML”和“Vue 页面完成渲染”是连续但不同的两个步骤。

## 11. 检查点 F：整理、提交与自查

检查发现官方示例的 `main.css` 会在宽屏下把 `#app` 设置为两栏布局，即使 `App.vue` 已经改好，页面仍可能受到残留样式影响。AI 将全局布局简化为单页居中，并删除没有引用的示例组件、图标和 logo；再次执行 `npm run build` 后，Vite 成功转换 13 个模块，CSS 构建产物由约 2.09 kB 减少到 1.82 kB。

提交前检查确认：

- `node_modules/`、`dist/` 和临时日志均被忽略。
- 暂存区只包含 12 个 `frontend/` 项目文件。
- `git diff --cached --check` 没有发现空白错误。

AI 根据学习者的“继续”指令创建功能提交：

```powershell
git add -- frontend
git commit -m "feat: add minimal Vue frontend"
```

实际提交：`f1ab439 feat: add minimal Vue frontend`。

## 12. 复习问题与参考答案

1. **Node.js 和浏览器分别执行什么？**  Node.js 在开发阶段运行 npm、Vite 等工具；浏览器加载构建后的资源并执行页面中的 JavaScript。
2. **`package.json` 和 `package-lock.json` 有什么区别？**  前者声明直接依赖范围和项目脚本，后者记录实际解析出的精确依赖树。
3. **页面如何从 `index.html` 到达 `App.vue`？**  `index.html` 加载 `main.js`；`main.js` 导入根组件并调用 `createApp(App).mount('#app')`；Vue 把组件渲染到挂载节点。
4. **`<template>`、`<script setup>`、`<style scoped>` 各做什么？**  分别描述组件结构、组件逻辑和仅作用于当前组件的样式。
5. **开发服务器和生产构建有什么区别？**  开发服务器面向本地调试并支持快速更新；生产构建把源码转换、压缩为可部署的 `dist/` 文件。

易错点：Python 的 `(.venv)` 提示不会把 npm 依赖安装进 Python 环境；`node_modules/` 和 `dist/` 都可重新生成，不应提交；页面布局异常时不仅要检查 `App.vue`，还要检查全局 CSS。

## 13. 完整教程与课程总结

第 6～11 节依次记录了环境确认、Vue 脚手架、依赖安装、入口关系、根组件实现、开发服务器、生产构建、样式清理和 Git 提交，可作为本课完整复习路径。

- 使用 Vue 官方 `create-vue` 创建了基于 Vite 的 JavaScript 项目。
- 理解了 `index.html → main.js → App.vue` 的最小渲染流程。
- 使用变量插值、模板和局部样式完成了 NoteMind 最小首页。
- 理解了 `package.json`、锁文件、`node_modules/` 和 `dist/` 的不同职责。
- 通过开发服务器和生产构建验证了项目，并区分了执行环境权限错误与代码错误。
- 清理了未使用的官方示例资源和宽屏双栏样式。
- 创建了功能提交 `f1ab439`。

## 14. 验收与定档

学习者已明确确认“本课验收通过”。本课完成了 Vue 项目初始化、依赖安装、入口关系讲解、最小首页实现、开发服务器检查、生产构建、样式整理和 Git 功能提交，课程教程与总结现已定档。

下一课准确会话名称：`NoteMind 第04课：前后端第一次通信`。
