---
name: designer-vibecoding-starter
description: >
  为设计师/产品经理提供从"想法或设计稿"到"代码跑起来、能上线"的完整 vibecoding 全生命周期引导。
  覆盖四个核心环节：
  1) 需求收集（0-1 逐步追问 或 Figma 设计稿分析）
  2) 治理脚手架初始化（AGENTS.md / skills/ / prd-registry.md）
  3) 初始代码库生成（真实可运行的项目代码骨架）
  4) 部署上线引导（Vercel / Railway，5 分钟上线）
  采用单模型多 Agent 架构（Codewiz 主导 + 子 agent 执行）。
  触发词："帮我初始化项目"、"新建 vibecoding 项目"、"从0开始做一个应用"、
         "我有设计稿要开始开发"、"我想上线"、"怎么部署"、"帮我发布"
---

# Designer Vibecoding Starter

> **目标**：让没有代码经验的设计师，从一个想法或一份设计稿出发，
> 走完"需求确认 → 代码跑起来 → 上线给人用"的完整链路。
> Codewiz 负责全程引导，用户只需在关键节点做决策。

---

## 全流程总览

```
用户想法 / Figma 设计稿
         ↓
Phase 0：路径判断（1个问题）
         ↓
Phase 1A（0-1）或 Phase 1B（设计驱动）
  → 逐步追问 / 设计分析 → PRD 草稿 → 用户确认
         ↓
Phase 2A：治理脚手架（AGENTS.md / skills/ / prd-registry.md）
         ↓
Phase 2B：初始代码库生成（真实可运行代码，npm run dev 即可跑）
         ↓
Phase 3：后续开发协作引导（writing-plans → 子 agent → review）
         ↓
Phase 4：部署上线（可随时触发，5 分钟上线）
```

---

## Phase 0：路径判断

问用户**一个问题**：

```
你想用哪种方式开始？

A) 我有 Figma 设计稿（链接或文件）
B) 我还没有设计稿，从产品想法开始描述

（也可以直接粘贴 Figma 链接，我来判断）
```

根据回答跳转：
- A 或收到 Figma 链接 → Phase 1B（设计驱动）
- B → Phase 1A（0-1 路径）

---

## Phase 1A：0-1 路径 — 逐步需求澄清

> **核心原则**：一次只问一个问题，等待回答后再问下一个。绝不一次性列出所有问题。

### Step A-1：产品目标

```
你想构建的是什么？用一句话描述你的产品/应用。
（例如："一个帮助设计师快速整理灵感的工具"、"一个团队任务追踪看板"）
```

等待回答 → 记录 `product_goal`

### Step A-2：目标用户

```
好的，「[产品名]」的主要用户是谁？
他们现在是怎么解决这个问题的？
```

等待回答 → 记录 `target_user` + `current_pain`

### Step A-3：核心价值

```
你的产品比现有方案好在哪里？
最核心的差异点是什么？（一句话就够）
```

等待回答 → 记录 `core_value`

### Step A-4：MVP 功能范围

```
如果只做 3 个核心功能来验证这个想法，你会选哪 3 个？
（3 个是上限，越少越好——少了可以之后加，多了会拖慢进度）
```

等待回答 → 记录 `mvp_features[]`

### Step A-5：技术栈偏好（可选）

```
技术栈有偏好吗？
- 如果有：直接告诉我（如 React + TypeScript、Next.js 等）
- 如果没有：我会根据你的需求推荐合适的栈

（跳过也可以，我来推荐）
```

等待回答 → 记录 `tech_stack`（空则 Codewiz 推荐）

**Codewiz 推荐技术栈规则**：
- 纯前端展示/工具类 → **React + TypeScript + Vite + TailwindCSS**
- 需要路由/多页面 → 加 **React Router**
- 需要状态管理 → 加 **Zustand**（轻量，对设计师友好）
- 需要后端 API/数据库 → **Next.js + Prisma + SQLite/PostgreSQL**

