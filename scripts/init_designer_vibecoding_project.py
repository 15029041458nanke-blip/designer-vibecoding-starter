#!/usr/bin/env python3
"""
init_designer_vibecoding_project.py
单模型多 Agent 项目脚手架初始化脚本（v3.2）

用法：
    python init_designer_vibecoding_project.py \
        --target /path/to/my-project \
        --project-name "我的产品" \
        --path-mode zero-to-one        # 或 design-driven
        [--merge]                      # 允许向非空目录写入

变更（v3.2）：
    - agent-context/design-role-rules.md 改为全路径生成（不再仅限 design-driven）
    - skills/style-foundation/SKILL.md 改为全路径生成（不再按路径条件分流）
    - 理由：0-1 路径后续大概率会引入设计稿，提前 scaffold 降低补文件成本

变更（v3.1）：
    - style-foundation Skill 集成（0-1 路径参考图分流）
    - Constitution 驱动 Token 生成

变更（v3.0）：
    - 移除 --workflow / --openclaw 参数（不再支持 Codex/OpenClaw 架构）
    - 新增 skills/ 目录，内联 7 个 SKILL.md 文件
    - 新增 project-management/prd-registry.md（PRD 主控追踪）
    - 移除 .agent/ / ai-workflows/ / openclaw 相关脚本生成
    - AGENTS.md 更新为 v2.1 单模型多 Agent 风格
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────────────────

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _copy_style_foundation(root: Path) -> None:
    """
    从 skill 安装目录复制 style-foundation/SKILL.md 到目标项目。
    v3.2：全路径生成，不再依赖 path-mode 条件。

    查找顺序：
    1. 脚本同级的 ../skills/style-foundation/SKILL.md（开发目录结构）
    2. ~/.config/codewiz/skills/designer-vibecoding-starter/skills/style-foundation/SKILL.md
    """
    import shutil

    candidates = [
        Path(__file__).parent.parent / "skills" / "style-foundation" / "SKILL.md",
        Path.home() / ".config" / "codewiz" / "skills" / "designer-vibecoding-starter"
        / "skills" / "style-foundation" / "SKILL.md",
    ]
    src = next((p for p in candidates if p.exists()), None)
    dest = root / "skills" / "style-foundation" / "SKILL.md"

    if src:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"[style-foundation] 复制自 {src}")
    else:
        # fallback：写一个最小占位文件，避免项目 scaffold 不完整
        write(
            dest,
            "# Skill: style-foundation\n\n"
            "> 风格基石 Skill — 请从 designer-vibecoding-starter 安装目录手动复制完整版本。\n"
            "> 安装路径：~/.config/codewiz/skills/designer-vibecoding-starter/skills/style-foundation/SKILL.md\n",
        )
        print("[style-foundation] 未找到源文件，已写入占位文件，请手动补充完整版本。")


# ──────────────────────────────────────────────────────────────────────────────
# 顶层治理文件
# ──────────────────────────────────────────────────────────────────────────────

def make_agents_md(project_name: str) -> str:
    return f"""# AGENTS.md（项目级总规则入口）

> 最高优先级规则文件。所有 agent、子 agent、工具调用均须遵守本文件。
> 本文件 = 强制规则，不是建议。
> 版本：v2.3（单模型多 Agent + PRD 驱动开发流）

> ⚡ **新会话强制启动协议——收到任何消息前必须先执行，不得跳过、不得等用户提问：**
> 1. 读 `agent-context/current-workflow.md`
> 2. 读 `project-management/prd-registry.md`
> 3. 读 `LEARNINGS.md`（如存在）
> 4. 主动告知用户：「当前 Active PRD 是 [XXX]，下一步是 [task]，确认继续？」
> 用户说「开始」时，同样触发此协议后再行动。

---

## 项目信息

- **项目名**：{project_name}
- **初始化**：{today()} via `designer-vibecoding-starter`

---

## 1. 协作架构（单模型多 Agent）

本项目采用 **单模型多 Agent** 模式，Codewiz 是唯一主导：

```
用户
 └→ Codewiz（主 agent：规划 + 编排 + review）
       ├─ 子 agent-1（实现 task-1，隔离上下文）
       ├─ 子 agent-2（review task-1，隔离上下文）
       ├─ 子 agent-3（实现 task-2，隔离上下文）
       └─ ...
```

**核心原则**：
- Codewiz 是唯一编排者，负责规划、拆解、派发子 agent、review
- 每个子 agent 获得精确构造的上下文（不继承对话历史）
- 子 agent 只执行一个明确的 task，完成后上报状态

---

## 1.5 角色 → Skill 对照表

| 原角色 | 对应 Skill | 触发条件 |
|--------|-----------|---------|
| `design-analyst` | `skills/design-analysis` | 有设计稿输入 / UI 任务完成前 |
| `product-strategist` | `skills/requirements-refinement` | 需求不清 / PRD 缺 AC |
| `project-manager` | `project-management/prd-registry.md` 协议 | 会话启动 / 任务完成 |
| `architect` | `skills/architecture-check` + `skills/writing-plans` | 架构变更前 / 中大任务 |
| `engineer` | 子 agent 执行协议 | 每个实现 task |
| `reviewer` | `skills/two-stage-review` | 每个 task 完成后 |
| `tester` | `two-stage-review` AC 验证阶段 | 同 reviewer |

