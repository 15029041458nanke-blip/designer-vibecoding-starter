#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def make_agents_md(project_name: str) -> str:
    return f"""# AGENTS.md

## Purpose
- Keep this project usable, collaborative, and easy to hand off.
- Use the workflow files as the source of truth instead of chat memory.

## Working Rules
- Start small, verify fast, expand later.
- Do not change scope silently.
- Write plans for tasks with 3+ steps or any architecture decision.
- Do not mark work done without runnable evidence.

## Must-Read Order
1. `AGENTS.md`
2. `agent-context/current-workflow.md`
3. `project-management/active-sprint.md`

## Project
- Name: `{project_name}`
- This repo was initialized from `designer-vibecoding-starter`.
"""


def make_current_workflow(workflow_id: str) -> str:
    owner = "claude+codex" if workflow_id == "claude-planner-codex-builder" else "codex"
    return f"""# Current Workflow

workflow_id: {workflow_id}
updated_at: {today()}
owner: {owner}

## Start Here
1. `/AGENTS.md`
2. `/agent-context/current-workflow.md`
3. `/agent-context/default-context.md`
4. `/project-management/active-sprint.md`
5. `/project-management/backlog.md`

## Rule
- Only one workflow is active at a time.
- If switching workflow, update this file first.
"""


def make_default_context(path_mode: str, openclaw_enabled: bool) -> str:
    path_line = (
        "Design-driven path: design analysis -> PRD -> product check -> build -> test -> design QA"
        if path_mode == "design-driven"
        else "Zero-to-one path: intent -> planning -> PRD -> spec/todo -> build -> test -> review"
    )
    remote_line = (
        "OpenClaw is enabled for optional background execution."
        if openclaw_enabled
        else "OpenClaw is not enabled in this project by default."
    )
    return f"""# Default Context

## Delivery Path
- {path_line}

## Collaboration Modes
- `claude-planner-codex-builder`
- `codex-fullstack-workflow`
- {remote_line}

## Shared Inputs
- `.agent/handoff.json` is the single task handoff source.
- `.agent/status.json` is the single execution status source.
- `scripts/agent_run.sh` is the single execution entry.
"""


def make_workflow_selector() -> str:
    return """# Workflow Selector

## Available modes

1. `Claude Code + Codex`
2. `Codex fullstack`
3. `OpenClaw` background execution (optional overlay)

## Example Chinese intents

- `切换到 Claude 规划 + Codex 开发`
- `跟我用 Codex 协作链路`
- `开启 OpenClaw 后台执行`
"""


def make_collab_overview(path_mode: str, openclaw_enabled: bool) -> str:
    path_label = "基于设计稿" if path_mode == "design-driven" else "0-1 无设计稿"
    openclaw_line = "Enabled" if openclaw_enabled else "Disabled"
    return f"""# Collaboration Workflows Overview

## Current delivery path
- {path_label}

## Modes
- `claude-planner-codex-builder`
- `codex-fullstack-workflow`
- `OpenClaw`: {openclaw_line}

## Single sources of truth
- `agent-context/current-workflow.md`
- `.agent/handoff.json`
- `.agent/status.json`
- `scripts/agent_run.sh`
"""


def make_workflow_doc(name: str, summary: str) -> str:
    return f"""# {name}

## Summary
- {summary}

## Steps
1. Clarify the task
2. Write or refine the spec/todo
3. Fill `.agent/handoff.json`
4. Execute with `scripts/agent_run.sh`
5. Verify and record results
"""


def make_agent_roles() -> str:
    return """# Agent Roles

- `project-manager`: clarify scope and track status
- `architect`: define implementation structure
- `engineer`: implement the change
- `tester`: run validation
- `reviewer`: check risk and regressions
- `design-analyst`: translate design into implementation constraints
"""