### Step A-6：设计风格定义（仅有前端 UI 时询问）

```
界面风格有倾向吗？可以用以下任何方式告诉我：

A) 发几张你喜欢的网站/应用截图（直接拖入对话框）
B) 发一个你喜欢的网站 URL
C) 用文字描述（如：极简白底、类 Linear、深色系科技感……）
D) 不确定 / 跳过 → 我会给一个简洁的基础样式

推荐选 A 或 B，效果最好——我能从参考图中提取完整的设计语言。
```

等待回答 → 根据回答分流：

**分流 A/B：用户提供了参考图或 URL**
```
触发 style-foundation Skill（skills/style-foundation/SKILL.md）
  → Phase 0 判断模式（Mode A: Image Extract）
  → Phase 1 追问（情感目标、反参考等，逐步追问）
  → Phase 2 Section-First 三层递进提取
  → Phase 3 输出风格宪法 → 写入 docs/style-constitution.md
  → 记录 has_constitution = true
```

**分流 C：用户给了文字描述**
```
判断描述的丰富程度：
  - 丰富（≥2 个维度，如"深色系 + 类 Linear + 极简"）
    → 触发 style-foundation Mode B（文字描述推导）
    → 输出风格宪法 → 写入 docs/style-constitution.md
    → 记录 has_constitution = true
  - 简单（单个关键词，如"极简"）
    → 记录 design_style，不触发 style-foundation
    → 记录 has_constitution = false
```

**分流 D：用户跳过**
```
记录 design_style = ""，has_constitution = false
后续 Phase 2B 使用默认基础样式
```

> **为什么升级**：之前只记录一个 `design_style` 字符串，导致后续生成的设计 Token
> 是硬编码的通用值，与用户的审美意图脱节。通过集成 style-foundation，
> 用户提供参考图后能得到一份完整的「风格宪法」，后续所有 UI 实现都以此为准。

### Step A-7：生成 PRD 草稿 + 用户确认

综合 A-1 到 A-6，输出：

```markdown
## PRD-001：[产品名]

**User Story**
作为 [target_user]，我想要 [product_goal]，以便 [core_value]。

**优先级**：P0

**MVP 功能范围**
- 功能1：作为用户，我可以 [操作]，以便 [目的]
- 功能2：...
- 功能3：...

**不包含（Out of Scope）**
- [根据功能推断 3-5 条明确不做的事]

**技术栈**
- [tech_stack 或推荐栈，注明理由]

**Acceptance Criteria**
- AC-1: 当用户 [功能1操作] 时，[可观察结果]
- AC-2: 当用户 [功能2操作] 时，[可观察结果]
- AC-3: ...（边界/错误场景）
```

输出后询问：

```
这是根据我们讨论生成的 PRD 草稿。

有需要调整的地方吗？
- 没有 → 直接说"确认"，我开始搭建项目
- 要修改 → 告诉我哪里不对
```

用户确认 → 进入 Phase 2A

---

## Phase 1B：设计驱动路径 — Design Analysis 集成

### Step B-1：收集设计信息

已有 Figma 链接 → 跳到 Step B-2

否则询问：
```
请把 Figma 设计稿的链接发给我。
（支持 figma.com/file/... 或 figma.com/design/... 格式）
```

### Step B-2：判断设计稿场景

调用 `mcp__figma__get_figma_data` 拉取顶层结构，判断场景：

**场景 A — 大型设计稿（顶层 Frame ≥2，功能相互独立）**
```
1. 列出识别到的功能模块
2. 问："这个设计稿包含 [N] 个功能：[A/B/C]。
        建议拆分为 [N] 个 PRD，优先实现哪个？"
3. 用户确认 → 对第一个 PRD 做完整 Phase-1 分析
4. 其余 PRD 加入 prd-registry.md 队列（占位）
```