---

## 2. 任务分级与强制流程

### 🟢 小任务（≤2步，单文件，无架构变更）
```
直接实现 → verify（build 通过）→ 完成
```

### 🟡 中任务（3-6步，跨2个模块）
```
写 plan → spec 自检 → 实现（可派子 agent）→ 两阶段 review → 完成
```

### 🔴 大任务（跨模块/架构调整/高风险）
```
brainstorming → 写 spec → spec 自检 → 用户 review spec
→ 写 plan → 子 agent 实现（每 task 独立）→ 两阶段 review → 完成
```

**不允许跳级**：大任务不得直接进入实现。

---

## 3. 强制 Skill：何时触发

| 触发情况 | 必须使用的 Skill |
|---|---|
| 输入包含 Figma 链接 / 设计稿引用 | `skills/design-analysis` Phase-1 |
| 任何 UI 任务进入 DoD 前 | `skills/design-analysis` Phase-2 |
| 需求描述不具体 / PRD 缺 AC | `skills/requirements-refinement` |
| 任何 bug / 测试失败 / 意外行为 | `skills/systematic-debugging` |
| 新功能 / 新组件（中/大任务） | `skills/writing-plans` |
| 大任务需求不清晰 | `skills/brainstorming` |
| 每个 task 完成后 | `skills/two-stage-review` |
| 架构变更前 | `skills/architecture-check` |

---

## 4. 子 Agent 协议

子 agent 状态：`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`

- `BLOCKED` 连续 3 次 → 停止，向用户上报，不得继续猜测
- 派发时必须提供：任务全文 + 相关文件路径 + 验证命令

---

## 5. Plan 质量规则

```
❌ "TBD" / "TODO" / "后续处理"
❌ "添加适当的错误处理"
❌ 没有验证命令的步骤
❌ 代码步骤没有实际代码
```

---

## 6. 两阶段 Review 门控

每个 task 完成后必须执行（见 `skills/two-stage-review/SKILL.md`）：
1. Spec 合规 Review
2. 代码质量 Review

两关都通过才算完成。

---

## 7. 完成定义（DoD）

- [ ] 功能可运行
- [ ] `npm run build`（或对应构建命令）通过
- [ ] 两阶段 review 通过
- [ ] 有设计稿时：Design QA 通过
- [ ] 无明显回归风险

---

## 8. 会话启动协议（PRD 驱动）

**⚠️ 强制执行，不得等待用户提问，不得跳过任何步骤。**

```
Step 1  读 agent-context/current-workflow.md   → 获取当前路径和状态
Step 2  读 project-management/prd-registry.md  → 找到 Active PRD 和未完成任务
Step 3  读 LEARNINGS.md（如存在）              → 避免重复犯同类错误
Step 4  主动输出启动报告（格式如下）：
```

**启动报告格式**（每次新会话必须输出）：

```
📋 会话启动报告
━━━━━━━━━━━━━━━━━━━━━━━━
Active PRD：[PRD-XXX 名称]
当前状态：[in-progress / queued]
下一步任务：[具体 task 描述]
相关设计稿：[有 / 无]
━━━━━━━━━━━━━━━━━━━━━━━━
确认继续这个任务吗？还是要调整方向？
```

**触发词**：用户说「**开始**」时，立即执行完整启动协议后再等待确认。

---

## 9. 任务完成更新协议

每个任务完成后：

```
1. 在 prd-registry.md 中将该任务标记为 ✅ done
2. 将下一个任务标记为 🔄 in-progress
3. 如果当前 PRD 所有任务完成 → PRD 移入已完成，取下一个 PRD
4. 更新 project-management/changelog.md
```

---

## 10. Skills 目录

```
skills/
├── design-analysis/SKILL.md         # 设计分析（前置 + 后置 QA）
├── style-foundation/SKILL.md        # 风格基石（参考图/描述 → 风格宪法）
├── requirements-refinement/SKILL.md # 需求精化（DoR 检查 + AC 补全）
├── systematic-debugging/SKILL.md    # Debug 四阶段规则
├── writing-plans/SKILL.md           # Plan 写作规范
├── brainstorming/SKILL.md           # 需求探索
├── two-stage-review/SKILL.md        # 两阶段 Review
└── architecture-check/SKILL.md      # 架构变更前检查
```

---

## 11. 信息写入路由（★ 强制前置判断）

**每次需要记录/新增任何信息时，必须先执行以下判断，再决定写哪个文件。禁止直接追加到 AGENTS.md。**

```
要写的内容是什么？
│
├── 产品交互行为规则
│   （菜单关闭、颜色规则、操作约束、UI 状态机等）
│   → 写入 docs/product/ 对应 .md 文件
│   → 在本文件第 12 章引用表格里加一行指针
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 开发经验/踩坑记录
│   → 写入 LEARNINGS.md 或 tasks/knowledge/lessons.md
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 需求/功能/AC
│   → 写入 tasks/prd/ 对应 PRD 文件
│   → 在 project-management/prd-registry.md 更新状态
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 重要架构/产品决策
│   → 写入 project-management/decision-log.md
│   ❌ 禁止写入 AGENTS.md 正文
│
└── AI 协作流程规则
    （agent 协议、DoD 定义、review 流程、Skill 触发条件）
    → 写入 AGENTS.md 或 skills/ 对应 SKILL.md
    ✅ 这是 AGENTS.md 唯一允许的新增内容类型
```

