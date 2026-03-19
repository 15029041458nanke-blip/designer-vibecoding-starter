# Working Spec

这份文档是 `designer-vibecoding-starter` 的唯一事实源。

目标不是继续写散的建议，而是让 Codex 和 Claude 围绕同一份规格协作，把这个 skill 打磨成一个真正可用、可发布、可复用的项目初始化器。

---

## 1. 最终目标

这个 skill 被调用时，应该能够：

1. 引导用户回答最少但关键的初始化问题
2. 根据答案为用户生成一个完整的项目文件夹骨架
3. 支持两种开发路径：
   - `zero-to-one`
   - `design-driven`
4. 支持两种默认协作模式：
   - `claude-planner-codex-builder`
   - `codex-fullstack-workflow`
5. 可选接入 `OpenClaw`
6. 初始化完成后，用户可以直接按这套协作模式开始工作，而不是只得到一堆静态文档

---

## 1.1 为什么要做这个 skill

这个 skill 不是为了生成一个“泛用项目模板”，而是为了把我们已经在真实项目里跑过的一套设计师 vibecoding 方法，沉淀成一个可以被别人一键拿走、直接开始工作的初始化器。

这个方法的核心不是“AI 帮你写代码”，而是：

- 设计师如何从 0 到 1 启动项目
- 如何把需求、设计输入、协作模式和执行入口一次性配好
- 如何避免上下文混乱、角色打架、文档散落、状态丢失

换句话说，这个 skill 最终要交付的是一套“设计师能直接开始 vibecoding 的项目操作系统”。

---

## 1.2 这个 skill 要服务的典型场景

它至少要覆盖这几种典型启动方式：

1. 用户只有一个产品想法，没有设计稿
2. 用户已经有设计稿，希望直接按设计驱动方式启动项目
3. 用户希望 Claude 负责规划、Codex 负责执行
4. 用户希望默认走 Codex 多角色链路
5. 用户希望任务可以在后台继续跑，不用一直盯着窗口

它不能只适合其中一个场景，而是必须把这些选择在初始化阶段说明白。

---

## 2. 不可退化约束

以下约束不能被优化掉：

### 2.1 不能伪造完成状态

- `agent_run.sh` 不能在没有执行真实命令的情况下直接把状态写成 `done`
- 如果仍是占位实现，至少要明确失败、待配置，或显式停在非完成状态

### 2.2 不能污染已有目录

- 初始化脚本遇到已有目录时，必须有保护策略
- 不能默认往已有目录里静默覆盖文件
- 至少要支持：
  - 明确确认 merge
  - 或自动创建子目录

### 2.3 中文切换不能退化成演示

- `workflow_intent.sh` 不能只返回一个 JSON 样例
- 它至少要保留“识别当前意图并产出可用结果”的能力
- 理想状态下，保留我们最早那版对：
  - `Claude/Codex`
  - `有设计稿/没设计稿`
  - `OpenClaw/后台/远程`
  的识别逻辑

### 2.4 skill 要保留正式形态

- 不要随便删除 `agents/openai.yaml`
- 如果要删，必须先证明不会影响 UI 展示、技能发现、默认 prompt 和后续集成
- 默认倾向：保留

### 2.5 初始化结果要能开始工作

生成后的项目不能只是“文档模板集合”，还必须至少具备：

- `AGENTS.md`
- `agent-context/current-workflow.md`
- `.agent/handoff.json`
- `.agent/status.json`
- `scripts/agent_run.sh`
- `scripts/validate_handoff.sh`
- `tasks/todo.md`
- `project-management/active-sprint.md`

### 2.6 不能丢掉产品化目标

这个 skill 的目标不是“给用户一份说明书”，而是“给用户一个已经配置好的起点”。

所以任何优化如果导致下面这些事情退化，都不能接受：

- 用户还要自己猜应该用哪条链路
- 用户还要自己补出关键目录结构
- 用户还要自己设计中文切换口令
- 用户拿到模板后还不能直接开始第一轮 handoff / 执行

---

## 2.7 中文意图切换很重要

中文意图切换不是锦上添花，而是这个模板产品体验的一部分。

原因有 3 个：

1. 真实用户不会总是记住具体命令
2. 协作模式切换本来就是高频动作
3. 设计师更自然的使用方式就是直接说“跟我用 Codex 协作链路”“切换到 Claude 规划 + Codex 开发”“开启 OpenClaw 后台执行”

所以：

- `workflow_intent.sh` 不能退化成只返回一个示例 JSON
- 它至少要保留“中文意图 -> 协作模式判断”的实际价值

---

## 2.8 三条链路必须被产品化理解