**场景 B — 同时提供产品需求文档 + 设计稿**
```
1. 读产品需求，提取功能清单
2. 拉取设计稿，提取设计侧功能点
3. 对照输出三类结论：
   ✅ 一致项 → 写入 AC
   ⚠️ 设计稿有·需求未提 → 逐一询问用户是否纳入
   ❗ 需求有·设计未覆盖 → 标注设计遗漏风险
4. 确认后生成对齐 PRD
```

**场景 C — 单组件/小模块设计稿**
```
1. 完整执行 Phase-1 分析
2. 查 prd-registry.md，判断归属现有 PRD 还是新建
3. 生成单 PRD
```

### Step B-3：执行 design-analysis Phase-1

按 `skills/design-analysis/SKILL.md` 执行：
```
1. 提取组件层级、状态矩阵、间距、颜色 token、交互行为
2. 识别设计疑点（缺失状态/不一致/无法映射的值）
3. 逐一提问消除疑点（一次一个）
4. 输出设计分析包（状态矩阵 + 间距规格 + 交互行为）
5. 转化为 PRD 设计规格区块 + Acceptance Criteria
```

详细还原规则：见 `agent-context/design-role-rules.md`

### Step B-4：生成 PRD + 用户确认

同 Phase 1A Step A-7 格式，"设计规格"区块已由分析结果填充。

用户确认 → 进入 Phase 2A

---

## Phase 2A：治理脚手架生成

PRD 确认后，**立即**运行 scaffold 脚本，不需要再问用户：

```bash
python3 skills/designer-vibecoding-starter/scripts/init_designer_vibecoding_project.py \
  --target "<target-dir>" \
  --project-name "<project-name>" \
  --path-mode zero-to-one|design-driven
```

生成治理结构（详见 `references/template-map.md`），完成后直接进入 Phase 2B，不停下来等用户。

> **📌 全量 scaffold 规则（v3.2 起）**：
>
> 无论用户选择 0-1 路径还是设计驱动路径，以下文件**必须全量生成**，不受路径条件限制：
> - `agent-context/design-role-rules.md` — Figma→CSS 还原规则库，即使当前无设计稿，后续大概率会补
> - `skills/style-foundation/SKILL.md` — 风格基石 Skill，随时可触发，不依赖启动时有无参考图
>
> **理由**：0-1 路径初期通常无设计稿，但后续迭代中大概率会引入 Figma 设计稿。
> 若 scaffold 阶段漏掉这两个文件，后续补文件成本高且容易遗漏。
> 全量生成成本低（两个文件），收益高（全程备用）。

> **⚠️ 信息归属提醒（生成后向用户说明）**：
>
> 脚手架生成了两类文件，用途完全不同：
> - `AGENTS.md` / `skills/` / `project-management/` → AI 协作配置，只给 AI 工具读
> - `docs/product/` → 产品行为规范，工程师和 AI 都读，随代码库长期演进
>
> **实践规则**：遇到需要沉淀的"产品交互规则"（如菜单行为、颜色规则、操作约束），
> 必须写入 `docs/product/` 对应文件，在 `AGENTS.md` 里只保留指向该文件的引用指针。
> 直接写进 `AGENTS.md` 正文 = 错误归属，后续维护会失控。
>
> 详细原则见 `references/template-map.md` →「信息归属原则」章节。

---

## Phase 2B：初始代码库生成

> **这是核心环节**：Phase 2A 只生成了治理文档，Phase 2B 生成真实可运行的项目代码。
> 完成后用户应该能 `npm install && npm run dev` 直接看到初始 UI。

### Step 2B-1：确认技术栈 + 输出架构方案

根据 PRD 中记录的 `tech_stack`（或 Phase 1A Step A-5 的推荐），输出架构方案：