**快速判断口诀**：去掉 AI 工具后，工程师还需要这条信息吗？
- 需要 → 不属于 AGENTS.md，找对应的产品/需求/决策文件
- 不需要 → 属于 AI 协作层，可以写入 AGENTS.md 或 skills/

---

## 12. 产品规范引用表（只放指针，正文在 docs/product/）

| 规范类型 | 文档位置 |
|---------|---------|
| 交互规则（菜单关闭、组件行为等） | [`docs/product/`](docs/product/) |

---

## 13. 会话启动触发词

新会话时，用户只需发送：

> **「开始」**

Codewiz 收到「开始」后必须：先完整执行第 8 章启动协议（读 3 个文件 + 输出启动报告），再等待用户确认，不得直接进入实现。

---

_版本：v2.3 | 初始化时间：{today()} | 启动协议升级：v2.3_
"""


def make_learnings_md() -> str:
    return f"""# LEARNINGS.md

> 记录本项目的经验教训。每次会话开始时必读，避免重复犯同类错误。

---

## 规则

- 每次重复出现的问题，在此记录一条教训
- 每条教训格式：`[日期] [类别] 描述`
- 类别：`[架构]` / `[调试]` / `[需求]` / `[工作流]`

---

## 教训记录

<!-- 在此追加，最新的放在最上面 -->

_{today()} 项目初始化，暂无教训记录_
"""


# ──────────────────────────────────────────────────────────────────────────────
# agent-context/
# ──────────────────────────────────────────────────────────────────────────────

def make_current_workflow(path_mode: str) -> str:
    path_desc = (
        "设计驱动路径：Figma → design-analysis Phase-1 → PRD → 实现 → Design QA"
        if path_mode == "design-driven"
        else "0-1 路径：逐步追问（6 步）→ PRD 确认 → 实现 → review"
    )
    return f"""# Current Workflow

updated_at: {today()}
path_mode: {path_mode}

---

## 启动必读顺序

1. `/AGENTS.md`
2. `/agent-context/current-workflow.md`（本文件）
3. `/project-management/prd-registry.md`
4. `/LEARNINGS.md`（如存在）

## 当前交付路径

{path_desc}

## 设计稿场景判断

| 场景 | 判断标准 | 处理方式 |
|------|---------|---------|
| A：大型多功能设计稿 | 顶层 Frame ≥2，功能相互独立 | 拆分为多个 PRD，逐一分析 |
| B：文字 PRD + 设计稿 | 用户同时提供两份输入 | 对照对齐，产出一致/疑点/风险三类结论 |
| C：单组件设计稿 | 内容聚焦于一个组件/模块 | 先查 prd-registry，再决定是否新建 PRD |

## 规则

- 只有一条交付路径在同一时间是 active 的
- 如需切换路径，先更新本文件
"""


def make_design_role_rules() -> str:
    """v3.2：全路径生成，不再限于 design-driven 路径"""
    return """# Design Role Rules

> 本文件是 `skills/design-analysis/SKILL.md` 的扩展规则库。
> 执行任何设计分析前必读。
> 内容来源：项目实践沉淀，优先级高于 SKILL.md 文档。

---

## §1 图标还原规则

- 始终使用设计稿指定的图标组件或 SVG，禁止用 emoji 替代
- 图标尺寸：以设计稿像素值为准，映射到 `--icon-size-*` token
- 图标颜色：继承父元素 `color`（`currentColor`），不硬编码
- 不同状态下图标的变化（如 filled/outlined）必须在状态矩阵中标注

## §2 Border 规则

- `backgroundColor`（填充色）与 `borderColor`（描边色）在同一节点上永远互斥
  - 设填充色 → 清除 borderColor
  - 设描边色 → 清除 backgroundColor
- border-width：使用设计稿标注值，禁止四舍五入
- border-radius：优先使用 design token（`--radius-*`），无 token 时使用具体 px 值

## §3 尺寸还原规则

- 不得将设计稿 px 值"估计"为圆整数，必须与标注一致
- 用 `rem` 时，换算基准明确标注（通常 1rem = 16px）
- min-width / max-width 等约束：设计稿未标注时，必须作为"设计疑点"记录，不得自行推断

## §4 节点类型规则

- Frame → `<div>`（布局容器）
- Text → `<span>` 或 `<p>`（取决于块级/内联语义）
- Component → 使用项目对应的 React/Vue 组件，不直接写 HTML
- Group → 检查是否有布局含义（如果无，可以合并到父节点）
- Vector/SVG → 直接导出为 SVG 文件，禁止用 PNG 代替

## §5 布局对齐规则

- Auto Layout → CSS Flexbox
  - direction: horizontal → `flex-direction: row`
  - direction: vertical → `flex-direction: column`
  - spacing: `gap` 属性
  - padding: 按 top/right/bottom/left 分别设置
- Grid Layout → CSS Grid
- 绝对定位（Absolute）→ `position: absolute`，只在设计稿明确使用时才用

## §6 组件系统规则

- 优先复用项目已有组件（查 src/components/ 或设计系统）
- 新建组件前检查：功能是否与现有组件 ≥80% 重叠？若是，考虑扩展而非新建
- 组件 Props 命名与设计稿的属性名保持一致（如 `variant`, `size`, `disabled`）