def make_figma_mcp_setup() -> str:
    return (
        "# Figma MCP 接入指南\n\n"
        "> **定位**：design-driven 路径下，Figma MCP 是设计稿分析与图标下载的核心工具。\n"
        "> 完成以下配置后，Claude 可以直接读取 Figma 文件结构、下载 SVG 图标到本地。\n\n"
        "---\n\n"
        "## 步骤 1：获取 Figma Personal Access Token\n\n"
        "1. 打开 Figma → 右上角头像 → **Settings**\n"
        "2. 进入 **Security** 标签页\n"
        "3. 点击 **Generate new token**（Personal access tokens）\n"
        "4. 填写名称（如 `claude-mcp`），权限选 **Read-only**（File content）\n"
        "5. 复制 Token（只显示一次，请保存好）\n\n"
        "---\n\n"
        "## 步骤 2：配置 Claude Code MCP（.mcp.json）\n\n"
        "在项目根目录创建 `.mcp.json`：\n\n"
        "```json\n"
        "{\n"
        '  "mcpServers": {\n'
        '    "figma": {\n'
        '      "command": "npx",\n'
        '      "args": ["-y", "figma-developer-mcp", "--stdio"],\n'
        '      "env": {\n'
        '        "FIGMA_API_KEY": "YOUR_FIGMA_TOKEN_HERE"\n'
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n"
        "```\n\n"
        "替换 `YOUR_FIGMA_TOKEN_HERE` 为步骤 1 中的 Token。\n\n"
        "---\n\n"
        "## 步骤 3：安装 vite-plugin-svgr（SVG → React 组件）\n\n"
        "```bash\n"
        "npm install --save-dev vite-plugin-svgr\n"
        "```\n\n"
        "**vite.config.ts**：\n\n"
        "```ts\n"
        "import svgr from 'vite-plugin-svgr'\n"
        "export default defineConfig({\n"
        "  plugins: [svgr(), react()],\n"
        "})\n"
        "```\n\n"
        "**src/vite-env.d.ts**：\n\n"
        "```ts\n"
        "/// <reference types=\"vite/client\" />\n"
        "/// <reference types=\"vite-plugin-svgr/client\" />\n"
        "```\n\n"
        "---\n\n"
        "## 步骤 4：使用 download_figma_images 下载图标\n\n"
        "在 Claude 对话中说：\n\n"
        "> 使用 download_figma_images 下载 Figma 节点 [nodeId] 为 SVG，保存到 src/components/icons/[name].svg\n\n"
        "**注意事项**：\n"
        "- `nodeId` 必须是顶层可导出节点（Frame / Component 顶层，非内部子节点）\n"
        "- 从 Figma URL 获取：`node-id=5023-57260` → nodeId = `5023:57260`\n"
        "- `fileKey` 从 Figma URL 获取：`figma.com/design/[fileKey]/...`\n\n"
        "---\n\n"
        "## 步骤 5：在 React 中使用下载的 SVG\n\n"
        "```tsx\n"
        "import FillColorIcon from '@/components/icons/fill-color.svg?react'\n"
        "<FillColorIcon width={20} height={20} aria-label=\"填充色\" />\n"
        "```\n\n"
        "---\n\n"
        "## 完整图标还原流程\n\n"
        "```\n"
        "get_figma_data → 找到图标节点 nodeId（type=IMAGE-SVG）\n"
        "     ↓\n"
        "download_figma_images → src/components/icons/[name].svg\n"
        "     ↓\n"
        "import Icon from '@/components/icons/[name].svg?react'\n"
        "     ↓\n"
        "替换 <IconPlaceholder /> → <Icon width={20} height={20} />\n"
        "```\n\n"
        "---\n\n"
        "## 常见问题\n\n"
        "| 问题 | 原因 | 解决 |\n"
        "|------|------|------|\n"
        "| 404 Not Found | nodeId 是 Component 内部子节点 | 在 Figma 里选顶层 Frame/Component，从 URL 获取 node-id |\n"
        "| 无权限 | Token 权限不足 | 重新生成 Token，勾选 File content Read |\n"
        "| SVG 无 currentColor | Figma 导出时颜色被硬编码 | 手动将 fill 值替换为 `currentColor` |\n"
    )


def make_design_role_rules(creation_date: str) -> str:
    return (
        "# Design Role Rules — 设计还原规则手册\n\n"
        "> **定位**：设计角色（design-analyst / engineer 还原阶段 / reviewer 走查阶段）的强制遵守规则集。\n"
        "> **目标**：第一稿还原率 > 80%，逐版本迭代提升。\n"
        "> **更新机制**：每次发现新的典型还原问题，立即在对应章节追加案例。\n\n"
        "---\n\n"
        "## §1 图标（Icon）还原规则\n\n"
        "### 优先方案：download_figma_images 直接下载\n\n"
        "通过 `download_figma_images` MCP 工具下载真实 SVG，配合 `vite-plugin-svgr` 转为 React 组件。\n"
        "详见 `docs/design/figma-mcp-setup.md` 完整接入指南。\n\n"
        "```tsx\n"
        "import FillColorIcon from '@/components/icons/fill-color.svg?react'\n"
        "<FillColorIcon width={20} height={20} />\n"
        "```\n\n"
        "### 兜底方案：IconPlaceholder 临时占位\n\n"
        "当图标无法下载时（nodeId 不可导出 / Token 未配置），用 `IconPlaceholder` 临时占位，**禁止**：\n"
        "- 用文字替代图标\n"
        "- 自行绘制语义化图标\n\n"
        "IconPlaceholder 规格（项目启动时确认）：容器尺寸 / 内圆直径 / 描边粗细\n\n"
        "### §1 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §2 Border 还原规则\n\n"
        "- 默认策略：内 border → `width/height` 显式固定 + `box-sizing: border-box`\n"
        "- 含 `fill` 子元素的结构性容器：用 `outline` 不用 `border`（Figma Inside stroke 不压缩 fill 子内容，CSS border-box 会压缩）\n"
        "- 验证：浏览器渲染尺寸 == Figma 标注尺寸 ✅\n\n"
        "### §2 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §3 尺寸还原规则\n\n"
        "- sizing 类型（hug/fixed/fill）必须从 Component Set 直接读取，禁止从使用侧推断\n"
        "- 从小到大逐层验证：icon → button → row → panel → modal\n\n"
        "### §3 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §4 节点内容类型识别规则\n\n"
        "实现前必须查 Figma 节点 `type`：\n\n"
        "| Figma type | 对应实现 |\n"
        "|-----------|----------|\n"
        "| `TEXT` | 文字 children |\n"
        "| `IMAGE-SVG` / `VECTOR` / `BOOLEAN_OPERATION` | `IconPlaceholder`，禁止用文字 |\n"
        "| `FRAME` / `INSTANCE` | React 组件或 div |\n"
        "| `RECTANGLE` / `ELLIPSE` | CSS 形状或 SVG 基本图形 |\n\n"
        "### §4 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §5 布局对齐规则\n\n"
        "**Figma MCP 对齐数据返回机制**：\n\n"
        "| 元素类型 | MCP 返回 | 处理方式 |\n"
        "|---------|---------|----------|\n"
        "| Auto Layout 子元素 | `alignItems` / `justifyContent` / `alignSelf` | 直接映射 CSS flex 属性 |\n"
        "| 绝对定位元素 | 只有 `locationRelativeToParent: {x, y}` | 手动判断居中意图 |\n\n"
        "居中意图判断：若 `x == (父宽-子宽)/2` 且 `y == (父高-子高)/2` → 用 `inset: 0 + flex`，禁止字面翻译坐标为 top/left。\n\n"
        "排列数量验证：`N × 元素宽 + (N-1) × gap ≤ 容器可用宽度`\n\n"
        "### §5 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §6 组件系统规则\n\n"
        "- 变体必须从 Component Set 顶层节点枚举，禁止从使用侧实例读取\n"
        "- 正确路径：`componentSetId` → Component Set children → 完整变体列表\n\n"
        "### §6 典型案例\n\n> （在此处追加每次发现的案例）\n\n"
        "---\n\n"
        "## §7 设计走查清单（QA Checklist）\n\n"
        "- [ ] 所有图标已用 IconPlaceholder，无文字替代\n"
        "- [ ] 每个组件 width / height 与 Figma 标注值相差 ≤ 0.5px\n"
        "- [ ] 含 fill 子元素的容器边框：用 `outline` 而非 `border`\n"
        "- [ ] 每行/列元素数量与设计稿完全一致\n"
        "- [ ] 绝对定位居中元素：已判断居中意图，用 `inset:0 + flex`\n"
        "- [ ] 所有 Component Set 变体均已实现\n\n"
        "---\n\n"
        "## §CHANGELOG\n\n"
        "| 日期 | 版本 | 内容 | 触发问题 |\n"
        "|------|------|------|----------|\n"
        f"| {creation_date} | v0.1 | 初始框架生成，by designer-vibecoding-starter | 项目初始化 |\n"
    )


