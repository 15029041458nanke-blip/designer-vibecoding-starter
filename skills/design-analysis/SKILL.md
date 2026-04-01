# Skill: design-analysis

> 本 Skill 对应原 `design-analyst` 角色，是历经多轮实践优化的沉淀。
> 分两个阶段：**Phase-1（前置设计分析）** 和 **Phase-2（后置 Design QA）**。
> 两个阶段都是强制门控，不得跳过。
>
> **扩展规则库**（执行前必读）：`agent-context/design-role-rules.md`
> 包含：Figma→CSS 还原的完整规则集（§1 图标 / §2 Border / §3 尺寸 / §4 节点类型 / §5 布局对齐 / §6 组件系统 / §7 走查清单），每条规则均附真实错误案例和修复方案，优先级高于本 Skill 文档。

---

## 触发条件

| 场景 | 触发阶段 |
|---|---|
| 任务输入包含 Figma 链接或设计稿引用 | Phase-1（必须在写 Plan 前完成） |
| 任何 UI 任务进入 DoD 检查前 | Phase-2（必须在宣布完成前完成） |
| PRD 缺少 UI 规格，需要从设计提取 | Phase-1 |

---

## 设计稿输入场景判断（Phase-1 前置步骤）

拿到设计稿后，**先判断场景**，再执行 Phase-1 分析。

### 场景 A：大型设计稿（包含多个独立功能）

**判断标准**：拉取 Figma 数据后，发现顶层 Frame/Section ≥2 个，且功能相互独立（不共享主要状态）。

```
执行流程：
1. 对整个设计稿做结构速览（不深入每个组件）
2. 识别出几个独立功能模块，列出清单
3. 向用户展示拆分方案：
   「这个设计稿包含 3 个独立功能：A / B / C。
     建议拆为 PRD-XXX / PRD-YYY / PRD-ZZZ，按 A→B→C 顺序实现。
     是否确认这个拆分方案和优先级？」
4. 用户确认后，逐一对每个 PRD 执行 Phase-1 完整分析
5. 将所有新 PRD 加入 prd-registry.md 队列
```

禁止：一口气分析所有功能后产出一个大 PRD，必须拆分。

### 场景 B：同时提供产品 PRD + 设计稿

**判断标准**：用户同时给出了文字版产品需求文档（或口头描述的功能范围）+ Figma 链接。

```
执行流程：
1. 先读产品 PRD，提取功能范围清单（列出所有提到的功能点）
2. 对设计稿执行 Phase-1 分析，提取设计侧的功能点和 UI 规格
3. 对照两者，产出三类结论：
   ✅ 一致项：直接写入 PRD 的 AC
   ⚠️  设计稿有、PRD 未提及：标注「设计疑点」，逐一询问用户是否纳入范围
   ❗ PRD 有、设计稿未覆盖：标注「设计遗漏风险」，告知用户
4. 对齐确认后，输出完整 PRD（含设计规格 + 产品逻辑 + AC）
```

禁止：把"设计稿未覆盖"的内容当成"不需要实现"，必须标注风险告知用户。

### 场景 C：单组件 / 小模块设计稿

**判断标准**：Figma 链接只包含一个组件或一个功能模块，内容较聚焦。

```
执行流程：
1. 对该模块执行 Phase-1 完整分析
2. 检查 prd-registry.md，判断归属：

   情况 1：prd-registry 中有现有 PRD 已包含该组件
   → 在现有 PRD 的"设计规格"区块中补充分析结果
   → 不新建 PRD，告知用户「已补充到 PRD-XXX」

   情况 2：该功能未出现在任何已有 PRD 中
   → 新建 PRD-XXX 文件（按 tasks/prd/README.md 的格式）
   → 在 prd-registry.md 队列中加入，询问用户优先级

3. 告知用户判断结果，确认后执行
```

禁止：不看 prd-registry 就直接新建 PRD，可能造成重复。

---

## Phase-1：前置设计分析（Design Analysis）

**目标**：把设计稿转化为结构化 Spec，作为 PRD 和 Plan 的输入。
**产物**：设计分析包（Design Analysis Package）+ PRD UI 规格章节草稿。

### 执行步骤

**Step 1：获取设计数据**
```
优先级：
1. 有 Figma 链接 → 调用 Figma MCP（mcp__figma__get_figma_data）拉取节点数据
2. 有 SPEC 文件 → 读取 tasks/prd/SPEC-*.md
3. 仅有截图描述 → 必须明确标注"基于描述推断，需设计确认"
```
禁止：在没有设计证据的情况下开始分析。

**Step 1.5：图标资产配置检查（有 Figma 链接时必须执行）**