## §7 走查清单（Design QA 执行时使用）

- [ ] 颜色值：与设计稿 token 完全一致？
- [ ] 间距：padding/margin/gap 均与设计稿标注一致？
- [ ] 字体：size / weight / line-height 一致？
- [ ] 圆角：border-radius 一致？
- [ ] 状态矩阵：default/hover/active/disabled/focus/error 均已实现？
- [ ] 图标：尺寸/颜色/类型与设计稿一致？
- [ ] 响应式：设计稿涉及的断点均已处理？
- [ ] 动效：transition 时间/缓动函数与标注一致？

---

_来源：项目实践迭代沉淀_
"""


# ──────────────────────────────────────────────────────────────────────────────
# skills/（7 个 Skill 模板）
# ──────────────────────────────────────────────────────────────────────────────

SKILL_DESIGN_ANALYSIS = """\
# Skill: design-analysis

> 分两阶段：Phase-1（前置设计分析）和 Phase-2（后置 Design QA）。
> 两个阶段都是强制门控，不得跳过。
>
> **扩展规则库**（执行前必读）：`agent-context/design-role-rules.md`

---

## 触发条件

| 场景 | 触发阶段 |
|---|---|
| 任务输入包含 Figma 链接或设计稿引用 | Phase-1（必须在写 Plan 前完成） |
| 任何 UI 任务进入 DoD 检查前 | Phase-2 |

---

## 设计稿场景判断（Phase-1 前置）

### 场景 A：大型多功能设计稿
顶层 Frame ≥2，功能相互独立 → 向用户展示拆分方案，确认后逐一分析，拆为多个 PRD。

### 场景 B：文字 PRD + 设计稿
先读 PRD 提取功能清单，再分析设计稿，产出三类结论：
- ✅ 一致项 → 写入 AC
- ⚠️ 设计稿有、PRD 未提及 → 逐一询问用户
- ❗ PRD 有、设计稿未覆盖 → 标注设计遗漏风险

### 场景 C：单组件设计稿
先查 prd-registry.md，判断归属现有 PRD 还是新建 PRD。

---

## Phase-1：执行步骤

1. 调用 Figma MCP 拉取节点数据
2. 提取组件层级、状态矩阵、间距、颜色、字体、交互行为
3. 识别设计疑点（未标注的状态/不一致/非标准值）
4. 逐一消除疑点（一次一问，等待确认）
5. 输出设计分析包（状态矩阵 + 间距规格 + 交互行为 + 已确认疑点）
6. 转化为 PRD UI 规格 + Acceptance Criteria

每条 AC 格式：
> AC-1: 当 [条件] 时，[行为] → [可观察结果]（含具体颜色值/像素值）

---

## Phase-2：Design QA 步骤

1. 读 PRD AC 列表 + Phase-1 设计分析包
2. 逐 AC 定位代码，提取实际值，与设计规格对比
3. 输出 QA 报告（PASS / FAIL / NEEDS_CLARIFICATION）
4. Critical 项全部 PASS → 还原通过，可进入 DoD

严重度：Critical（设计意图被错误还原，阻塞发布）/ Minor（像素级偏差，记录即可）

---

_版本：v1.0_
"""

SKILL_REQUIREMENTS_REFINEMENT = """\
# Skill: requirements-refinement

> 对应原 `product-strategist` + `project-manager` 规划侧职责。
> 目标：确保每个进入开发的需求满足 Definition of Ready（DoR）。

---

## 触发条件

- 需求描述不够具体（缺 AC / 范围 / 角色）
- 现有 PRD 缺少 Acceptance Criteria
- 新需求与现有 PRD 有范围重叠

---

## Definition of Ready（DoR）

进入开发前，需求必须满足：
- [ ] User Story 格式：作为 [角色]，我想 [操作]，以便 [目的]
- [ ] 有明确 Acceptance Criteria（每条可独立验证）
- [ ] 范围边界清晰（有"不包含"列表）
- [ ] 外部依赖明确（设计稿 / API / 其他 PRD）
- [ ] 优先级已确认（P0 / P1 / P2）
- [ ] 无未解决的需求冲突

---

## 执行步骤

1. DoR 快速检查，标记所有未满足项
2. 逐项补全（一次一问）：
   - "这个功能是为了解决什么问题？"
   - "完成后，你怎么判断它做好了？"
   - "这个功能不包含哪些情况？"
   - "优先级如何？"
   - "有设计稿吗？"
3. 输出完整 PRD（User Story + AC + Scope + 依赖 + 优先级）

---

_版本：v1.0_
"""

SKILL_SYSTEMATIC_DEBUGGING = """\
# Skill: systematic-debugging

> 遇到任何 bug / 测试失败 / 意外行为，必须按四阶段执行。
> 铁律：未找到根因，禁止提 fix。已尝试 3 次 fix 仍失败，禁止继续，向用户上报。

---

## 触发条件

- 任何 bug / 测试失败 / 意外行为
- 代码改动后出现回归

---

## 四阶段流程

### 阶段 1：症状记录
- 精确描述：什么触发 / 什么现象 / 期望 vs 实际
- 收集：错误信息 / 堆栈 / 日志

### 阶段 2：根因假设
- 列出 2-3 个可能的根因（不要只列一个）
- 按可能性排序