def make_design_file(title: str, active: bool, body: str) -> str:
    status = "active" if active else "optional"
    return f"""# {title}

status: {status}

{body}
"""


def make_design_role_rules() -> str:
    return f"""# Design Role Rules — 设计还原规则手册

> **定位**：设计角色（design-analyst / engineer 还原阶段 / reviewer 走查阶段）的强制遵守规则集。
> **目标**：第一稿还原率 > 80%，逐版本迭代提升。
> **更新机制**：每次发现新的典型还原问题，立即在对应章节追加案例，注明发现时间和修复方案。
>
> 版本历史见文末 §CHANGELOG。

---

## 使用说明

本文件适用于设计驱动链路的三个环节：

| 环节 | 读取重点 |
|------|---------|
| **设计分析**（design-analyst 提取 SPEC） | §1 图标 / §3 尺寸 / §4 节点内容类型 / §5 布局 / §6 组件系统 |
| **代码转化**（engineer 实现） | §2 border / §3 尺寸 / §4 节点内容类型 / §5 布局排列数量 |
| **设计走查**（design-analyst QA / reviewer） | §3 尺寸验证 / §5 排列数量验证 / §7 走查清单 |

**规则优先级**：本文件 > SPEC 文档 > 实现惯例。若本文件与 SPEC 冲突，以本文件为准并更新 SPEC。

---

## §1 图标（Icon）还原规则

### 1.1 核心规则

Figma 中 `IMAGE-SVG` 类型的节点（图标）**无法通过 MCP 直接导出 SVG 路径数据**。

所有无法导出的图标，统一使用 `IconPlaceholder` 组件占位，**禁止**：
- 用文字替代图标
- 自行绘制语义化图标（自造箭头、形状等）
- 留空不处理

### 1.2 IconPlaceholder 规格（项目启动时确认，不得随意修改）

```
容器：[填入尺寸]px
内圆：直径 [填入]px，描边粗细 [填入]px
颜色：rgba(0, 0, 0, 0.15) stroke，无填充
```

### 1.3 典型错误案例

> （在此处追加每次发现的案例）

---

## §2 Border 还原规则

### 2.1 Figma stroke → CSS border 映射

**默认策略：内 border**（border 向内画，不撑大容器）

```css
element {{
  width: [Figma标注值]px;
  height: [Figma标注值]px;
  box-sizing: border-box;
  border: Npx solid {{color}};
}}
```

### 2.2 验证方法

浏览器 DevTools 测量渲染尺寸 vs Figma 标注尺寸：
- ✅ **相同** → border 方向正确
- ❌ **相差 N×2** → border 向外画了

### 2.3 特殊场景：fill 子元素容器的结构性 border

当容器含 `sizing: fill` 的子元素 + Inside stroke 时，**必须用 `outline`**，不能用 `border + border-box`。

```css
.container {{
  outline: 0.5px solid rgba(0, 0, 0, 0.08); /* 不影响盒模型 */
  border: none;
}}
```

### 2.4 典型错误案例

> （在此处追加每次发现的案例）

---

## §3 尺寸还原规则

### 3.1 核心原则

还原后从小到大逐层验证：`icon → button → row → panel → modal`

### 3.2 关键尺寸来源

从 Figma MCP `globalVars.styles` 中的 layout token 读取：
- `dimensions.width / height` → fixed 尺寸
- `padding` → 内边距
- `gap` → 子元素间距
- `borderRadius` → 圆角

### 3.3 重要原则

**sizing 类型必须从组件自身 Component Set 直接读取，禁止从使用侧实例推断。**

### 3.4 典型错误案例

> （在此处追加每次发现的案例）

---

## §4 节点内容类型识别规则

### 4.1 实现前必须查 Figma 节点 type

| Figma type | 对应实现 |
|-----------|---------|
| `TEXT` | 文字 children |
| `IMAGE-SVG` / `VECTOR` / `BOOLEAN_OPERATION` | `<IconPlaceholder />`，**禁止用文字替代** |
| `FRAME` / `INSTANCE` | React 组件或 div |
| `RECTANGLE` / `ELLIPSE` | CSS 形状或 SVG 基本图形 |

### 4.2 典型错误案例

> （在此处追加每次发现的案例）

---

## §5 布局还原规则

### 5.1 容器 sizing 分类

| Figma sizing | CSS 实现 |
|-------------|---------|
| **hug** | `width: fit-content` |
| **fixed** | `width: Npx; height: Npx` |
| **fill** | `flex: 1` |

### 5.2 排列数量严格对齐

设计稿中横向/纵向排列了 N 个元素，实现必须也是 N 个。

验证公式：`N × 元素宽 + (N-1) × gap ≤ 容器可用宽度`

### 5.3 元素对齐规则

**Figma MCP 对齐数据返回机制**：

| 元素类型 | MCP 返回字段 | 处理方式 |
|---------|------------|---------|
| Auto Layout 子元素 | `alignItems` / `justifyContent` / `alignSelf` | 直接映射 CSS flex 属性 |
| 绝对定位元素 | 只有 `locationRelativeToParent: {{x, y}}` | 手动判断：x/y == (父-子)/2 → 居中意图；否则 → 真实偏移 |

**居中意图判断**：若 `x == (父宽-子宽)/2` 且 `y == (父高-子高)/2`：

```css
/* 居中意图 → 禁止字面翻译坐标 */
.element {{
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}}
```

### 5.4 典型错误案例

> （在此处追加每次发现的案例）

---

## §6 组件与设计系统规则

### 6.1 组件识别与下钻

1. Figma Component Set → React 独立组件
2. Component Set 所有变体 → `variant` prop（**不得遗漏**）
3. **必须直接查 Component Set 顶层节点**，禁止从使用侧实例读取变体

```
正确路径：Figma MCP → Component Set（componentSetId）→ children → 完整变体
错误路径：Figma MCP → 使用侧 Frame → 嵌套 Instance → 只看到部分变体
```

### 6.2 典型错误案例

> （在此处追加每次发现的案例）

---

## §7 设计走查清单（Design QA Checklist）

每次实现后，按以下顺序逐项检查：

### 7.1 元素层面
- [ ] 所有图标已使用 IconPlaceholder（无法导出时），无文字替代
- [ ] 所有 TEXT 节点内容与设计稿文案完全一致

### 7.2 尺寸层面
- [ ] 每个组件的 width / height 与 Figma 标注值相差不超过 0.5px
- [ ] 所有 padding / gap 值与 Figma layout token 一致
- [ ] border-radius 一致

### 7.3 Border 层面
- [ ] 有 Inside stroke 的组件：浏览器渲染尺寸 == Figma 标注尺寸
- [ ] 含 fill 子元素的结构性 border：使用 `outline` 而非 `border`

### 7.4 布局层面
- [ ] 每行/列的元素数量与设计稿完全一致
- [ ] 所有 sizing 类型（hug/fixed/fill）已正确对应 CSS 实现
- [ ] **绝对定位居中元素**：已判断居中意图，使用 `inset:0 + flex` 而非 `top/left` 坐标

### 7.5 组件层面
- [ ] 所有 Component Set 变体均已实现（通过 componentSetId 逐一核对）
- [ ] 嵌套组件已下钻到子 Component Set 独立核实

---

## §CHANGELOG

| 日期 | 版本 | 新增/修改内容 | 触发问题 |
|------|------|------------|---------|
| {today()} | v0.1 | 初始框架生成，by designer-vibecoding-starter | 项目初始化 |

---

> **如何更新本文件**
>
> 1. 发现新的典型问题 → 在对应 §CHANGELOG 追加一行
> 2. 若问题属于已有规则的新案例 → 在对应章节末尾追加「典型错误案例」
> 3. 若问题属于全新规则类别 → 新建 §N 章节，并在 CHANGELOG 记录
> 4. 每条案例必须包含：错误描述 / 根因 / 修复方案 / 新增/强化的规则引用
"""