```
我将使用以下技术栈搭建项目骨架：

技术栈：[React + TypeScript + Vite + TailwindCSS（+ React Router）]
理由：[针对你的需求，这套栈对设计师友好、上手快、部署简单]

项目结构：
<project-name>/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── tailwind.config.ts
└── src/
    ├── main.tsx            ← 应用入口
    ├── App.tsx             ← 路由根组件
    ├── router/
    │   └── index.tsx       ← 路由定义
    ├── pages/
    │   ├── [功能1]/Page.tsx
    │   ├── [功能2]/Page.tsx
    │   └── [功能3]/Page.tsx
    ├── components/         ← 复用组件
    ├── hooks/              ← 自定义 Hook
    ├── stores/             ← 状态管理（Zustand）
    ├── styles/
    │   ├── tokens.css      ← 设计 token（颜色/间距/字体）
    │   └── global.css
    └── types/
        └── index.ts        ← 类型定义

确认这个结构，我立即开始生成？
（也可以告诉我要调整哪里）
```

等待确认（或直接默认 5 秒内无回复视为确认，继续执行）

### Step 2B-2：生成配置文件

依次生成以下文件（使用 write_to_file 工具逐个写入）：

**package.json**
```json
{
  "name": "<project-name>",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.28.0",
    "zustand": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.5.0",
    "vite": "^6.0.0"
  }
}
```

**tsconfig.json / vite.config.ts / tailwind.config.ts**：按标准模板生成（不允许 TBD，必须是完整可用内容）

**index.html**：包含正确的 `<div id="root">` 和 `<script type="module" src="/src/main.tsx">`

### Step 2B-3：生成设计 Token（关键）

根据 Phase 1A/1B 的结果，分三种情况生成设计 Token：

**情况 1：有风格宪法（`has_constitution = true`）**

从 `docs/style-constitution.md` 的「Token 草案（CSS 变量）」章节直接提取，写入 `src/styles/tokens.css`。

```
操作步骤：
1. 读取 docs/style-constitution.md
2. 找到「Token 草案（CSS 变量）」章节
3. 将其中的 CSS 变量直接写入 src/styles/tokens.css
4. 如果宪法中有 Google Fonts 引用，在 index.html 的 <head> 中添加 <link>
5. 如果宪法中有 Section Storyboard 定义了深色/浅色 section，
   确保 tokens.css 包含对应的 surface_light / surface_dark 变量
```

> **铁律**：有 Constitution 时，Token 必须 100% 来自 Constitution，
> 禁止自行编造颜色值或"优化"Constitution 中的值。

**情况 2：无宪法但有 `design_style` 文字描述**

根据 `design_style` 关键词生成基础 token（保持原有逻辑）：
```css
/* src/styles/tokens.css */
:root {
  /* 颜色 — 根据 design_style 关键词选择 */
  --color-primary: #[根据风格选择];
  --color-primary-hover: #[...];
  --color-bg: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-border: #e5e7eb;

  /* 间距 */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-6: 24px;
  --spacing-8: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* 字体 */
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  --font-size-2xl: 32px;
}
```

**情况 3：设计驱动路径**

从 Phase 1B 的设计分析包中提取颜色、间距、圆角值，转化为 CSS custom properties，与设计稿保持一致。

### Step 2B-4：生成入口文件和路由

**src/main.tsx**：标准 React 18 入口

**src/App.tsx**：基于 PRD MVP 功能生成路由结构：
```tsx
// 根据 PRD 的 mvp_features[] 生成对应的路由
// 每个功能点 → 一个 Route + 一个 Page 组件
```

**src/router/index.tsx**：完整路由定义（含 404 兜底）

### Step 2B-5：生成 Page 骨架

根据 PRD 的 `mvp_features[]`，为**每个功能点**生成一个 Page 组件：

```tsx
// src/pages/[FeatureName]/Page.tsx
// 规则：
// 1. 包含功能标题和基本布局
// 2. 有 "// TODO: 实现 [功能描述]" 注释标记
// 3. 有真实的 UI 骨架（不是空白页），能看出功能意图
// 4. 设计驱动路径：按设计分析包中的组件结构生成组件 shell
```

