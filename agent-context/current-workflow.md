# Current Workflow

workflow_id: single-model-multi-agent
updated_at: 2026-03-26
owner: codewiz

## 协作模式

**单模型多 Agent**：Codewiz 是唯一主导，通过 `new_task` 派发子 agent，不跨模型协作。
- Codewiz = 规划 + 编排 + review（主 agent）
- 子 agent = 执行单一 task，隔离上下文（不继承对话历史）

---

## 会话启动必读顺序

```
1. /AGENTS.md                                  ← 最高优先级规则
2. /agent-context/current-workflow.md          ← 本文件
3. /project-management/prd-registry.md         ← 找到当前 Active PRD 和待做任务
4. /LEARNINGS.md                               ← 历史经验教训（防止重复犯错）
```

读完 prd-registry.md 后，告知用户：
> 「当前 Active PRD 是 [XXX]，下一步是 [task]，确认开始？」

---

## 核心规则入口

| 场景 | 对应 Skill | 不触发的后果 |
|------|-----------|-------------|
| 输入有 Figma 链接 / 设计稿 | `skills/design-analysis` Phase-1 | 禁止直接写 Plan |
| 任何 UI 任务完成前 | `skills/design-analysis` Phase-2 | 不算完成 |
| 需求不清 / PRD 缺 AC | `skills/requirements-refinement` | 禁止进入拆任务 |
| 任何 bug / 失败 | `skills/systematic-debugging` | 禁止直接提 fix |
| 中/大任务写实现计划 | `skills/writing-plans` | 禁止直接写代码 |
| 大任务需求不清晰 | `skills/brainstorming` | 禁止直接写 spec |
| 每个 task 完成后 | `skills/two-stage-review` | 不算完成 |
| 架构变更前 | `skills/architecture-check` | 禁止动手 |

---

## 设计稿输入场景判断

拿到设计稿后，先判断场景再行动：

```
场景 A（大型设计稿，多功能）→ 拆分为多个 PRD，逐一入队
场景 B（产品 PRD + 设计稿同时提供）→ 对照对齐，产出完整 PRD
场景 C（单组件/小模块）→ 检查 prd-registry，已有 PRD 则补充，否则新建
```

详见：`AGENTS.md` Section 14 / `skills/design-analysis/SKILL.md`

---

## 已废弃

以下工作流文件保留为历史参考，核心角色定义已升级为 Skills：
- `ai-workflows/codex-fullstack-workflow/`（多模型协作，已废弃）
- `ai-workflows/claude-planner-codex-builder/`（角色定义参考源，已升级为 Skills）
  - 原 `agent-roles.md` 的 7 个角色 → 见 `AGENTS.md` Section 1.5 对照表
