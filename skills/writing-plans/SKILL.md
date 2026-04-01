# Skill: writing-plans

> **触发条件**：中任务（3-6步）或大任务（跨模块/架构）开始前，必须先写 plan，禁止直接动手写代码。

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

**口诀**：去掉 AI 工具后，工程师还需要这条信息吗？需要 → docs/product/ 等产品文件；不需要 → AGENTS.md。

---

## Plan 写作原则

假设执行者（子 agent）是：
- 技术能力强，但对这个 codebase 零了解
- 不知道项目的特定规则和约定
- 有能力执行，但不能自己判断边界

**因此：plan 必须包含执行者所需的一切信息，不能依赖任何隐性假设。**

---

## Plan 文件结构

```markdown
# [功能名称] 实施计划

> **目标**：一句话说清楚这个 plan 要实现什么
> **架构**：2-3 句话说明技术方案
> **关键文件**：列出会改动的文件
> **验证命令**：npm run build / typecheck / test

---

### Task 1: [任务名]

**涉及文件**：
- 修改：`src/exact/path/to/file.tsx`（行范围，如已知）
- 新增：`src/exact/path/to/new-file.ts`

**步骤**：
- [ ] 步骤 1：[做什么]
  ```typescript
  // 具体代码
  ```
  验证：运行 `npm run typecheck`，期望无报错

- [ ] 步骤 2：[做什么]
  ```typescript
  // 具体代码
  ```
  验证：运行 `npm run test`，期望通过

- [ ] 步骤 3：提交
  ```bash
  git add [具体文件]
  git commit -m "feat: [描述]"
  ```

**完成标准**：[列出可验证的通过标准]
```

---

## No-Placeholder 规则（强制）

以下表达**一律禁止**出现在 plan 里：

```
❌ "TBD" / "TODO" / "待定" / "后续处理"
❌ "添加适当的错误处理"
❌ "按现有逻辑处理"
❌ "参考 Task N 的实现"（必须把代码写出来）
❌ 步骤里只有描述，没有代码（代码步骤必须有代码）
❌ 没有验证命令的步骤
❌ 没有期望输出的验证命令
```

**发现以上任何一条 → 立即修复，才能进入实施**。

---

## Spec 自检（写完 plan 后必须执行）

1. **Placeholder 扫描**：逐行检查，有没有上述禁止表达？
2. **内部一致性**：函数名、类型名、文件路径在不同 task 里是否一致？
3. **范围检查**：有没有把不相关的功能混进来？
4. **歧义检查**：每条需求是否只有一种解读？

自检通过 → 可以进入实施。

---

## 任务粒度参考

每个 task 应该是 5-15 分钟可完成的工作：
- ✅ "在 EditorPage.tsx 第 1248 行修改彩虹注入条件，加 `!node.data.borderColor` 判断"
- ✅ "在 colorUtils.ts 的 FILL_COLOR_ROWS 第 4 格从 #3D3D3D 改为 rgba(0,0,0,0.85)"
- ❌ "实现填充色功能"（太大，要拆）
- ❌ "修复颜色相关的 bug"（太模糊）

---

## 执行完成后

写完 plan → 执行 Spec 自检 → 通知用户 review plan → 用户确认后才开始实施。