def make_active_prd(project_name: str, path_mode: str) -> str:
    flow = (
        "Design analysis -> design contract -> PRD slices -> implementation -> design QA"
        if path_mode == "design-driven"
        else "Intent clarification -> PRD -> implementation slices -> validation"
    )
    return f"""# Active PRD

## Project
- {project_name}

## Path
- {path_mode}

## Delivery flow
- {flow}

## Current objective
- Replace this section with the first real deliverable.
"""


def make_active_sprint(project_name: str) -> str:
    return f"""# Active Sprint

- Project: {project_name}
- Status: in-progress

## Goal
- Initialize the collaboration system
- Define the first deliverable
- Produce the first executable handoff

## Checklist
- [ ] Confirm scope
- [ ] Fill active PRD
- [ ] Fill tasks/todo.md
- [ ] Create first handoff
- [ ] Run verification
"""


def make_backlog() -> str:
    return """# Backlog

## Now
- [ ] Define the first milestone

## Next
- [ ] Expand PRD slices
- [ ] Add verification cases

## Later
- [ ] Add automation improvements
"""


def make_changelog() -> str:
    return f"""# Changelog

## {today()}
- Project scaffold initialized from `designer-vibecoding-starter`.
"""


def make_todo(path_mode: str) -> str:
    extra = (
        "- [ ] Complete design analysis\n- [ ] Complete design QA"
        if path_mode == "design-driven"
        else "- [ ] Clarify initial product intent\n- [ ] Draft first PRD slice"
    )
    return f"""# Todo

## Current Plan
- [ ] Confirm first milestone
{extra}
- [ ] Create handoff
- [ ] Run verification

## Review
- Pending
"""


