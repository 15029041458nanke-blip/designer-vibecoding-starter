# Template Map

> 本文件是 SKILL.md 的执行参考，规定了具体的问题措辞、路径分支和 scaffold 行为。

---

## 路径判断问题（仅此一问）

```
你想用哪种方式开始？

A) 我有 Figma 设计稿（链接或文件）→ 设计驱动路径
B) 我还没有设计稿，从产品想法开始描述 → 0-1 路径

（也可以直接粘贴 Figma 链接，我来判断）
```

---

## 0-1 路径问题清单（逐步追问，一次一问）

| # | 问题 | 记录变量 |
|---|------|---------|
| 1 | `你想构建的是什么？用一句话描述你的产品/应用。` | `product_goal` |
| 2 | `好的，「[产品名]」的主要用户是谁？他们现在是怎么解决这个问题的？` | `target_user` + `current_pain` |
| 3 | `你的产品比现有方案好在哪里？最核心的差异点是什么？` | `core_value` |
| 4 | `如果只做 3 个核心功能来验证这个想法，你会选哪 3 个？（3 个是上限）` | `mvp_features[]` |
| 5 | `技术栈有偏好吗？没有的话我来推荐。` | `tech_stack`（可为空） |
| 6 | `界面风格有倾向吗？A)发参考截图 B)发URL C)文字描述 D)跳过` | `design_style` / `has_constitution` |

**问题 6 分流规则**：
- 用户选 A/B（提供参考图或 URL）→ 触发 `style-foundation` Skill → 生成 `docs/style-constitution.md` → `has_constitution = true`
- 用户选 C（丰富文字描述，≥2 维度）→ 触发 `style-foundation` Mode B → 生成 Constitution → `has_constitution = true`
- 用户选 C（简单关键词）→ 记录 `design_style` → `has_constitution = false`
- 用户选 D（跳过）→ `design_style = ""` → `has_constitution = false`

Constitution 生成完成后（或跳过后）→ 生成 PRD 草稿 → 用户确认

**问题顺序规则**：
- 必须按序，不可跳问
- 问题 5 和 6 可选，用户明确跳过时记为空
- 等收到明确答案后再问下一题，不催促
- 问题 6 如果触发 style-foundation，该 Skill 内部的追问（情感目标、反参考等）按 style-foundation 流程执行，完成后回到 starter 流程继续

---

## 设计驱动路径问题清单

| 步骤 | 行为 |
|------|------|
| 收到 Figma 链接 | 调用 Figma MCP 拉取顶层结构 |
| 判断场景 A/B/C | 见 SKILL.md Phase 1B |
| 逐一消除设计疑点 | 一次一个问题，等待确认 |
| 输出设计分析包 | 作为 PRD 的设计规格区块 |

**如果同时提供了文字 PRD + 设计稿（场景 B）**，需要：
```
1. 读产品 PRD，提取功能清单
2. 拉取设计稿，提取设计侧功能点
3. 对照产出三类结论：
   - ✅ 一致项：直接写入 AC
   - ⚠️ 设计稿有、PRD 未提及：逐一询问用户
   - ❗ PRD 有、设计稿未覆盖：标注风险
4. 确认后输出完整 PRD
```

---

## 首个 PRD 模板

```markdown
# PRD-001: [产品/功能名称]

> 状态: queued
> 优先级: P0
> 设计稿: [Figma 链接] 或 "无"
> 依赖: 无

---

## 1. User Story
作为 [target_user]，我想要 [product_goal]，以便 [core_value]。

## 2. 功能范围
### 包含
- [mvp_feature_1]
- [mvp_feature_2]
- [mvp_feature_3]

### 不包含（Out of Scope）
- [推断的不包含项 1]
- [推断的不包含项 2]

## 3. 设计规格
（design-driven 路径填充；0-1 路径留空，后续有设计稿时补充）

## 4. Acceptance Criteria
- AC-1: 当 [条件] 时，[行为] → [可观察结果]
- AC-2: ...
- AC-3: （边界/错误场景）...

## 5. 实现任务拆解
（由 writing-plans Skill 输出后填入）
| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 1 | ... | ⬜ pending | - |
| N | Design QA | ⬜ pending | 最后一步 |
```

---

## Scaffold 生成的文件列表

> vibecoding 项目包含三类文件，**只有应用代码层进入生产环境**。
> 另外两层集中在可枚举的目录下，由 `.vercelignore` / `.dockerignore` 统一排除。

### 三层架构总览

```
项目根目录
│
├── [应用代码层] ← 唯一进入生产的层
│   src/  public/  index.html  package.json  vite.config.ts ...
│
├── [AI 协作层] ← 开发时工具，.vercelignore 排除
│   AGENTS.md  LEARNINGS.md  skills/  agent-context/
│
├── [需求追踪层] ← 开发过程文档，.vercelignore 排除
│   tasks/prd/  project-management/
│
└── [产品规范层] ← 工程师参考，不部署但保留在 git
    docs/product/
```

### 所有路径共用

**应用代码层**（由 Phase 2B 生成，进入生产）

| 文件/目录 | 说明 |
|---------|------|
| `src/` | React 应用源码 |
| `public/` | 静态资源 |
| `index.html` `package.json` `vite.config.ts` 等 | 构建配置 |

**AI 协作层**（.vercelignore 排除，不进入生产）

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | AI 协作规则总入口（只放 AI 工具读取的规则） |
| `LEARNINGS.md` | 经验教训（空模板） |
| `agent-context/current-workflow.md` | 单模型多 Agent 启动协议 |
| `skills/design-analysis/SKILL.md` | 设计分析 Skill |
| `skills/style-foundation/SKILL.md` | 风格基石 Skill（参考图→风格宪法） |
| `skills/requirements-refinement/SKILL.md` | 需求精化 Skill |
| `skills/systematic-debugging/SKILL.md` | Debug 四阶段 Skill |
| `skills/writing-plans/SKILL.md` | Plan 写作规范 Skill |
| `skills/brainstorming/SKILL.md` | 需求探索 Skill |
| `skills/two-stage-review/SKILL.md` | 两阶段 Review Skill |
| `skills/architecture-check/SKILL.md` | 架构检查 Skill |

