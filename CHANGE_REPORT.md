# Change Report

这个文件用于 Claude 和 Codex 之间的回合制协作记录。

每一轮修改后追加一节，保留历史记录。

---

## Round 5 — 2026-03-19（Claude 执行）

### 本轮目标

在真实 design-driven 项目（vibcoding 思维导图）的多轮 Figma → 代码还原与质检中，我们总结出了一套完整的设计还原规则体系（v1.8），并验证有效。本轮目标：将这套规则沉淀进 skill，使未来所有 design-driven 项目都能从第一稿开始受益。

### 改动清单

| 文件 | 改动内容 |
|------|---------|
| `WORKING_SPEC.md` | 新增 §8「design-driven 路径：设计还原规则沉淀」，含7类规则分类表、Figma MCP 对齐数据机制、生成物标准、质量目标和不可退化约束 |
| `scripts/init_designer_vibecoding_project.py` | 新增 `make_design_role_rules()` 函数，生成包含7个章节框架 + QA 清单 + CHANGELOG 的初始模板；`main()` 中 `design-driven` 路径下自动写入 `agent-context/design-role-rules.md` |

### 规则体系核心内容（7类）

| 类别 | 核心规则 | 典型根因 |
|------|---------|---------|
| §1 图标 | IMAGE-SVG → IconPlaceholder，禁止文字/自绘 | 未查节点 type |
| §2 Border | Inside stroke → border-box；fill子元素容器 → outline | border-box 压缩 fill 内容区 |
| §3 尺寸 | sizing 必须从 Component Set 直接读取 | 从使用侧推断 |
| §4 节点类型 | 实现前必须查 Figma 节点 type 字段 | 凭语义猜 |
| §5 布局对齐 | Auto Layout → MCP 直接给 align；绝对定位 → 只给坐标，需手动判断居中意图 | 字面翻译 x/y 坐标 |
| §6 组件系统 | 变体从 Component Set 顶层枚举 | 从使用侧实例读取遗漏变体 |
| §7 QA 清单 | 逐层走查（图标→尺寸→border→布局→变体） | 局部验证遗漏系统性问题 |

### 关键新增发现（v1.8）

**Figma MCP 对齐数据返回机制**：
- Auto Layout 子元素：直接返回 `alignItems` / `justifyContent` / `alignSelf`，可直接映射 CSS
- 绝对定位元素：只返回 `locationRelativeToParent: {x, y}`，无对齐标签，需手动判断是否居中意图

### 改动原因

- 在 vibcoding 思维导图项目中，通过6个典型 bug 的根因分析和修复，形成了可复用的规则体系
- design-driven 路径的核心价值不只是"有设计稿"，还需要有系统性的还原规则保障还原质量
- skill 的 `design-driven` 路径现在应该默认包含 `design-role-rules.md` 框架，而非让团队从零开始摸索

### 风险与影响

- 无能力削减：新增生成物（`design-role-rules.md`）是可选的模板框架，不影响现有流程
- 生成的 `design-role-rules.md` 是空白框架（典型案例处留占位符），由 design-analyst 在项目启动时填充，避免"强塞内容"
- `zero-to-one` 路径不受影响，不会生成该文件

### 需要 Codex 复核的点

1. `make_design_role_rules()` 函数中 `{x, y}` 占位符是否在 f-string 中需要转义（已用字符串拼接规避）
2. `agent-context/default-context.md` 是否应在 design-driven 路径中引用 `design-role-rules.md`（当前版本未引用，可作为下一轮迭代）
3. 是否应在 `AGENTS.md` 的 `Must-Read Order` 中加入 `design-role-rules.md`（design-driven 路径）

---

## Round 4 — 2026-03-18（Claude 执行）

### 本轮目标

Codex 已对 `ai-workflows/claude-planner-codex-builder/` 下的协作文档做了重要升级，引入了完整角色团队（design-analyst / product-strategist / project-manager / architect / engineer / reviewer / tester），将原来的"Claude 规划 / Codex 执行"简化版升级为"完整角色团队 + 双模型分工版"。

本轮目标：将 skill 的所有面向用户的描述文件对齐到这一最新版本，消除"Chain A 只有简单规划/执行两层"的误解，补入 design-analyst 在 design-driven 路径中的核心位置。

### 改动清单

| 文件 | 改动内容 |
|------|---------|
| `presentations/designer-vibecoding-share/skill-landing.html` | 1) Hero 模式卡片：补充"完整角色团队 + 双模型分工"表述<br>2) Chain A 描述：列出 Claude 侧五个规划角色 + Codex 侧两个执行角色<br>3) Chain B 描述：明确"同一套完整角色团队，由 Codex 单模型串联驱动"<br>4) Design Driven 路径步骤：补入 design-analyst 作为第一步，四步完整流程<br>5) Footer：更新为 Round 4 |
| `skills/designer-vibecoding-starter/SKILL.md` | 1) 模式描述补全角色列表：明确 Claude 侧和 Codex 侧各自负责哪些角色<br>2) Guidance 补充：两种模式共享完整角色团队，差别只是模型分工；design-driven 时 design-analyst 必须是第一个角色 |
| `skills/designer-vibecoding-starter/references/template-map.md` | 1) 问题 3 选项描述补全角色列表<br>2) 推荐措辞补充角色分工说明<br>3) Mode-specific behavior 两个模式均补入完整角色职责说明 |
| `~/.agents/skills/designer-vibecoding-starter/SKILL.md` | 同步本地安装版 |
| `~/.agents/skills/designer-vibecoding-starter/references/template-map.md` | 同步本地安装版 |

### 改动原因

- 根本原因：`agent-roles.md` 升级后，`claude-planner-codex-builder` 不再是双角色简化版，而是"完整角色团队 + 双模型分工版"。skill 的描述文件没有跟进，会让用户误以为 Chain A 没有 design-analyst 等角色。
- design-analyst 是设计驱动链路最关键的差异点，之前在落地页和 SKILL.md 完全缺失。
- Chain A 和 Chain B 的本质区别不是"有没有完整角色"，而是"由哪个模型驱动"，这一点原来没有表达清楚。

### 风险与影响

- 无能力削减：本轮只是描述层更新，不影响脚手架生成逻辑、执行脚本或 handoff 结构。
- 无 WORKING_SPEC 偏离：所有改动都在补充角色信息，未改变路径/模式/OpenClaw 的选择结构。
- 使用门槛：角色列表的引入会让描述更详细，可能对新用户有一定信息量，但准确性优先于简洁性。

### 需要 Codex 复核的点

1. `init_designer_vibecoding_project.py` 生成的 `ai-workflows/claude-planner-codex-builder/agent-roles.md` 是否已同步最新完整角色内容（尤其是 design-analyst、product-strategist）？
2. 生成的 `current-workflow.md` 的模式说明是否也更新为"完整角色团队"表述？
3. 是否需要在 WORKING_SPEC.md Section 5 补入最新角色边界说明？

---

## Round 1-3（历史记录）

- Round 3：落地页 skill-landing.html 重构为分享 PPT 专题网页，完整呈现协作链路与模板产物
- Round 2：脚手架稳定性修复（--merge 目录保护、中文意图识别、pending-config 初始化状态）
- Round 1：初始版本建立，确立 WORKING_SPEC.md + CHANGE_REPORT.md 协作机制