这个 skill 初始化出来的项目，必须明确体现下面三条链路：

### 链路 A：Claude Code + Codex

适用于：

- Claude 配额还在
- 任务复杂、上下文长
- 希望把规划和执行拆开

### 链路 B：Codex 全流程 / 多角色

适用于：

- 希望在一个环境里完成产品、架构、开发、测试、review
- Claude 配额用光，或者本来就想默认走 Codex

### 链路 C：OpenClaw 后台执行

适用于：

- 需要远程/后台工作
- 不想一直盯着窗口

注意：

- C 不是替代 A/B，而是叠加层
- skill 初始化后的文件和文案必须把这一点表达清楚

---

## 2.9 两条开发路径必须是初始化阶段就选清楚的

### 路径 1：zero-to-one

用于：

- 没有设计稿
- 从意图 -> 产品规划 -> PRD -> handoff 开始

这一条路径里不应默认强制要求：

- 设计分析
- 设计合同
- 设计 QA

### 路径 2：design-driven

用于：

- 已有设计稿
- 需要设计分析 -> 设计转 PRD -> 产品校验 -> 开发 -> Design QA

这一条路径里应默认生成并强调：

- `docs/design/figma-source.md`
- `docs/design/design-analysis.md`
- `docs/design/design-contract.md`
- `docs/design/design-qa.md`

---

## 3. 当前已确认方向

这些方向可以继续保留：

1. `SKILL.md` 增加中文触发词
2. 日期从硬编码改为动态生成
3. 路径和协作模式仍然维持：
   - `zero-to-one`
   - `design-driven`
   - `claude-planner-codex-builder`
   - `codex-fullstack-workflow`
   - optional `OpenClaw`

4. skill 应该优先通过“少量关键问题”完成初始化，而不是变成一个长问卷

---

## 3.1 理想初始化结果

理想情况下，skill 运行完后，用户应该拿到一个像这样的项目骨架：

- `AGENTS.md`
- `agent-context/`
- `ai-workflows/`
- `docs/project-entry/`
- `docs/workflows/`
- `docs/product/`
- `docs/design/`
- `project-management/`
- `tasks/`
- `scripts/`
- `.agent/`
- `package.json`

并且这些文件不是空摆设，而是能支持：

- 看规则
- 看当前 workflow
- 写第一轮 todo
- 填第一份 handoff
- 跑第一轮执行

---

## 3.2 初始化后用户应该怎么开始

skill 运行结束后，理想的引导顺序应该是：

1. 打开 `AGENTS.md`
2. 打开 `agent-context/current-workflow.md`
3. 打开 `project-management/active-sprint.md`
4. 填 `tasks/todo.md`
5. 填 `.agent/handoff.json`
6. 运行：
   - `npm run workflow:intent`
   - `npm run agent:run`
   - 如果启用了 OpenClaw，再运行 `npm run openclaw:worker` 或 `npm run openclaw:daemon`

---

## 4. 当前待修问题

截至本轮 review，以下问题仍待处理：

1. `agent_run.sh` 仍会伪造完成状态
2. 初始化脚本缺少“已有目录保护”
3. `workflow_intent.sh` 被过度简化
4. `agents/openai.yaml` 被删除，不建议直接接受

---

## 4.1 对 Claude 优化的评判标准

Claude 后续的每一轮优化，都应该用下面这几个问题来判断是否真的更好：

1. 有没有更接近“一键初始化后可直接工作”
2. 有没有削弱实际执行能力
3. 有没有把本来产品化的体验又变回说明文档
4. 有没有让 skill 更容易被中文用户正确触发
5. 有没有让后续发布形态更完整，而不是更随意

---

## 5. Claude / Codex 协作规则

### Claude 负责

- 按 skill 最佳实践审查结构和触发词
- 优化 `SKILL.md`
- 优化 skill 的使用引导、提问顺序和文档口径
- 提出脚本层面的修改建议

### Codex 负责

- 审查是否偏离项目真实需求
- 判断是否影响“初始化后可直接工作”的目标
- 修改脚本、模板和验证逻辑
- 对 Claude 的优化做最终技术 review

### 双方共同遵守

- 所有关键结论先写进本文件
- 每轮改动必须更新 `CHANGE_REPORT.md`
- 不要在没有写明理由的情况下删文件、降级能力或改变目标

---

## 5.1 最终发布形态

这个 skill 的理想终态不是只留在本地目录里，而是：

1. 先在本地验证通过
2. 再整理成一个独立 skill 仓库
3. 最终能被别人通过安装命令直接使用

所以在设计这个 skill 时，要默认它未来是一个正式发布物，而不是一次性的内部实验脚本。