**需求追踪层**（.vercelignore 排除，不进入生产）

| 文件 | 说明 |
|------|------|
| `project-management/prd-registry.md` | PRD 主控（含 PRD-001 已注册） |
| `project-management/backlog.md` | 想法池模板 |
| `project-management/changelog.md` | 变更记录模板 |
| `project-management/decision-log.md` | 决策记录模板 |
| `project-management/active-sprint.md` | Sprint 模板 |
| `tasks/prd/PRD-001-*.md` | 第一个 PRD（从对话生成） |
| `tasks/knowledge/lessons.md` | 经验教训模板 |

**产品规范层**（不部署，但保留在 git）

| 文件 | 说明 |
|------|------|
| `docs/product/README.md` | 产品规范目录入口（工程师实现依据） |
| `docs/style-constitution.md` | 风格宪法（由 style-foundation Skill 生成，仅 0-1 路径有参考图时） |

**部署配置**

| 文件 | 说明 |
|------|------|
| `.vercelignore` | Vercel 部署忽略（排除 AI 协作层 + 需求追踪层） |
| `.dockerignore` | Docker 部署忽略（有后端服务时使用） |

### 仅 design-driven 路径额外生成

| 文件 | 说明 |
|------|------|
| `agent-context/design-role-rules.md` | Figma→CSS 详细还原规则库（411 行实战沉淀） |

### 不再生成（已废弃）

```
❌ .agent/             旧 Codex 编排目录（不需要）
❌ ai-workflows/        旧双模型工作流（不需要）
❌ current-docs/        旧导航层（不需要）
❌ scripts/openclaw_*   OpenClaw 后台执行（不需要）
❌ scripts/validate_handoff.sh  handoff 校验（不需要）
❌ scripts/agent_run.sh         旧 Codex 运行脚本（不需要）
```

---

## 信息归属原则（⚠️ 必读，防止踩坑）

**核心判断问题**：这条信息是给 AI agent 看的，还是给工程师/产品看的？

| 信息类型 | 放在哪里 | 原因 |
|---------|---------|------|
| AI 协作规则（角色分工、DoD、review 流程） | `AGENTS.md` / `skills/` | AI 工具读取上下文，不随产品交付 |
| 产品交互行为规范（菜单关闭机制、颜色规则等） | `docs/product/` | 工程师实现依据，随代码库长期存在 |
| PRD 和 Acceptance Criteria | `tasks/prd/` | 需求文档，AI 上下文 + 产品记录，保留在代码库 |
| 开发经验教训 | `LEARNINGS.md` / `tasks/knowledge/` | 两类人都有用，保留在代码库 |

**禁止行为**：
```
❌ 把产品交互规则写进 AGENTS.md
   → 问题：规则消失于部署流程，只在 AI 上下文里，工程师看不到
❌ 把 AI 协作流程写进 docs/product/
   → 问题：产品文档里混入工程脏话，信噪比下降
```

**正确做法**：
```
✅ AGENTS.md 里只有"产品规范放在 docs/product/ 下，按 §N 查阅"的引用指针
✅ docs/product/ 里有实际的规范正文，工程师不需要 AI 工具也能读懂
✅ 每次发现新的产品行为规则，先问"这是 AI 配置还是产品规范？"
   → AI配置 → AGENTS.md
   → 产品规范 → docs/product/ 新建或追加 .md 文件
```

**`docs/product/README.md` 模板内容**：

```markdown
# Product Specs

> 产品行为规范文档目录。以下规范是工程师实现功能的权威依据，
> 与代码库共同演进，不依赖 AI 工具即可阅读。

## 规范列表

| 文件 | 内容 |
|------|------|
| `interaction-spec.md` | 全局交互规范（菜单关闭机制、节点颜色规则等） |

## 如何添加新规范

1. 在本目录新建 `<feature>-spec.md`
2. 在本 README 的规范列表中添加索引条目
3. 在 `AGENTS.md` 第 10 章的引用表格里加一行指向新文件
```

---

## 路径分支行为对比

| 特性 | 0-1 路径（无参考图） | 0-1 路径（有参考图） | 设计驱动路径 |
|------|---------|---------|------------|
| 启动问题数 | 6 个（逐步） | 6 个 + style-foundation 追问 | 1 个（Figma 链接） |
| 风格定义 | `design_style` 字符串 | 完整风格宪法 | design-analysis 提取 |
| 首个 PRD 来源 | 追问对话生成 | 追问对话生成 | design-analysis Phase-1 转化 |
| PRD 设计规格区块 | 空（后续可补） | 风格宪法引用 | 由 Figma 数据填充 |
| 设计 Token 来源 | 硬编码基础值 | Constitution Token 草案 | 设计分析包提取 |
| 后续 QA 阶段 | two-stage-review | two-stage-review + 风格守护 | two-stage-review + design-analysis Phase-2 |
| style-constitution.md | 不生成 | 生成 | 不生成（有设计稿） |
| design-role-rules.md | 不生成 | 不生成 | 生成 |
| 适合场景 | 快速验证、无设计资源 | 有审美方向、想要高质量 UI | 设计稿还原、UI 精度要求高 |

---

_更新：2026-04-01 v3.1 — 新增 style-foundation 集成、Constitution 驱动 Token 生成、0-1 路径参考图分流_