def make_lessons() -> str:
    return """# Lessons

- Add repeated corrections and workflow learnings here.
- Review relevant items before starting major work.
"""


def make_handoff() -> str:
    return json.dumps(
        {
            "task_id": "init-first-task",
            "title": "Replace with your first real task",
            "steps": [],
            "test_commands": [],
        },
        ensure_ascii=False,
        indent=2,
    )


def make_status() -> str:
    return json.dumps(
        {"status": "idle", "task_id": "", "updated_at": now_iso()},
        ensure_ascii=False,
        indent=2,
    )


def make_package_json(openclaw_enabled: bool) -> str:
    scripts = {
        "workflow:intent": "bash ./scripts/workflow_intent.sh",
        "validate:handoff": "bash ./scripts/validate_handoff.sh",
        "agent:run": "bash ./scripts/agent_run.sh",
    }
    if openclaw_enabled:
        scripts["openclaw:worker"] = "bash ./scripts/openclaw_worker.sh"
        scripts["openclaw:daemon"] = "bash ./scripts/openclaw_daemon.sh"
    return json.dumps(
        {"name": "designer-vibecoding-template", "private": True, "scripts": scripts},
        ensure_ascii=False,
        indent=2,
    )


WORKFLOW_INTENT_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

INTENT="${*:-}"
if [[ -z "$INTENT" ]]; then
  echo "Usage: bash ./scripts/workflow_intent.sh \\"中文意图\\""
  echo "例如："
  echo "  bash ./scripts/workflow_intent.sh \\"切换到 Claude 规划 + Codex 开发\\""
  echo "  bash ./scripts/workflow_intent.sh \\"跟我用 Codex 协作链路\\""
  echo "  bash ./scripts/workflow_intent.sh \\"开启 OpenClaw 后台执行\\""
  exit 1
fi

CURRENT_WORKFLOW="$(sed -n 's/^workflow_id: //p' agent-context/current-workflow.md | head -n 1)"
TARGET_WORKFLOW="$CURRENT_WORKFLOW"
OPENCLAW_ACTION="no-change"
PATH_MODE="no-change"
TARGET_OWNER="$(sed -n 's/^owner: //p' agent-context/current-workflow.md | head -n 1)"
TODAY="$(date +%F)"

# 协作模式识别
if [[ "$INTENT" == *"Claude"* ]] || [[ "$INTENT" == *"Claude 规划"* ]] || [[ "$INTENT" == *"旧协作"* ]]; then
  TARGET_WORKFLOW="claude-planner-codex-builder"
elif [[ "$INTENT" == *"Codex"* ]] || [[ "$INTENT" == *"多 agent"* ]] || [[ "$INTENT" == *"多agent"* ]] || [[ "$INTENT" == *"全流程"* ]]; then
  TARGET_WORKFLOW="codex-fullstack-workflow"
fi

if [[ "$TARGET_WORKFLOW" == "claude-planner-codex-builder" ]]; then
  TARGET_OWNER="claude+codex"
else
  TARGET_OWNER="codex"
fi

# OpenClaw 识别
if [[ "$INTENT" == *"OpenClaw"* ]] || [[ "$INTENT" == *"后台"* ]] || [[ "$INTENT" == *"远程"* ]]; then
  OPENCLAW_ACTION="enable"
fi

# 路径识别
if [[ "$INTENT" == *"有设计稿"* ]] || [[ "$INTENT" == *"设计驱动"* ]] || [[ "$INTENT" == *"design-driven"* ]]; then
  PATH_MODE="design-driven"
elif [[ "$INTENT" == *"没有设计稿"* ]] || [[ "$INTENT" == *"从零开始"* ]] || [[ "$INTENT" == *"zero-to-one"* ]]; then
  PATH_MODE="zero-to-one"
fi

# 如果 workflow 有变化，更新 current-workflow.md
if [[ "$TARGET_WORKFLOW" != "$CURRENT_WORKFLOW" ]]; then
  sed -i.bak "s/^workflow_id: .*/workflow_id: $TARGET_WORKFLOW/" agent-context/current-workflow.md
  sed -i.bak "s/^owner: .*/owner: $TARGET_OWNER/" agent-context/current-workflow.md
  sed -i.bak "s/^updated_at: .*/updated_at: $TODAY/" agent-context/current-workflow.md
  rm -f agent-context/current-workflow.md.bak
  echo "[workflow_intent] switched: $CURRENT_WORKFLOW -> $TARGET_WORKFLOW"
fi

cat <<EOF
{
  "intent": "$INTENT",
  "workflow": "$TARGET_WORKFLOW",
  "workflow_changed": $([ "$TARGET_WORKFLOW" != "$CURRENT_WORKFLOW" ] && echo "true" || echo "false"),
  "openclaw_action": "$OPENCLAW_ACTION",
  "path_mode": "$PATH_MODE"
}
EOF
"""


VALIDATE_HANDOFF_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FILE="${1:-.agent/handoff.json}"
jq -e '.task_id and .title' "$FILE" >/dev/null
echo "handoff ok"
"""