**骨架要求**：不得生成空白页面。每个 Page 至少包含：
- 页面标题
- 功能区域的布局占位（即使内容是假数据）
- 与 PRD AC 对应的 UI 元素位置

### Step 2B-6：生成导航和基础 Layout

**src/components/Layout.tsx**：全局 Layout（包含导航栏，菜单项对应各功能 Page）

**src/components/Navbar.tsx** 或 **Sidebar.tsx**：基于 mvp_features 生成导航项

### Step 2B-7：生成完成确认

所有文件写入完毕后，输出：

```
✅ 项目代码已生成！

目录：[project-path]/
文件数：[N] 个

立即启动：
  cd [project-name]
  npm install
  npm run dev

然后打开 http://localhost:5173 就能看到初始界面。

---

现在可以做：
A) 开始实现第一个功能 → 告诉我"开始做 PRD-001"
B) 先看看代码有没有问题 → 告诉我"检查一下代码"
C) 我想直接上线测试 → 告诉我"帮我部署"（跳转 Phase 4）
```

---

## Phase 3：后续开发协作引导

> 项目代码生成后，用户进入常规开发迭代。本 Phase 说明后续如何用协作链路推进开发。

### 当用户说"开始做 PRD-001"或"实现 [功能]"

触发流程：
```
1. 读 prd-registry.md → 确认 Active PRD
2. 触发 writing-plans Skill → 把 PRD 拆成具体实现 Task（含代码级别的步骤）
3. 逐 Task 派发子 agent 实现
4. 每个 Task 完成后触发 two-stage-review
5. 有设计稿的任务：review 后再过 design-analysis Phase-2（Design QA）
6. 所有 Task 完成 → 更新 prd-registry.md，通知用户
```

### 当用户说"我还想加 [功能]"

触发流程：
```
1. 触发 requirements-refinement Skill → DoR 检查 + AC 补全
2. 生成新 PRD，加入 prd-registry.md 队列
3. 询问优先级（"这个排在当前 PRD 前面还是后面？"）
4. 按序实现
```

### 当用户说"代码有问题" / "这里显示不对"

触发 `skills/systematic-debugging/SKILL.md` 四阶段流程（先找根因，再 fix）。

---

## Phase 4：部署上线

> **独立触发**：可在项目生命周期任意阶段触发，不必等开发完成。
>
> **触发词**：「帮我部署」、「怎么上线」、「我想让别人能访问」、
> 「发布到线上」、「deploy」、「能不能生成一个链接分享给别人」

### Step D-1：判断项目类型（只问一个问题）

```
你的项目有后端服务吗（比如需要登录账号、保存数据到数据库、有 API 接口）？

A) 没有，就是一个页面/工具（纯前端）
B) 有，需要后端 API 或数据库

（不确定的话选 A，大部分初期项目都是纯前端）
```

根据回答跳转：
- A → Step D-2A（Vercel，推荐）
- B → Step D-2B（Railway，推荐）

---

### Step D-2A：纯前端 → Vercel 部署

> **为什么推荐 Vercel**：免费、自动 HTTPS、全球 CDN、和 GitHub 深度集成、支持 React/Next.js/Vue 等所有主流框架，5 分钟上线。

#### 前置：确认代码是否在 GitHub

```
你的代码有没有推送到 GitHub？

A) 有 → 直接进入 Vercel 导入步骤
B) 没有 → 我来帮你一步步推上去
```

**如果没有 GitHub**，按以下步骤引导：