拿到 Figma 数据后，检查设计稿中是否存在图标节点（`IMAGE-SVG` / `COMPONENT` 类型的图标）。如果存在，**在进入 Step 2 前**，先向用户确认 Figma Personal Access Token（PAT）配置状态。

**执行流程：**

```
检查到设计稿含图标资产？
  YES → 执行下方「PAT 配置引导」
  NO  → 直接进入 Step 2
```

**PAT 配置引导（向用户说明）：**

> 设计稿中包含图标资产。为了下载原始 Figma 图标（SVG），需要配置 Figma Personal Access Token（PAT）。
>
> **如何获取 PAT：**
> 1. 打开 Figma 网页版（figma.com）→ 点击右上角头像 → Settings
> 2. 左侧菜单 → Security → Personal access tokens
> 3. 点击「Generate new token」，填写名称（如 codewiz），选择 Expiration
> 4. 复制生成的 token（格式：`figd_...`）
> 5. 将 token 粘贴在这里
>
> **如果暂时不想配置：** 图标位置将先用 IconPlaceholder 占位（20px 容器 + 18px 灰色圆圈），后续可随时补充 token 来替换为真实图标。

**用户响应处理：**

| 用户反应 | 处理方式 |
|---|---|
| 粘贴了 `figd_...` token | 记录 token，实现阶段用 REST API `/v1/images + curl` 下载图标（见 design-role-rules.md §1.2） |
| 说"跳过"/"暂不配置" | 继续分析，所有图标节点在实现阶段用 IconPlaceholder 占位，注释标注 Figma nodeId |
| 说"已经配置过了" | 直接进入 Step 2，图标下载时用已知 token |

**PAT 验证（用户提供 token 后立即执行）：**

```bash
curl -s "https://api.figma.com/v1/me" -H "X-Figma-Token: <token>" | python3 -c "import json,sys; d=json.load(sys.stdin); print('✅ Token 有效，用户：', d.get('email','?')) if 'email' in d else print('❌ Token 无效：', d)"
```

验证通过后继续。验证失败则重新引导用户生成 token。

---

**Step 2：提取结构信息**

对每个组件/页面提取：

| 维度 | 提取内容 | 映射到 |
|---|---|---|
| 组件层级 | 父子关系、嵌套结构 | 组件树 |
| 状态矩阵 | default/hover/active/disabled/focus/error | State Matrix 表 |
| 间距 | margin/padding/gap 像素值 | 对应 design token 变量名 |
| 颜色 | 所有颜色值 | 对应 token 名称（如 `--color-primary-500`） |
| 字体 | size/weight/line-height | 对应 token 或具体值 |
| 圆角/描边 | border-radius/border-width | 对应 token |
| 交互行为 | 点击/悬停/键盘响应 | 需要逐条记录 |

**Step 3：识别设计疑点**

以下情况必须记录为"设计疑点"，不得自行推断：
- 某状态在设计稿中未出现（如：没有 disabled 态）
- 不同页面同一组件的样式不一致
- 间距值无法映射到现有 token（非标准值）
- 交互行为未标注（如：点击后跳转还是展开？）
- 响应式断点未说明

**Step 4：逐一提问，消除疑点**

```
规则：
✅ 一次只问一个疑点
✅ 每个问题附带"如果不确定，我的默认处理是 X"供用户快速确认
✅ 用户回答后立即更新分析，再问下一个
❌ 禁止在疑点未解决时继续推进
❌ 禁止把"我的推断"当成"已确认需求"写入 PRD
```

**Step 5：输出设计分析包**

所有疑点解决后，输出：

```markdown
## 设计分析包：[组件/功能名称]

### 组件状态矩阵
| 状态 | 背景色 | 边框 | 文字色 | 图标 |
|------|--------|------|--------|------|
| default | --color-bg-1 | none | --color-text-1 | ... |
| hover | --color-bg-2 | ... | ... | ... |
| ...  | ... | ... | ... | ... |

### 间距规格
- 内边距：12px 16px（→ `--spacing-3` `--spacing-4`）
- 元素间距：8px（→ `--spacing-2`）

### 图标资产清单
| 图标名 | Figma nodeId | 节点类型 | 目标文件名 | 状态 |
|--------|-------------|----------|-----------|------|
| 添加图片 | I5074:58228;70:2085;70:1496 | IMAGE-SVG | add-image.svg | ✅ 已下载 / ⏳ 待下载 / 🔲 IconPlaceholder |
| ...    | ... | ... | ... | ... |

> 下载命令（需 PAT）：
> ```bash
> curl -s "https://api.figma.com/v1/images/<fileKey>?ids=<nodeId（%3B替换分号）>&format=svg" \
>   -H "X-Figma-Token: <token>" | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d['images'].values())[0])"
> # 拿到 S3 URL 后：curl -sL <url> -o src/assets/icons/<name>.svg
> ```

### 交互行为
- 点击 X → 触发 Y
- Escape → 关闭
- 键盘导航：...

### 已确认疑点
- Q: disabled 态是否需要？ A: 是，使用 opacity:0.4
- Q: ... A: ...

### 设计限制（Out of Scope）
- 移动端响应式（设计稿未提供）
- Dark mode（另立 PRD）
```