AGENT_RUN_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

TASK_ID="$(jq -r '.task_id // "unknown"' .agent/handoff.json)"
echo "{\\"status\\":\\"running\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json

# -------------------------------------------------------
# 配置执行命令
# 将下面的 CONFIGURED=false 改为 CONFIGURED=true，
# 并在 run_task() 中填写实际执行命令，例如：
#   codex run --task "$TASK_ID"
#   claude --task "$TASK_ID"
# -------------------------------------------------------
CONFIGURED=false

run_task() {
  # TODO: 替换为实际执行命令
  echo "[agent_run] no command configured"
  return 1
}

if [[ "$CONFIGURED" == "true" ]]; then
  if run_task; then
    echo "{\\"status\\":\\"done\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json
    echo "[agent_run] completed: $TASK_ID"
  else
    echo "{\\"status\\":\\"failed\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json
    echo "[agent_run] failed: $TASK_ID"
    exit 1
  fi
else
  echo "{\\"status\\":\\"pending-config\\",\\"task_id\\":\\"$TASK_ID\\",\\"error\\":\\"CONFIGURED=false. Edit scripts/agent_run.sh to add your execution command.\\"}" > .agent/status.json
  echo "[agent_run] not configured — set CONFIGURED=true and fill run_task() first."
  exit 1
fi
"""


OPENCLAW_WORKER_SH = """#!/usr/bin/env bash
# OpenClaw Worker — 拉取最新 handoff，执行任务，推回状态
#
# 前置要求（首次使用前必须配置）：
#   1. git init 并推送到 GitHub：
#        git init && git remote add origin <your-repo-url>
#        git push -u origin main
#   2. 确保 jq 已安装：
#        brew install jq   # macOS
#        apt install jq    # Ubuntu/Debian
#   3. 配置好 Git 凭据（HTTPS token 或 SSH key），保证 push/pull 不需要交互输入。
#   4. 将实际执行命令填入 scripts/agent_run.sh 并将 CONFIGURED 改为 true。
#
# 可选环境变量（运行时覆盖）：
#   OPENCLAW_REMOTE       远端名称，默认 origin
#   OPENCLAW_BRANCH       分支名称，默认当前分支
#   OPENCLAW_AUTO_PUSH    执行后自动推回，默认 true
#   OPENCLAW_ALLOW_DIRTY  允许工作区有未提交变更，默认 false
#   OPENCLAW_DRY_RUN      演练模式（不执行、不推送），默认 false

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$REPO_ROOT"

HANDOFF_FILE=".agent/handoff.json"
STATUS_FILE=".agent/status.json"
STATE_FILE=".agent/worker-state.json"

OPENCLAW_REMOTE="${OPENCLAW_REMOTE:-origin}"
OPENCLAW_BRANCH="${OPENCLAW_BRANCH:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)}"
OPENCLAW_AUTO_PUSH="${OPENCLAW_AUTO_PUSH:-true}"
OPENCLAW_ALLOW_DIRTY="${OPENCLAW_ALLOW_DIRTY:-false}"
OPENCLAW_DRY_RUN="${OPENCLAW_DRY_RUN:-false}"

# ── 依赖检查 ──────────────────────────────────────────────────────────────
require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "❌ 缺少命令: $1 — 请先安装后再运行 OpenClaw"
    exit 1
  fi
}
require_cmd git
require_cmd jq

# ── git 仓库检查 ────────────────────────────────────────────────────────
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "❌ 当前目录不是 git 仓库。请先运行："
  echo "     git init && git remote add origin <your-repo-url>"
  echo "     git add -A && git commit -m 'init' && git push -u origin main"
  exit 1
fi

if ! git remote get-url "$OPENCLAW_REMOTE" >/dev/null 2>&1; then
  echo "❌ 远端 '$OPENCLAW_REMOTE' 不存在。请先配置："
  echo "     git remote add $OPENCLAW_REMOTE <your-repo-url>"
  exit 1
fi

# ── 工作区洁净检查 ──────────────────────────────────────────────────────
if [[ "$OPENCLAW_ALLOW_DIRTY" != "true" ]]; then
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "❌ 工作区有未提交变更，请先 commit/stash，或设置 OPENCLAW_ALLOW_DIRTY=true"
    exit 1
  fi
fi

echo "== OpenClaw Worker =="
echo "repo:       $REPO_ROOT"
echo "remote:     $OPENCLAW_REMOTE"
echo "branch:     $OPENCLAW_BRANCH"
echo "auto_push:  $OPENCLAW_AUTO_PUSH"
echo "dry_run:    $OPENCLAW_DRY_RUN"
echo

# ── 拉取最新 handoff ────────────────────────────────────────────────────
if [[ "$OPENCLAW_DRY_RUN" != "true" ]]; then
  git fetch "$OPENCLAW_REMOTE" "$OPENCLAW_BRANCH"
  git pull --rebase "$OPENCLAW_REMOTE" "$OPENCLAW_BRANCH"
fi

# ── 校验 handoff ────────────────────────────────────────────────────────
if [[ ! -f "$HANDOFF_FILE" ]]; then
  echo "❌ 找不到 $HANDOFF_FILE — 请先填写任务后再运行 worker"
  exit 1
fi

if [[ "$OPENCLAW_DRY_RUN" != "true" ]]; then
  bash ./scripts/validate_handoff.sh >/dev/null
fi