```
步骤 1：注册 GitHub（如果还没有）
  → 打开 https://github.com，点右上角 Sign Up，用邮箱注册

步骤 2：创建新仓库
  → 登录后点右上角 "+" → "New repository"
  → Repository name：[project-name]
  → 选择 Public（免费托管）→ 点 "Create repository"

步骤 3：在项目目录运行以下命令
  （我可以帮你逐条确认每步是否成功）

  git init
  git add .
  git commit -m "feat: initial project scaffold"
  git branch -M main
  git remote add origin https://github.com/[你的用户名]/[project-name].git
  git push -u origin main

  ✅ 推送成功后，GitHub 页面刷新能看到文件
```

#### Vercel 部署步骤

```
步骤 1：打开 https://vercel.com，点右上角 "Sign Up"
        → 选择 "Continue with GitHub"，用刚才的 GitHub 账号登录
        （Vercel 会申请授权，点 Authorize 即可）

步骤 2：点 "Add New..." → "Project"
        → 找到你的 [project-name] 仓库，点 "Import"

步骤 3：检查构建配置（通常不需要改）
        Framework Preset：Vercel 会自动检测（Vite / Next.js 等）
        Build Command：自动填好（npm run build）
        Output Directory：自动填好（dist）

        如果是 Vite 项目没有自动识别：
        Framework Preset → 选 "Vite"
        Build Command → npm run build
        Output Directory → dist

步骤 4：点 "Deploy"
        → 等待约 1-3 分钟
        → 看到 "Congratulations!" 页面 ✅

步骤 5：点 "Visit" 打开你的线上地址
        格式：https://[project-name]-xxx.vercel.app

🎉 完成！把这个链接发给任何人都能访问。
```

#### 后续更新代码如何重新部署

```
每次本地改完代码，只需：

git add .
git commit -m "改动描述"
git push

Vercel 检测到 push 后自动重新部署，约 1 分钟更新完成。
不需要再手动操作。
```

#### 如果需要自定义域名

```
在 Vercel 项目页面 → Settings → Domains → Add Domain
输入你的域名 → 按提示在域名服务商添加 DNS 记录
通常 5-30 分钟生效，Vercel 自动配置 HTTPS。
```

---

### Step D-2B：有后端/数据库 → Railway 部署

> **为什么推荐 Railway**：免费额度 $5/月（足够个人项目用）、支持 Node.js/Python/数据库、一键部署、环境变量管理友好。

#### 前置：同样先确认代码在 GitHub（步骤同上）

#### Railway 部署步骤

```
步骤 1：打开 https://railway.app，点 "Start a New Project"
        → 选择 "Sign in with GitHub"，授权登录

步骤 2：点 "New Project" → "Deploy from GitHub repo"
        → 找到你的仓库，点 "Deploy Now"

步骤 3：配置环境变量（重要）
        点项目卡片 → "Variables" 标签
        把 .env 文件里的变量一条一条加进去
        （如 DATABASE_URL、API_KEY 等）
        ⚠️ 绝对不要把 .env 文件提交到 GitHub

步骤 4：确认构建配置
        如果是 Next.js：Start Command → npm start
        如果是 Node.js API：Start Command → node src/index.js
        （Railway 通常会自动检测）

步骤 5：点 "Deploy" → 等待 2-5 分钟
        成功后在 Settings → Networking → Generate Domain
        获得公开访问地址

🎉 完成！
```

#### 如果需要数据库

```
在 Railway 项目中：
→ "New" → "Database" → 选择 PostgreSQL 或 MySQL
→ 创建后在 Variables 里会自动生成 DATABASE_URL
→ 在你的应用 Variables 里添加同样的 DATABASE_URL

数据库和应用同在 Railway，内网直连，速度快、免费额度充足。
```

---

### Step D-3：部署后验证清单

```
部署完成后，一起检查：

[ ] 页面能正常打开？
[ ] 核心功能能用（对照 PRD AC 逐条验证）？
[ ] 移动端显示正常（手机打开链接看一下）？
[ ] 有报错信息吗（打开浏览器 DevTools → Console 看看）？

如果有问题，告诉我报错信息，我来帮你排查。
```