**Step 6：转化为 PRD UI 规格 + Acceptance Criteria**

每条 AC 必须可验证，格式：
```
AC-1: 当用户悬停 X 组件时，背景色变为 --color-bg-2（#F5F5F5），过渡时间 150ms ease
AC-2: 当 X 组件处于 disabled 状态时，opacity 为 0.4，cursor 为 not-allowed，点击无响应
```

禁止模糊 AC：
```
❌ "hover 时有视觉反馈"
✅ "hover 时背景色从 transparent 变为 --color-bg-hover，过渡 150ms ease-in-out"
```

---

## Phase-2：后置 Design QA

**目标**：用苛刻的设计视角，逐条验证实现是否还原设计稿。
**产物**：QA 报告 + 最终结论（还原通过 / 需要修改）。
**触发时机**：任何 UI 任务完成、进入 DoD 检查之前，必须先过 Design QA。

### 执行步骤

**Step 1：读取验证基准**
- PRD 中的 AC 列表（必须逐条过，不能跳）
- Phase-1 输出的设计分析包（颜色/间距/状态矩阵）

**Step 2：逐 AC 验证**

对每条 AC 执行：
1. 定位到对应的代码（组件文件/CSS 变量）
2. 提取实际值
3. 对比设计规格值
4. 输出结果：PASS / FAIL / NEEDS_CLARIFICATION

**Step 3：输出 QA 报告**

```markdown
## Design QA 报告：[组件/功能名称]

| AC | 检查项 | 设计规格 | 实现值 | 结果 | 严重度 |
|----|--------|----------|--------|------|--------|
| AC-1 | hover 背景色 | #F5F5F5 | #F5F5F5 | PASS | - |
| AC-2 | disabled opacity | 0.4 | 0.5 | FAIL | Critical |
| AC-3 | 过渡时间 | 150ms | 未设置 | FAIL | Minor |

### 失败项详情

**AC-2 [Critical]**
- 期望：opacity: 0.4
- 实际：opacity: 0.5（在 MindmapNode.tsx:156）
- 修复：将 `opacity: 0.5` 改为 `opacity: 0.4`

**AC-3 [Minor]**
- 期望：transition: 150ms ease-in-out
- 实际：无 transition
- 修复：在 `.node-shell:hover` 中添加 `transition: background-color 150ms ease-in-out`

### 最终结论

结论：**需要修改**（Critical 项未通过）
需修复后重新 QA。

---
或：
结论：**还原通过** ✅（所有 Critical 项通过，Minor 项已知晓）
可进入 DoD。
```

### 严重度定义

| 级别 | 含义 | 是否阻塞发布 |
|---|---|---|
| Critical | 设计意图被错误还原（颜色/结构/核心交互） | 是 |
| Minor | 像素级偏差、过渡时间差异（≤10%） | 否（记录即可） |
| N/A | 实现超出设计稿范围的合理增强 | 否 |

### 铁律

```
❌ 禁止：跳过 Design QA 直接宣告完成
❌ 禁止：在没有代码证据的情况下给出"还原通过"
❌ 禁止：把"我认为看起来差不多"当成 PASS
❌ 禁止：Critical 项未通过，结论写"通过"
✅ Critical 项全部 PASS → 可以给"还原通过"结论
✅ 有 Minor 项但无 Critical → 记录后可通过
```

---

## 与其他 Skill 的衔接

```
[有设计稿的任务链路]

design-analysis Phase-1（本 Skill）
  ↓ 产物：设计分析包 + PRD UI 规格 + AC 列表
requirements-refinement（如需补充产品逻辑）
  ↓ 产物：完整 PRD
architecture-check（如涉及架构变更）
  ↓
writing-plans（写实现 Plan）
  ↓
子 agent 实现
  ↓
two-stage-review（Spec 合规 + 代码质量）
  ↓
design-analysis Phase-2（本 Skill，Design QA）← 必须在 DoD 前执行
  ↓ 结论：还原通过
DoD 完成
```

---

_版本：v1.1_
_来源：从 agent-roles.md design-analyst 角色升级，保留所有迭代沉淀_
_v1.1 新增：Step 1.5 图标资产配置检查（PAT 引导 + 验证 + IconPlaceholder 兜底说明）_