task_id="$(jq -r '.task_id // empty' "$HANDOFF_FILE")"
if [[ -z "$task_id" ]]; then
  echo "❌ handoff 中 task_id 为空，请检查 $HANDOFF_FILE"
  exit 1
fi

# ── 去重检查（已完成任务不重复执行）───────────────────────────────────────
last_task_id=""
[[ -f "$STATE_FILE" ]] && last_task_id="$(jq -r '.last_task_id // empty' "$STATE_FILE" 2>/dev/null || true)"

status_value=""
status_task_id=""
if [[ -f "$STATUS_FILE" ]]; then
  status_task_id="$(jq -r '.task_id // empty' "$STATUS_FILE" 2>/dev/null || true)"
  status_value="$(jq -r '.status // empty' "$STATUS_FILE" 2>/dev/null || true)"
fi

if [[ "$task_id" == "$last_task_id" && "$status_task_id" == "$task_id" && "$status_value" == "done" ]]; then
  echo "ℹ️  无新任务（已完成）：$task_id"
  exit 0
fi

# ── 执行任务 ────────────────────────────────────────────────────────────
echo "▶ 执行任务：$task_id"
if [[ "$OPENCLAW_DRY_RUN" == "true" ]]; then
  echo "DRY RUN：跳过 scripts/agent_run.sh"
else
  bash ./scripts/agent_run.sh
fi

executed_at="$(date -Iseconds 2>/dev/null || date +%Y-%m-%dT%H:%M:%S)"
cat > "$STATE_FILE" <<EOF
{
  "last_task_id": "$task_id",
  "last_executed_at": "$executed_at"
}
EOF

# ── 推回状态 ────────────────────────────────────────────────────────────
if [[ "$OPENCLAW_DRY_RUN" == "true" ]]; then
  echo "DRY RUN：跳过 git push"
  exit 0
fi

if [[ "$OPENCLAW_AUTO_PUSH" == "true" ]]; then
  git add -A
  if [[ -n "$(git status --porcelain)" ]]; then
    git commit -m "chore(agent): complete $task_id at $executed_at"
    git push "$OPENCLAW_REMOTE" "$OPENCLAW_BRANCH"
    echo "✅ 已推送任务结果：$task_id"
  else
    echo "ℹ️  无文件变更，跳过 push"
  fi
else
  echo "ℹ️  auto push 已禁用（OPENCLAW_AUTO_PUSH=false）"
fi
"""


OPENCLAW_DAEMON_SH = """#!/usr/bin/env bash
# OpenClaw Daemon — 持续轮询执行 worker
#
# 使用方式：
#   bash ./scripts/openclaw_daemon.sh
#   OPENCLAW_POLL_SECONDS=60 bash ./scripts/openclaw_daemon.sh   # 每 60 秒轮询
#   OPENCLAW_MAX_ROUNDS=3 bash ./scripts/openclaw_daemon.sh      # 最多跑 3 轮
#   OPENCLAW_DRY_RUN=true bash ./scripts/openclaw_daemon.sh      # 演练模式

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$REPO_ROOT"

INTERVAL_SECONDS="${OPENCLAW_POLL_SECONDS:-30}"
MAX_ROUNDS="${OPENCLAW_MAX_ROUNDS:-0}"  # 0 表示无限循环
round=0

echo "== OpenClaw Daemon =="
echo "repo:          $REPO_ROOT"
echo "poll interval: ${INTERVAL_SECONDS}s"
if [[ "$MAX_ROUNDS" == "0" ]]; then
  echo "max rounds:    infinite"
else
  echo "max rounds:    $MAX_ROUNDS"
fi
echo

while true; do
  round=$((round + 1))
  echo "---- round $round @ $(date '+%Y-%m-%d %H:%M:%S') ----"
  if bash ./scripts/openclaw_worker.sh; then
    echo "worker done"
  else
    echo "worker failed (continuing daemon loop)"
  fi
  echo

  if [[ "$MAX_ROUNDS" != "0" && "$round" -ge "$MAX_ROUNDS" ]]; then
    echo "daemon finished: reached max rounds $MAX_ROUNDS"
    exit 0
  fi

  sleep "$INTERVAL_SECONDS"