### 阶段 3：最小复现
- 构造最小复现用例，隔离变量
- 验证假设：一次只改一个变量

### 阶段 4：修复 + 回归验证
- 找到根因后提出 fix
- 验证 fix 不引入新回归

---

## 铁律

```
❌ 未找到根因，禁止提 fix
❌ 已尝试 3 次 fix 仍失败，禁止继续加 fix
✅ 3 次 fix 失败 → 停下来质疑架构，向用户上报
```

---

_版本：v1.0_
"""

SKILL_WRITING_PLANS = """\
# Skill: writing-plans

> 对应原 `architect` 角色的规划职责。
> 中大任务在进入实现前，必须先写 Plan。

---

## ★ 写之前：信息写入路由检查（前置必做）

**写任何文件之前，先判断内容类型，再决定写哪里。**

```
要写的内容是什么？
│
├── 产品交互行为规则（菜单/颜色/操作约束）
│   → docs/product/ 对应文件
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 开发经验 / 踩坑记录
│   → LEARNINGS.md 或 tasks/knowledge/lessons.md
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 需求 / 功能 / AC
│   → tasks/prd/ 对应 PRD 文件
│   ❌ 禁止写入 AGENTS.md 正文
│
├── 架构 / 产品决策
│   → project-management/decision-log.md
│   ❌ 禁止写入 AGENTS.md 正文
│
└── AI 协作流程规则（agent 协议、DoD、review 流程）
    → AGENTS.md 或 skills/ 对应 SKILL.md
    ✅ AGENTS.md 唯一允许写正文的内容类型
```

**口诀**：去掉 AI 工具后，工程师还需要这条信息吗？需要 → 对应产品/需求文件；不需要 → AGENTS.md。

---

## 触发条件

- 任何 3 步以上的新功能或新组件
- 跨模块的改动
- 涉及架构变更的任务

---

## Plan 必须包含的内容

每个 step 必须包含：
1. 做什么（具体操作）
2. 怎么做（代码/命令）
3. 如何验证（期望输出/通过标准）

---

## Plan 禁止出现的内容

```
❌ "TBD" / "TODO" / "后续处理"
❌ "添加适当的错误处理"（必须说明是什么错误处理）
❌ "参考 Task N 的写法"（必须把代码重复写出来）
❌ "按现有逻辑处理"（必须明确说是什么逻辑）
❌ 没有验证命令的步骤
❌ 代码步骤没有实际代码
```

---

## Spec 自检（写完 Plan 后必须执行）

1. Placeholder 扫描：有无上述禁止表达？
2. 内部一致性：各章节是否矛盾？
3. 范围检查：是否混入了不相关功能？
4. 歧义检查：每条需求是否只有一种解读？

---

_版本：v1.0_
"""

SKILL_BRAINSTORMING = """\
# Skill: brainstorming

> 用于大任务需求不清晰时的探索阶段。
> 必须在写 Spec 之前完成。

---

## 触发条件

- 大任务需求描述模糊，存在多种解读
- 涉及新的产品方向，需要先探索可行性
- 用户提出"我想做 X，但不确定怎么做"

---

## 执行步骤

1. **现状分析**：用户现在是怎么做的？痛点在哪里？
2. **目标澄清**：成功完成后，用户能做到什么是现在做不到的？
3. **方案发散**：列出 2-3 种可能的实现方向，每种附优缺点
4. **约束确认**：技术约束 / 时间约束 / 范围约束
5. **选择 + 文档化**：用户选定方案后，输出简明的决策记录

---

## 产物

- 决策记录（写入 `project-management/decision-log.md`）
- 简明的需求范围（作为 requirements-refinement 的输入）

---

_版本：v1.0_
"""

SKILL_TWO_STAGE_REVIEW = """\
# Skill: two-stage-review

> **触发条件**：每个 task 完成后，必须顺序执行两阶段 review。两阶段都通过，才算完成。

---

## 执行顺序（不可调换，不可跳过）

```
Task 实现完成
    ↓
阶段 1：Spec 合规 Review
    ↓ 通过
阶段 2：代码质量 Review
    ↓ 通过
Task 完成 ✅
```

---

## 阶段 1：Spec 合规 Review

- [ ] spec 中每条需求，代码里是否有对应实现？（逐条核对）
- [ ] 有没有实现了 spec 以外的功能？（over-engineering 也算问题）
- [ ] 所有边界条件是否处理了？（空值、异常输入、极端情况）
- [ ] 错误处理是否明确？

**未通过 → 实现者修复 → 重新 review（不得跳过）**

---

## 阶段 2：代码质量 Review

- [ ] 类型安全（TypeScript 严格模式无 any？）
- [ ] 是否遵循项目架构规则？
- [ ] 相同逻辑是否超过 2 处？（应抽取）
- [ ] 是否有明显的回归风险？
- [ ] 命名是否清晰？

**未通过 → 修复 → 重新 review（不得跳过）**

---

## review 后需要补写文档时：信息写入路由

| 内容类型 | 写入位置 |
|---------|---------|
| 产品交互行为规则 | `docs/product/` 对应文件 |
| 开发踩坑 / 经验 | `LEARNINGS.md` 或 `tasks/knowledge/lessons.md` |
| 需求 / AC 变更 | `tasks/prd/` 对应 PRD 文件 |
| 架构 / 产品决策 | `project-management/decision-log.md` |
| AI 协作规则 | `AGENTS.md` 或 `skills/` 对应 SKILL.md |