---

## 关键规则汇总

### 问题节奏规则（适用所有 Phase）

```
✅ 每次只问一个问题
✅ 等待用户回答后再问下一个
✅ 可选问题用户跳过后，给出合理默认值并说明
❌ 禁止一次性抛出问题列表
❌ 禁止在用户未确认时自动进入下一 Phase
```

### 代码生成规则（Phase 2B）

```
✅ 每个文件必须是完整可用的内容（可直接运行）
✅ Page 组件必须有真实 UI 骨架，能看出功能意图
✅ 设计 token 必须来源于设计稿或 design_style，不得硬编码随机颜色
❌ 禁止生成空白页面或纯注释文件
❌ 禁止在任何文件中写 "TODO: implement this"（除了功能实现占位注释）
```

### 部署引导规则（Phase 4）

```
✅ 推荐平台时说明推荐理由
✅ 每个步骤配上精确的 URL 和界面操作描述
✅ 每次询问用户"这步完成了吗？"再继续下一步
✅ 遇到报错，立即询问报错信息并分析
❌ 禁止假设用户知道 git 操作，必须提供完整命令
❌ 禁止一次性给出所有步骤让用户自己操作
```

---

## Skill 联动关系

| 时机 | 触发的 Skill |
|------|-------------|
| 0-1 路径用户提供参考图/URL/丰富风格描述 | `style-foundation`（生成风格宪法） |
| 用户输入 Figma 链接 | `design-analysis` Phase-1 |
| PRD 确认后实现功能 | `writing-plans` → 子 agent |
| 每个 Task 完成后 | `two-stage-review` |
| UI 任务完成后 | `design-analysis` Phase-2（Design QA） |
| 需求不清晰 | `requirements-refinement` |
| 代码有 bug | `systematic-debugging` |
| 架构变更前 | `architecture-check` |

### Constitution 强制读取规则

当项目中存在 `docs/style-constitution.md` 时，以下环节**必须先读取 Constitution**：

| 环节 | 读取内容 | 用途 |
|------|---------|------|
| Phase 2B-3 生成设计 Token | Token 草案章节 | 直接提取 CSS 变量 |
| Phase 2B-5 生成 Page 骨架 | Section Storyboard 章节 | 指导页面布局和视觉节奏 |
| Phase 3 实现功能（调用 frontend-design） | 完整 Constitution | 作为 frontend-design 的风格约束输入 |
| Phase 3 Design QA | 设计原则 DO/DON'T | 验证实现是否符合风格宪法 |

**铁律**：有 Constitution 的项目，任何 UI 实现步骤都不得忽略 Constitution。
如果 frontend-design skill 被触发，必须在 prompt 中包含 Constitution 的核心内容
（至少包含：Style DNA 一句话 + Section Storyboard 亮点 + Token 草案 + DO/DON'T）。

---

## Resources

- [`references/template-map.md`](references/template-map.md)：问题清单 + 路径分支行为 + Scaffold 文件列表
- [`scripts/init_designer_vibecoding_project.py`](scripts/init_designer_vibecoding_project.py)：Phase 2A 治理脚手架脚本
- [`skills/design-analysis/SKILL.md`](../design-analysis/SKILL.md)：设计分析完整流程
- [`skills/style-foundation/SKILL.md`](../style-foundation/SKILL.md)：风格基石（参考图→风格宪法）
- [`agent-context/design-role-rules.md`](../../agent-context/design-role-rules.md)：Figma→CSS 还原规则库

---

_版本：v4.1（2026-04-01）_
_变更：Phase 1A Step A-6 集成 style-foundation（参考图→风格宪法）+ Phase 2B-3 Constitution 驱动 Token 生成 + Constitution 强制读取规则_
_覆盖：需求收集 → 风格定义 → 代码生成 → 开发迭代 → 上线部署，设计师全生命周期_