done
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--path-mode", choices=["zero-to-one", "design-driven"], required=True)
    parser.add_argument(
        "--workflow",
        choices=["claude-planner-codex-builder", "codex-fullstack-workflow"],
        required=True,
    )
    parser.add_argument("--openclaw", action="store_true")
    parser.add_argument("--merge", action="store_true", help="Allow scaffolding into a non-empty directory")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()

    if root.exists() and any(root.iterdir()):
        if not args.merge:
            print(
                f"[error] Target directory already exists and is not empty: {root}\n"
                f"        Use --merge to scaffold into an existing directory, or choose a different target."
            )
            raise SystemExit(1)

    root.mkdir(parents=True, exist_ok=True)

    write(root / "AGENTS.md", make_agents_md(args.project_name))
    write(root / "agent-context/current-workflow.md", make_current_workflow(args.workflow))
    write(root / "agent-context/default-context.md", make_default_context(args.path_mode, args.openclaw))

    write(root / "ai-workflows/claude-planner-codex-builder/workflow.md", make_workflow_doc("Claude Planner + Codex Builder", "Claude manages planning/context, Codex handles execution."))
    write(root / "ai-workflows/claude-planner-codex-builder/agent-roles.md", make_agent_roles())
    write(root / "ai-workflows/codex-fullstack-workflow/workflow.md", make_workflow_doc("Codex Fullstack Workflow", "Codex handles planning, build, test, and review by default."))
    write(root / "ai-workflows/codex-fullstack-workflow/agent-roles.md", make_agent_roles())
    write(root / "ai-workflows/shared/handoff-template.md", "# Handoff Template\n\n- Goal\n- Constraints\n- Steps\n- Test commands\n")
    write(root / "ai-workflows/shared/review-template.md", "# Review Template\n\n- Findings\n- Risks\n- Follow-ups\n")
    write(root / "ai-workflows/shared/test-plan-template.md", "# Test Plan Template\n\n- Happy path\n- Edge cases\n- Regression checks\n")

    write(root / "docs/project-entry/workflow-selector.md", make_workflow_selector())
    write(root / "docs/workflows/collaboration-workflows-overview.md", make_collab_overview(args.path_mode, args.openclaw))
    write(root / "docs/product/active-prd.md", make_active_prd(args.project_name, args.path_mode))
    write(root / "docs/design/figma-source.md", make_design_file("Figma Source", args.path_mode == "design-driven", "Add the design source URL or selection details here."))
    write(root / "docs/design/design-analysis.md", make_design_file("Design Analysis", args.path_mode == "design-driven", "Translate layout, components, tokens, and interaction states here."))
    write(root / "docs/design/design-contract.md", make_design_file("Design Contract", args.path_mode == "design-driven", "List component mapping, token constraints, and acceptance rules here."))
    write(root / "docs/design/design-qa.md", make_design_file("Design QA", args.path_mode == "design-driven", "Record final design comparison and issues here."))

    if args.path_mode == "design-driven":
        write(root / "agent-context/design-role-rules.md", make_design_role_rules(today()))
        write(root / "docs/design/figma-mcp-setup.md", make_figma_mcp_setup())

    write(root / "project-management/active-sprint.md", make_active_sprint(args.project_name))
    write(root / "project-management/backlog.md", make_backlog())
    write(root / "project-management/changelog.md", make_changelog())

    write(root / "tasks/todo.md", make_todo(args.path_mode))
    write(root / "tasks/lessons.md", make_lessons())
    write(root / ".agent/handoff.json", make_handoff())
    write(root / ".agent/status.json", make_status())
    (root / ".agent/logs").mkdir(parents=True, exist_ok=True)

    write(root / "package.json", make_package_json(args.openclaw))
    write(root / "scripts/workflow_intent.sh", WORKFLOW_INTENT_SH)
    write(root / "scripts/validate_handoff.sh", VALIDATE_HANDOFF_SH)
    write(root / "scripts/agent_run.sh", AGENT_RUN_SH)
    if args.openclaw:
      write(root / "scripts/openclaw_worker.sh", OPENCLAW_WORKER_SH)
      write(root / "scripts/openclaw_daemon.sh", OPENCLAW_DAEMON_SH)

    for script in root.glob("scripts/*.sh"):
        script.chmod(0o755)

    result = {
        "target": str(root),
        "project_name": args.project_name,
        "path_mode": args.path_mode,
        "workflow": args.workflow,
        "openclaw": args.openclaw,
        "status": "ok",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # ── OpenClaw 启用时输出 git 配置清单 ────────────────────────────────────
    if args.openclaw:
        print()
        print("=" * 60)
        print("  OpenClaw 已启用 — 请完成以下 Git 配置后再运行 worker")
        print("=" * 60)
        print()
        print("【步骤 1】初始化 git 仓库并推送到 GitHub")
        print(f"  cd {root}")
        print("  git init")
        print("  git remote add origin <your-github-repo-url>")
        print("  git add -A")
        print("  git commit -m 'init: designer-vibecoding-starter scaffold'")
        print("  git push -u origin main")
        print()
        print("【步骤 2】确保 jq 已安装")
        print("  macOS : brew install jq")
        print("  Ubuntu: sudo apt install jq")
        print()
        print("【步骤 3】配置 Git 凭据（选其一）")
        print("  SSH  : ssh-keygen -t ed25519 && 将公钥添加到 GitHub Settings > SSH keys")
        print("  HTTPS: 使用 GitHub Personal Access Token，运行：")
        print("           git config credential.helper store")
        print("         首次 push 时输入 token 后会自动缓存")
        print()
        print("【步骤 4】填写执行命令")
        print(f"  编辑 {root}/scripts/agent_run.sh")
        print("  将 CONFIGURED=false 改为 CONFIGURED=true")
        print("  在 run_task() 中填入实际执行命令（如 codex run）")
        print()
        print("【步骤 5】演练验证（不会真正执行或推送）")
        print("  OPENCLAW_DRY_RUN=true npm run openclaw:worker")
        print()
        print("【步骤 6】正式启动")
        print("  npm run openclaw:worker   # 手动单次执行")
        print("  npm run openclaw:daemon   # 后台持续轮询（Ctrl+C 停止）")
        print()
        print("  可选环境变量：")
        print("    OPENCLAW_REMOTE=origin        # 远端名称")
        print("    OPENCLAW_BRANCH=main          # 目标分支")
        print("    OPENCLAW_POLL_SECONDS=30      # 轮询间隔（秒）")
        print("    OPENCLAW_AUTO_PUSH=true       # 执行后自动推回结果")
        print("    OPENCLAW_ALLOW_DIRTY=false    # 是否允许脏工作区")
        print()
        print("  完成配置后，通过 GitHub 写入新的 handoff.json 即可远程触发执行。")
        print()


if __name__ == "__main__":
    main()
