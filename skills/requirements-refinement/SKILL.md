# Skill: requirements-refinement

> 本 Skill 对应原 `product-strategist` + `project-manager` 角色的规划侧职责。
> 目标：确保每个进入开发的需求都满足 Definition of Ready（DoR），避免"模糊需求驱动开发"。

---

## 触发条件

| 场景 | 说明 |
|---|---|
| 用户提出新功能，描述不够具体（缺少 AC/范围/角色） | 必须先过 DoR，再进入 brainstorming 或 writing-plans |
| 现有 PRD 缺少 Acceptance Criteria | 补充 AC 后才允许进入开发 |
| 任务卡在 `NEEDS_CONTEXT` 状态 | 检查是否是需求未澄清导致的 |
| 新需求与现有 PRD 有范围重叠 | 必须先调整范围边界，再拆任务 |

**注意**：如果需求已经有 Figma 设计稿，优先触发 `design-analysis` Phase-1 Skill，设计分析产出会作为需求精化的输入。

---

## Definition of Ready（DoR）

**每个进入开发的需求，必须满足以下全部条件：**

```
[ ] 用 User Story 格式描述：作为 [角色]，我想 [操作]，以便 [目的]
[ ] 有明确的 Acceptance Criteria（每条可独立验证）
[ ] 范围边界清晰（有"不包含"列表）
[ ] 外部依赖已明确（设计稿/API/其他 PRD）
[ ] 设计稿引用或明确标注"无设计，按规范实现"
[ ] 优先级已确认（P0/P1/P2）
[ ] 没有未解决的需求冲突
```

未满足 DoR → 不得进入任务拆解。

---

## 执行步骤

**Step 1：DoR 快速检查**

读取用户输入，对照 DoR 清单逐项打勾。标记所有 `[ ]` 未满足项。

**Step 2：逐项补全（一次一问）**

对每个未满足项，按以下顺序逐一提问：

1. 用户价值（"这个功能是为了解决什么问题？"）
2. 验收标准（"完成后，你怎么判断它做好了？"）
3. 范围边界（"这个功能不包含哪些情况？"）
4. 优先级（"这个和现有 P0 任务比，优先级如何？"）
5. 设计依赖（"有设计稿吗？还是按现有组件风格实现？"）

```
规则：
✅ 一次只问一个问题
✅ 每次提问附带建议选项（降低用户思考成本）
✅ 记录每个答案，最后汇总输出
❌ 禁止在 DoR 未满足时开始写 Spec 或 Plan
```

**Step 3：输出精化后的需求**

```markdown
## 需求：[功能名称]

**User Story**
作为 [用户角色]，我想要 [操作/功能]，以便 [目的/价值]。

**优先级**: P0 / P1 / P2

**Acceptance Criteria**
- AC-1: 当 [条件] 时，[系统行为] → [可观察结果]
- AC-2: 当 [条件] 时，[系统行为] → [可观察结果]
- AC-3: （边界/错误场景）...

**不包含（Out of Scope）**
- X 功能（后续单独 PRD）
- Y 场景（已知不支持）

**依赖**
- 设计稿：[Figma 链接] 或 "无，按现有规范"
- 依赖 PRD：PRD-XXX（需先完成）
- 依赖 API：无 / [描述]
```

**Step 4：范围冲突检查**

输出草稿后，扫描 `project-management/prd-registry.md`：
- 是否与现有 Active/Queued PRD 有功能重叠？
- 是否会被某个 in-progress PRD 的架构决策影响？

有冲突 → 明确告知用户，建议合并或调整优先级。

**Step 5：写入 PRD 文件**

确认后，在 `tasks/prd/` 创建或更新对应 PRD 文件，并在 `prd-registry.md` 的 Queue 中添加条目。

---

## AC 质量标准

**合格 AC**：
```
✅ "当用户点击'折叠'按钮时，子节点动画收起（200ms ease-out），折叠图标旋转 90°"
✅ "当画布无节点被选中时，右键菜单不出现"
✅ "Escape 键按下时，所有已展开的下拉菜单关闭"
```

**不合格 AC**（必须重写）：
```
❌ "交互体验流畅"（不可验证）
❌ "颜色正确"（不具体）
❌ "性能良好"（没有指标）
```

---

## 与其他 Skill 的衔接

```
[无设计稿的任务链路]

用户提出需求
  ↓ DoR 检查未通过
requirements-refinement（本 Skill）
  ↓ 产物：满足 DoR 的需求 + PRD 草稿
（如需求复杂）brainstorming
  ↓
writing-plans
  ↓
子 agent 实现 → two-stage-review → DoD

[有设计稿的任务链路]

design-analysis Phase-1（提取设计规格）
  ↓ 产物：设计分析包
requirements-refinement（本 Skill，补充产品逻辑/用户价值）
  ↓ 产物：完整 PRD（设计规格 + 产品逻辑 + AC）
→ 进入开发链路
```

---

_版本：v1.0_
_来源：从 agent-roles.md product-strategist + project-manager 角色升级_