---

## 6. 每轮协作输出要求

每一轮修改后，必须同步更新：

1. `CHANGE_REPORT.md`
2. 如有新结论，更新 `WORKING_SPEC.md`

`CHANGE_REPORT.md` 至少要写清楚：

- 改了什么
- 为什么改
- 风险是什么
- 是否影响初始化后可直接工作的目标
- 需要对方重点复核什么

---

## 7. 下一轮重点

Claude 下一轮复核时，请重点看这 4 件事：

1. 如何在不牺牲简洁度的前提下，修回 `workflow_intent.sh` 的可用能力
2. 如何给初始化脚本补上"已有目录保护"
3. 如何处理 `agent_run.sh` 的占位状态，避免伪完成
4. 是否应恢复 `agents/openai.yaml`

---

## 8. design-driven 路径：设计还原规则沉淀（Round 5 新增）

### 8.1 背景

在真实的 design-driven 项目（vibcoding 思维导图）中，经过多轮 Figma → 代码还原与质检，我们总结出了一套系统性的设计还原规则，适用于 `design-analyst` → `engineer` → `reviewer` 的完整链路。

这套规则已在项目内落地为 `agent-context/design-role-rules.md`（v1.8），并验证有效。

### 8.2 核心规则分类（共 7 类）

| 类别 | 核心内容 | 典型陷阱 |
|------|---------|---------|
| §1 图标规则 | IMAGE-SVG 节点禁止用文字或自绘替代，统一用 `IconPlaceholder`（20px容器+18px圆+1.5px描边） | 凭语义自造图标内容 |
| §2 Border 规则 | Inside stroke → CSS border-box；含 fill 子元素的结构性容器用 `outline` 不用 `border` | border-box 压缩 fill 子元素内容区 |
| §3 尺寸规则 | sizing 类型（hug/fixed/fill）必须从 Component Set 直接读取，不能从使用侧推断 | 从父容器使用侧推断 fill/fixed |
| §4 节点类型识别 | 实现前必须查 Figma 节点 `type` 字段，`TEXT` 才用文字，其余用 IconPlaceholder | 未查 type 凭语义猜 |
| §5 布局对齐 | Auto Layout：MCP 直接返回 `alignItems`/`justifyContent`；绝对定位：只返回 `locationRelativeToParent {x,y}`，需手动判断居中意图 | 字面翻译绝对定位坐标为 top/left |
| §6 组件系统 | 变体必须从 Component Set 顶层节点枚举，不能从使用侧实例读取 | 从使用侧实例读取，遗漏变体 |
| §7 QA 清单 | 逐层走查：图标→尺寸→border→布局→变体→token | 局部验证遗漏系统性问题 |

### 8.3 关键发现：Figma MCP 对齐数据机制

Figma MCP **会**返回对齐属性，但分两类：

- **Auto Layout 子元素**：直接返回 `alignItems` / `justifyContent` / `alignSelf`，可直接映射 CSS flex 属性
- **绝对定位元素**（`position: absolute`）：只返回 `locationRelativeToParent: {x, y}`，无对齐标签，需手动判断：
  - 若 `x == (父宽-子宽)/2` 且 `y == (父高-子高)/2` → 居中意图 → `inset: 0 + flex 双轴居中`
  - 否则 → 真实偏移 → `top/left`（须加父容器 border 宽度修正）

### 8.4 design-driven 项目生成物标准

skill 初始化 `design-driven` 路径时，除原有设计文件外，应额外生成：

```
agent-context/
  design-role-rules.md   ← 设计还原规则手册（新增生成物）
```

该文件包含以下章节的初始框架（空模板），供团队在项目中迭代填充：
- §1 图标规则
- §2 Border 规则
- §3 尺寸规则
- §4 节点类型识别
- §5 布局对齐规则（含 MCP 数据机制说明）
- §6 组件系统规则
- §7 QA 走查清单
- §CHANGELOG

### 8.5 还原质量目标

| 阶段 | 目标 |
|------|------|
| 第一稿还原 | > 80% 精准还原（基于完整规则手册） |
| 质检修复 | 平均每轮 QA 发现问题 < 5 个 |
| 规则迭代 | 每发现新典型问题 → 立即追加规则案例并更新 CHANGELOG |

### 8.6 不可退化约束

- `design-role-rules.md` 不能是纯描述文档，必须包含可执行的走查清单（§7）
- 规则必须有触发案例支撑（无案例的规则不算有效规则）
- 新项目初始化时生成的是"空白模板框架"，不是已填充内容——填充由 design-analyst 角色在项目启动时完成