**禁止把产品规则、踩坑记录、需求变更直接追加进 AGENTS.md 正文。**

---

_版本：v1.0_
"""

SKILL_ARCHITECTURE_CHECK = """\
# Skill: architecture-check

> 任何架构变更前必须执行。
> 目标：在动手前发现架构问题，避免事后重构。

---

## 触发条件

- 新增目录或模块
- 引入新的数据流或状态管理方式
- 改变组件间的依赖关系
- 修改核心数据结构

---

## 执行步骤

### 快速扫描清单

- [ ] 相同逻辑是否出现在 2+ 个文件？（→ 应抽取）
- [ ] 新功能是否引入了新"维度"？（→ 检查是否有统一入口）
- [ ] 改动文件是否超过 500 行？（→ 应提前拆分）
- [ ] 数据来源是否唯一（Single Source of Truth）？
- [ ] 新模块的边界是否清晰？（职责是否单一）

### 发现问题时

**禁止沉默**。必须向用户说明：
1. 当前需求会带来什么技术债
2. 架构调整的收益
3. 获得确认后再重构

---

## 架构检查后需要补写规则时：信息写入路由

| 内容类型 | 写入位置 |
|---------|---------|
| 产品交互行为规则（颜色互斥、状态机） | `docs/product/` 对应文件 |
| 架构决策（为什么这样设计） | `project-management/decision-log.md` |
| 开发踩坑记录 | `LEARNINGS.md` |
| AI 协作流程规则 | `AGENTS.md` 或 `skills/` 对应 SKILL.md |

**禁止把产品规则或架构约束直接写进 AGENTS.md 正文。**
AGENTS.md 只保留指向 `docs/product/` 的引用指针。

---

_版本：v1.0_
"""


# ──────────────────────────────────────────────────────────────────────────────
# project-management/
# ──────────────────────────────────────────────────────────────────────────────

def make_prd_registry(project_name: str) -> str:
    return f"""# PRD Registry（PRD 主控追踪）

> **单一数据源**：所有 PRD 的状态、优先级、进度均在此文件追踪。
> 每次会话启动时必读；每个任务完成后必须更新。

---

## 会话启动协议

每次新会话，Codewiz 必须：

```
1. 读取本文件
2. 找到 Active PRD 和当前未完成任务
3. 告知用户：「当前 Active PRD 是 [XXX]，下一步是 [task]，确认继续？」
4. 用户确认 → 开始执行
```

---

## 任务完成更新协议

```
1. 将完成的任务标记为 ✅ done
2. 将下一个任务标记为 🔄 in-progress
3. 如果当前 PRD 所有任务完成 → 移入"已完成 PRD"，从队列取下一个
4. 更新 project-management/changelog.md
```

---

## Active PRD

<!-- 当前正在开发的 PRD，每次只有一个 Active -->

| ID | 名称 | 优先级 | 状态 | 设计稿 |
|----|------|--------|------|--------|
| PRD-001 | {project_name} MVP | P0 | 🔄 in-progress | 待补充 |

### PRD-001 任务清单

| # | 任务 | 状态 |
|---|------|------|
| 1 | 完善 PRD（填写 User Story / AC / 功能范围） | ⬜ pending |
| 2 | 架构检查（architecture-check Skill） | ⬜ pending |
| 3 | 编写实现 Plan（writing-plans Skill） | ⬜ pending |
| N | Design QA（如有设计稿） | ⬜ pending |

---

## PRD 队列（待开发）

| ID | 名称 | 优先级 | 状态 | 备注 |
|----|------|--------|------|------|
| — | 暂无排队需求 | — | — | 从 backlog 中提取 |

---

## 已完成 PRD

| ID | 名称 | 完成时间 | 备注 |
|----|------|---------|------|
| — | 暂无 | — | — |

---

## Sprint 生命周期

### 关闭协议
```
1. 确认本 Sprint 所有 PRD 任务完成
2. 将本 Sprint 快照归档到 project-management/active-sprint.md（注明日期）
3. 在 changelog.md 记录 Sprint 产出摘要
```

### 开启协议
```
1. 从 PRD 队列中选取下一批 PRD
2. 更新 active-sprint.md（新 Sprint 目标 + PRD 清单）
3. 将第一个 PRD 设为 Active
```

---

_初始化：{today()}_
"""


def make_active_sprint(project_name: str) -> str:
    return f"""# Active Sprint

- 项目：{project_name}
- 状态：in-progress
- 开始时间：{today()}

---

## Sprint 目标

- 完成项目初始化
- 明确第一个 MVP 需求（PRD-001）
- 产出可验证的第一个交付物

---

## PRD 清单

| PRD | 状态 |
|-----|------|
| PRD-001 | 🔄 in-progress |

---

## Checklist

- [ ] PRD-001 完成需求精化（requirements-refinement）
- [ ] PRD-001 通过两阶段 review
- [ ] changelog.md 更新
"""


def make_backlog() -> str:
    return """# Backlog（想法池）

> 未进入 PRD 队列的原始想法。
> 定期 review，有价值的提升为 PRD，加入 prd-registry.md 队列。

---

## 待探索

- [ ] （在此记录你的产品想法）

## 已评估，暂不做

- （无）

## 已提升为 PRD

- （无）
"""


def make_changelog() -> str:
    return f"""# Changelog

## {today()}

- 项目通过 `designer-vibecoding-starter` scaffold 初始化
- 创建 PRD-001 占位
"""


def make_decision_log() -> str:
    return f"""# Decision Log（决策记录）

> 记录重要的架构和产品决策，及其背景与理由。

---

## 格式

```
### [日期] [决策标题]
- **背景**：为什么需要做这个决策？
- **选项**：考虑了哪些方案？
- **决策**：选择了哪个方案？
- **理由**：为什么选这个？
```

---

## 记录

### {today()} 项目初始化
- **背景**：项目通过 designer-vibecoding-starter 初始化
- **决策**：使用单模型多 Agent 架构（Codewiz 主导）
- **理由**：避免多模型协调开销，Codewiz 负责规划+编排，子 agent 执行具体 task
"""


# ──────────────────────────────────────────────────────────────────────────────
# tasks/
# ──────────────────────────────────────────────────────────────────────────────

def make_prd_001(project_name: str, path_mode: str) -> str:
    design_section = (
        "设计稿已提供，执行 design-analysis Phase-1 后填充此区块。"
        if path_mode == "design-driven"
        else "无（0-1 路径，后续有设计稿时补充）"
    )
    return f"""# PRD-001: {project_name} MVP

> 状态：🔄 in-progress
> 优先级：P0
> 设计稿：{design_section}
> 依赖：无

---

## 1. User Story

作为 [目标用户]，我想要 [核心功能]，以便 [用户价值]。

<!-- 从对话中生成后填入 -->

---

## 2. 功能范围

### 包含

- [ ] （功能点 1）
- [ ] （功能点 2）
- [ ] （功能点 3）

### 不包含（Out of Scope）

- （明确排除的功能）

---

## 3. 设计规格

{design_section}

---

## 4. Acceptance Criteria

- AC-1: 当 [条件] 时，[行为] → [可观察结果]
- AC-2: ...
- AC-3: （边界/错误场景）

---

## 5. 实现任务拆解

（由 writing-plans Skill 输出后填入）

| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 1 | ... | ⬜ pending | - |

---

_版本：草稿 | 创建时间：{today()}_
"""


def make_vercelignore() -> str:
    return """\
# ============================================================
# Vercel 部署忽略文件
# vibecoding 项目三层架构：只有"应用代码层"进入 CDN
# ============================================================

# ── AI 协作层（AI 工具专用，不随产品交付）────────────────────
AGENTS.md
LEARNINGS.md
skills/
agent-context/

# ── 需求追踪层（开发过程文档，不随产品交付）──────────────────
tasks/
project-management/

# ── 产品规范层（工程师参考文档，不部署但保留在 git）────────────
# docs/ 目录保留在 git（版本管理），但不进入生产服务器
docs/

# ── 开发工具 ────────────────────────────────────────────────
scripts/
presentations/
tokens/

# ── 说明 ─────────────────────────────────────────────────────
# "应用代码层"（实际进入 CDN 的）：
#   src/ public/ index.html package.json vite.config.ts 等
# Vite 构建后只有 dist/ 被部署，以上三层均不会出现在生产环境。
"""


def make_dockerignore() -> str:
    return """\
# ============================================================
# Docker 部署忽略文件（有后端服务时使用）
# ============================================================

# ── AI 协作层 ────────────────────────────────────────────────
AGENTS.md
LEARNINGS.md
skills/
agent-context/

# ── 需求追踪层 ───────────────────────────────────────────────
tasks/
project-management/

# ── 产品规范层（不进入容器，但保留在 git）──────────────────────
docs/

# ── 开发工具 ────────────────────────────────────────────────
scripts/
presentations/
tokens/
*.test.ts
*.test.tsx

# ── 标准排除 ─────────────────────────────────────────────────
node_modules/
dist/
.env
.env.local
"""


def make_docs_product_readme() -> str:
    return """\
# Product Specs

> 产品行为规范文档目录。以下规范是工程师实现功能的权威依据，
> 与代码库共同演进，不依赖 AI 工具即可阅读。

---

## 规范列表

| 文件 | 内容 |
|------|------|
| （在此添加规范文件） | — |

---

## 如何添加新规范

1. 在本目录新建 `<feature>-spec.md`
2. 在本 README 的规范列表中添加索引条目
3. 在 `AGENTS.md` 第 11 章的引用表格里加一行指向新文件

---

## 信息归属原则

| 问题 | 放在哪里 |
|------|---------|
| 这条规则给 AI 工具看的吗？（如 review 流程、DoD 定义） | `AGENTS.md` / `skills/` |
| 这条规则描述产品行为的吗？（如菜单关闭机制、颜色规则） | `docs/product/`（本目录） |
| 需求和验收标准（AC）？ | `tasks/prd/` |

**快速判断**：去掉 AI 工具后，工程师还需要这条规则吗？
- 需要 → `docs/product/`
- 不需要 → `AGENTS.md` / `skills/`
"""


def make_lessons() -> str:
    return """# Lessons（经验教训）

> 记录重复出现的问题和优化方案。
> 每次开始重要工作前，review 相关条目。

---

## 格式

`[日期] [类别] 教训描述`

类别：`[架构]` / `[调试]` / `[需求]` / `[工作流]`

---

## 记录

<!-- 追加教训，最新在最上面 -->
"""


# ──────────────────────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="designer-vibecoding-starter v3.0 — 单模型多 Agent 项目脚手架"
    )
    parser.add_argument("--target", required=True, help="目标目录路径")
    parser.add_argument("--project-name", required=True, help="项目名称（中英文均可）")
    parser.add_argument(
        "--path-mode",
        choices=["zero-to-one", "design-driven"],
        required=True,
        help="交付路径：zero-to-one（0-1 追问）或 design-driven（设计驱动）",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="允许向非空目录写入（不会删除已有文件）",
    )
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()

    if root.exists() and any(root.iterdir()):
        if not args.merge:
            print(
                f"[error] 目标目录不为空：{root}\n"
                f"        使用 --merge 向已有目录写入，或选择新目录。"
            )
            raise SystemExit(1)

    root.mkdir(parents=True, exist_ok=True)

    # ── 顶层治理文件 ────────────────────────────────────────────────────────
    write(root / "AGENTS.md", make_agents_md(args.project_name))
    write(root / "LEARNINGS.md", make_learnings_md())

    # ── agent-context/ ────────────────────────────────────────────────────
    write(root / "agent-context/current-workflow.md", make_current_workflow(args.path_mode))
    # v3.2：全路径生成，不再按 path-mode 条件分流
    write(root / "agent-context/design-role-rules.md", make_design_role_rules())

    # ── skills/（7 个核心 Skill）─────────────────────────────────────────
    write(root / "skills/design-analysis/SKILL.md", SKILL_DESIGN_ANALYSIS)
    write(root / "skills/requirements-refinement/SKILL.md", SKILL_REQUIREMENTS_REFINEMENT)
    write(root / "skills/systematic-debugging/SKILL.md", SKILL_SYSTEMATIC_DEBUGGING)
    write(root / "skills/writing-plans/SKILL.md", SKILL_WRITING_PLANS)
    write(root / "skills/brainstorming/SKILL.md", SKILL_BRAINSTORMING)
    write(root / "skills/two-stage-review/SKILL.md", SKILL_TWO_STAGE_REVIEW)
    write(root / "skills/architecture-check/SKILL.md", SKILL_ARCHITECTURE_CHECK)

    # v3.2：style-foundation 全路径生成（从 skill 安装目录复制）
    _copy_style_foundation(root)

    # ── project-management/ ───────────────────────────────────────────────
    write(root / "project-management/prd-registry.md", make_prd_registry(args.project_name))
    write(root / "project-management/active-sprint.md", make_active_sprint(args.project_name))
    write(root / "project-management/backlog.md", make_backlog())
    write(root / "project-management/changelog.md", make_changelog())
    write(root / "project-management/decision-log.md", make_decision_log())

    # ── docs/product/ ─────────────────────────────────────────────────────
    write(root / "docs/product/README.md", make_docs_product_readme())

    # ── 部署忽略文件 ───────────────────────────────────────────────────────
    write(root / ".vercelignore", make_vercelignore())
    write(root / ".dockerignore", make_dockerignore())

    # ── tasks/ ────────────────────────────────────────────────────────────
    write(root / "tasks/prd/PRD-001-mvp.md", make_prd_001(args.project_name, args.path_mode))
    write(root / "tasks/knowledge/lessons.md", make_lessons())

    # ── 输出结果 ──────────────────────────────────────────────────────────
    result = {
        "target": str(root),
        "project_name": args.project_name,
        "path_mode": args.path_mode,
        "status": "ok",
        "generated": {
            "governance": ["AGENTS.md", "LEARNINGS.md"],
            "agent_context": [
                "current-workflow.md",
                "design-role-rules.md",  # v3.2: 全路径生成
            ],
            "skills": [
                "design-analysis",
                "style-foundation",  # v3.2: 全路径生成
                "requirements-refinement",
                "systematic-debugging",
                "writing-plans",
                "brainstorming",
                "two-stage-review",
                "architecture-check",
            ],
            "project_management": [
                "prd-registry.md",
                "active-sprint.md",
                "backlog.md",
                "changelog.md",
                "decision-log.md",
            ],
            "tasks": ["prd/PRD-001-mvp.md", "knowledge/lessons.md"],
            "docs": ["product/README.md"],
            "deploy_config": [".vercelignore", ".dockerignore"],
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # ── 启动引导 ──────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print(f"  项目已初始化：{args.project_name}")
    print("=" * 60)
    print()
    print("下一步：在 Codewiz 中打开此项目目录，开始对话。")
    print()
    if args.path_mode == "zero-to-one":
        print("【0-1 路径】Codewiz 将逐步追问（最多 6 个问题）来生成 PRD-001。")
        print("  问完后输出 PRD 草稿，确认后进入实现阶段。")
    else:
        print("【设计驱动路径】提供 Figma 链接，Codewiz 将触发 design-analysis Phase-1。")
        print("  分析完成后生成 PRD-001 的设计规格区块。")
    print()
    print("会话启动时，Codewiz 会自动读取：")
    print("  1. AGENTS.md")
    print("  2. agent-context/current-workflow.md")
    print("  3. project-management/prd-registry.md")
    print("  4. LEARNINGS.md")
    print()


if __name__ == "__main__":
    main()
