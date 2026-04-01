# Design Role Rules — 设计还原规则手册

> **定位**：设计角色（design-analyst / engineer 还原阶段 / reviewer 走查阶段）的强制遵守规则集。
> **版本**：v2.1（2026-03-26）— §1 调整为两层策略（REST API 首选 → IconPlaceholder 兜底），废弃 MCP 工具作为首选；新增图标资产清单规范
> **目标**：第一稿还原率 > 80%，逐版本迭代提升。
> **更新机制**：每次发现新的典型还原问题，立即在对应章节追加案例，注明发现时间和修复方案。
>
> 版本历史见文末 §CHANGELOG。

---

## 使用说明

本文件适用于设计驱动链路的三个环节，各环节读取重点不同：

| 环节 | 读取重点 |
|------|---------|
| **设计分析**（design-analyst 提取 SPEC） | §1 图标 / §3 尺寸 / §4 节点内容类型 / §5 布局 / §6 组件系统 |
| **代码转化**（engineer 实现） | §2 border / §3 尺寸 / §4 节点内容类型 / §5 布局排列数量 |
| **设计走查**（design-analyst QA / reviewer） | §3 尺寸验证 / §5 排列数量验证 / §7 走查清单 |

**规则优先级**：本文件 > SPEC 文档 > 实现惯例。若本文件与 SPEC 冲突，以本文件为准并更新 SPEC。

---

## §1 图标（Icon）还原规则

> **v2.0 更新（2026-03-26）**：升级为三层策略（MCP 工具 → Figma REST API → IconPlaceholder）；新增图标资产清单规范和 PAT 配置引导。

### 1.1 两层策略总览

| 优先级 | 方案 | 适用场景 | 已验证有效 |
|--------|------|---------|-----------|
| **1（首选）** | Figma REST API `/v1/images` + `curl` 下载 | **所有节点类型均适用**，包括 IMAGE-SVG | ✅（实测更通用） |
| **2（兜底）** | `<IconPlaceholder size={20} />` | 无 PAT / API 失败 / 权限不足 | ✅ |

> **注意**：`download_figma_images` MCP 工具不再作为首选——它对 IMAGE-SVG、Component 内部子节点等常见场景有限制，实测失败率高。**直接用 REST API 更可靠、覆盖所有场景。**

**铁律（无例外）**：
- ❌ 禁止用文字替代图标（如用"实线"代替线型图标）
- ❌ 禁止手写/自行绘制语义化图标 SVG（无论图标多简单）
- ❌ 禁止留空不处理
- ✅ 必须走两层策略：先 REST API，失败才 IconPlaceholder

### 1.2 层级 1（首选）：Figma REST API 直接渲染

**前提**：需要 Figma Personal Access Token（PAT，格式 `figd_...`）。
> ⚠️ `mcp.json` 里的 OAuth session token ≠ PAT，不能用于 REST API。
> PAT 生成：Figma 网页 → 头像 → Settings → Security → Personal access tokens。

**操作步骤**：
```bash
FILE_KEY="ySz0o9TxV0rIieDfxSbFwp"
PAT="figd_..."

# Step 1：获取渲染 URL（node id 中的分号需 URL encode 为 %3B）
curl -s "https://api.figma.com/v1/images/${FILE_KEY}?ids=<nodeId>&format=svg" \
  -H "X-Figma-Token: ${PAT}" | python3 -m json.tool
# → { "images": { "<nodeId>": "https://figma-alpha-api.s3.us-west-2.amazonaws.com/..." } }

# Step 2：下载 SVG
curl -sL "<s3_url>" -o src/assets/icons/<name>.svg

# Step 3：验证
head -1 src/assets/icons/<name>.svg   # 应以 <svg 开头
```

**验证 PAT 是否有效**：
```bash
curl -s "https://api.figma.com/v1/me" -H "X-Figma-Token: <PAT>" | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print('✅', d.get('email')) if 'email' in d else print('❌ 无效')"
```

### 1.3 层级 2（兜底）：IconPlaceholder 规格（固定标准，不得修改）

```
容器：width: 20px; height: 20px（由 size prop 控制）
占位：直径 18px 圆形，stroke 1.5px，颜色 rgba(0,0,0,0.15)，无填充
```

```tsx
// 使用方式：附 TODO 注释标注 Figma nodeId，等 PAT 可用后替换
<IconPlaceholder size={20} aria-hidden />
{/* TODO: 替换为真实图标，Figma nodeId: <nodeId>，fileKey: ySz0o9TxV0rIieDfxSbFwp */}
```

对应 React 实现：[`src/components/icons/index.tsx`](../src/components/icons/index.tsx) → `IconPlaceholder`。

### 1.4 图标资产清单规范

**每个含图标的 PRD/SPEC 必须维护一张图标资产清单**，记录在设计分析包里：

```markdown
### 图标资产清单

| 图标语义 | Figma nodeId | 节点类型 | 目标文件 | 下载状态 |
|---------|-------------|---------|---------|---------|
| 添加图片 | I5074:58228;70:2085;70:1496 | IMAGE-SVG | add-image.svg | ✅ REST API 下载 |
| 添加表情 | I5074:58228;70:2086;70:1496 | IMAGE-SVG | add-emoji.svg | ✅ REST API 下载 |
| 添加描述 | I5074:58228;70:2087;70:1496 | IMAGE-SVG | add-description.svg | ✅ REST API 下载 |
```

**下载状态枚举**：
- `✅ REST API 下载` — 层级 1 成功
- `🔲 IconPlaceholder` — 层级 2 兜底，nodeId 已记录，待替换
- `⏳ 待下载` — 已识别，尚未执行

### 1.5 典型错误案例

> **[2026-03-19] border 面板线型选项用文字**
>
> 错误：`<FocusBtn>实线</FocusBtn>`（自造文字）
> 根因：未查看 Figma 节点 type，凭语义自造内容
> 修复：查 Figma → `5023:57260` type=`IMAGE-SVG`，降级为 `<IconPlaceholder size={20} />`
> 新增规则：§4 节点内容类型识别

> **[2026-03-20] download_figma_images 返回 404**
>
> 错误：nodeId 使用了 Component 内部子节点 `5023:57260`
> 根因：Component 内部子节点不是顶层可导出节点，MCP 工具无法直接下载
> 修复：改为层级 2（REST API），用实例节点 ID 渲染导出
> 新增规则：§1.2 → §1.3 降级路径

> **[2026-03-26] IMAGE-SVG 节点下载 0×0 / 手写语义 SVG**
>
> 错误：IMAGE-SVG 节点用 MCP 工具下载得到 0×0 空文件，改为手写 `<svg>` 还原图标外观
> 根因：两个错误叠加——MCP 不支持 IMAGE-SVG、没有尝试层级 2
> 修复：用层级 2（REST API `/v1/images?format=svg`）成功下载真实矢量 SVG
> 新增规则：§1.1 三层策略 + §1.3 REST API 步骤

---

## §2 Border 还原规则

### 2.1 Figma stroke → CSS border 映射

**默认策略：内 border**（border 向内画，不撑大容器）

```css
/* 正确实现内 border */
element {
  width: [Figma标注值]px;   /* 显式固定，必须 */
  height: [Figma标注值]px;  /* 显式固定，必须 */
  box-sizing: border-box;
  border: Npx solid {color};
}
```

### 2.2 验证方法

浏览器 DevTools 测量渲染尺寸 vs Figma 标注尺寸：
- ✅ **相同** → border 方向正确
- ❌ **相差 N×2**（N = border-width）→ border 向外画了，切换实现方式

### 2.3 特殊场景：fill 子元素容器的结构性 border

当 Figma 容器满足以下条件时，**不能用 `border + border-box`，必须用 `outline`**：
- 容器有 Inside stroke
- 容器内有 `sizing: fill` 的子元素

**原因**：Figma Inside stroke 是叠加装饰层，fill 子元素仍填满容器声明尺寸（如 208px）。CSS `border + border-box` 会真实压缩内容区（208→207px），导致 fill 子元素尺寸不足，出现换行、列数变少等问题。

```css
/* 含 fill 子元素的结构性容器边框 */
.container {
  width: 208px;
  box-sizing: border-box;
  outline: 0.5px solid rgba(0, 0, 0, 0.08); /* 不影响盒模型 */
  border: none;
}
```

### 2.4 典型错误案例

> **[2026-03-19] 颜色面板 5 列变 4 列**
>
> 错误：`FlowMenuDropdown` 使用 `border: 0.5px + border-box`，内容区 207px，5个28px圆点(184px)+4个11px间距(44px)=184px > 183px，放不下第5个
> 根因：Figma Inside stroke 不压缩 fill 子内容，CSS border-box 会压缩
> 修复：改为 `outline: 0.5px solid`，内容区恢复 208px，5列正常排布
> 新增规则：§5.3 排列数量验证

---

## §3 尺寸还原规则

### 3.1 核心原则

还原后从小到大逐层验证：`icon → button → row → panel → modal`

每一层与 Figma 标注值**完全一致**，不允许凭感觉近似。

### 3.2 关键尺寸来源

从 Figma MCP `globalVars.styles` 中的 layout token 读取精确数值：
- `dimensions.width / dimensions.height` → fixed 尺寸
- `padding` → 内边距（注意多值顺序：top right bottom left）
- `gap` → 子元素间距
- `borderRadius` → 圆角

### 3.3 典型错误案例

> **[2026-03-19] FocusBtn 宽度错误**
>
> 错误：`width: 100%`（错误推断为 fill）
> 根因：没有直接查 FocusBtn Component Set，从使用侧推断 sizing 类型
> 修复：查 `5018:73659` → `layout_9CEFFC: sizing: fixed, width: 40, height: 36`
> 修复后：`width: 40px; height: 36px`
> 教训：**sizing 类型必须从组件的 Component Set 直接读取，不能从使用侧实例推断**

---

## §4 节点内容类型识别规则

### 4.1 实现前必须查 Figma 节点 type

| Figma type | 对应 CSS/React 实现 |
|-----------|-------------------|
| `TEXT` | 文字 `children`，保留 Figma `textStyle` 中的字体/大小/权重 |
| `IMAGE-SVG` / `VECTOR` | `<IconPlaceholder />` 或实际导出 SVG，**禁止用文字替代** |
| `FRAME` / `INSTANCE` | 对应 React 组件或 div，继续下钻 |
| `BOOLEAN_OPERATION` | 通常是 SVG 图形，用 IconPlaceholder |
| `RECTANGLE` / `ELLIPSE` | CSS 形状或 SVG 基本图形 |

### 4.2 查节点 type 的方法

通过 Figma MCP `get_figma_data` 获取节点数据，在返回结果的 `nodes[].type` 字段读取。

### 4.3 常见陷阱

- 同名元素在父组件中可能已被设置为某变体，**必须下钻到 Component Set 查看完整变体列表**
- 使用侧（UI 页面/父组件中的实例）的状态不代表所有可能状态

---

## §5 布局还原规则

### 5.1 容器 sizing 分类（必须逐一确认）

| Figma sizing | CSS 实现 | 说明 |
|-------------|---------|------|
| **hug** | `display: inline-flex` 或 `width: fit-content` | 由内容物撑开，禁止写死宽度 |
| **fixed** | `width: Npx; height: Npx`（显式固定） | 强制固定，不接受任何外部覆盖 |
| **fill** | `flex: 1` 或 `width: 100%`（在 flex 容器内） | 均分或撑满父容器可用空间 |

**sizing 类型的读取路径**：`globalVars.styles.[layoutToken].sizing.horizontal/vertical`

### 5.2 min / max 尺寸

若 Figma 标注了 min-width / max-width，必须在 CSS 中对应写 `min-width / max-width`，不得省略。

### 5.3 排列数量严格对齐

设计稿中横向/纵向排列了 N 个元素，实现必须也是 N 个。

**验证步骤**：
1. 数设计稿中每行/列的元素数量
2. 与实现对比
3. 若不一致：
   - 先检查元素宽度是否正确（fixed/hug 取值）
   - 再检查容器可用宽度（父容器宽度 - padding - border影响）
   - 再检查 gap 是否正确
   - 计算：`N × 元素宽 + (N-1) × gap ≤ 可用宽度`
   - 若不满足，找出导致可用宽度不足的原因（通常是 border 用了 box-sizing: border-box 压缩了内容区）

### 5.4 典型错误案例

> **[2026-03-19] 颜色面板每行4列 vs 设计稿5列**
>
> 设计稿：5列（5×28px + 4×11px = 184px = 208px容器-24px padding）
> 实现：4列（border: 0.5px + border-box → 内容区207px，减24px padding=183px < 184px）
> 修复：outline代替border，详见 §2.3

---

### 5.5 元素对齐规则

**每个元素都必须明确定义 X 轴和 Y 轴的对齐方式**，不允许无意中的位置偏移。

#### Figma MCP 返回的对齐数据说明

Figma MCP **会返回对齐属性**，但分两种情况，处理策略不同：

| 元素类型 | MCP 返回字段 | 处理方式 |
|---------|------------|---------|
| **Auto Layout 子元素** | `alignItems` / `justifyContent` / `alignSelf`（直接可读） | 直接映射到 CSS flex 属性 |
| **绝对定位元素**（`position: absolute`） | 只有 `locationRelativeToParent: { x, y }`，**无对齐标签** | 手动判断：若 x/y = (父-子)/2 → 居中意图；否则 → 真实偏移 |

```yaml
# Auto Layout 子元素（MCP 直接给出对齐）
layout_9CEFFC:
  mode: row
  alignItems: center       # ← Y轴对齐
  justifyContent: center   # ← X轴对齐

# 绝对定位元素（MCP 只给坐标，无对齐标签）
layout_SXONBD:
  mode: none
  position: absolute
  locationRelativeToParent:
    x: 6   # ← 需要手动判断是否居中意图
    y: 6
  dimensions:
    width: 16
    height: 16
```

#### 对齐实现方式对照表

| 对齐意图 | 判断条件 | CSS 正确实现 |
|---------|---------|------------|
| X+Y 居中（flex 容器内子元素） | MCP 返回 `alignItems: center` + `justifyContent: center` | `display: flex; align-items: center; justify-content: center` |
| X+Y 居中（绝对定位子元素） | 计算 x == (父宽-子宽)/2 且 y == (父高-子高)/2 | **`inset: 0` + flex 双轴居中，禁止字面翻译 x/y 坐标为 top/left** |
| 靠某边对齐（绝对定位） | x 或 y = 0 | `top/right/bottom/left: 0`（对应边） |
| 真实偏移（非居中） | x/y 值不等于居中公式结果 | `top: Ypx; left: Xpx`，但须加上父容器 border 宽度修正 |

#### ⚠️ Figma x/y 坐标字面翻译陷阱

当 Figma 元素坐标 `x = y = (父容器尺寸 - 子元素尺寸) / 2` 时，设计意图是**居中**，必须用 CSS 居中而非字面坐标。

原因：CSS 绝对定位原点是 **padding 边**（不含 border），父容器有 `border: Npx` 时，`top: 6px` 的实际视觉距离 = `N + 6px`，导致偏移：

```css
/* ❌ 错误：x:6, y:6 是居中值 (28-16)/2=6，字面翻译后因 border:2px 偏移 2px */
.check { position: absolute; top: 6px; left: 6px; }

/* ✅ 正确：居中意图 → inset:0 + flex 双轴居中，与 border/padding 无关 */
.check {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;     /* Y 轴居中 */
  justify-content: center; /* X 轴居中 */
}
```

#### 对齐走查步骤（放入 §7 QA 流程）

1. 对每个绝对定位元素，计算 `(父容器尺寸 - 子元素尺寸) / 2`
2. 若计算结果等于 Figma x/y 值 → 居中意图 → 改用 `inset:0 + flex` 实现
3. 若不等 → 真实偏移意图 → 用 `top/left`，同时确认父容器 border 是否影响坐标原点

### 5.6 典型错误案例（对齐）

> **[2026-03-19] ColorDot selected 态 check 图标偏上偏左**
>
> 错误：`top: 6px; left: 6px`（字面翻译 Figma x:6 y:6）
> 根因：x:6 y:6 = (28-16)/2 = 居中意图，父容器 `border:2px` 使 CSS 偏移变成 8px，图标中心在 16px 而容器中心在 14px，视觉偏移 2px
> 修复：`position: absolute; inset: 0; display: flex; align-items: center; justify-content: center`
> 教训：居中意图必须用 CSS 对齐属性，绝不能字面翻译 Figma 坐标

---

## §6 组件与设计系统规则

### 6.1 Tokens 绑定

- 设计稿使用了 tokens（颜色/字体等有明确 token 命名）→ 实现必须绑定 CSS 变量
- 设计稿未使用 tokens → 用具体值填充，并在 SPEC 中列出「未绑定 token 清单」提醒

**必须 token 化的属性**（若设计稿有定义）：
`color` / `font-size` / `font-weight` / `line-height` / `border-radius` / `border` / `box-shadow` / `spacing` / `z-index`

### 6.2 组件识别与下钻规则

1. Figma 中识别到 Component Set → 在 React 中实现为独立组件
2. Component Set 有多个变体 → 用 `variant` prop 映射所有变体，**不得遗漏任何变体**
3. **必须直接查 Component Set 节点**（通过 `componentSetId` 找到顶层节点），才能看到完整变体列表
4. 禁止仅从使用侧嵌套实例读取变体——使用侧的实例只展示当前被用到的变体，可能不完整

### 6.3 提取路径规则（防遗漏）

```
正确路径：Figma MCP → Component Set 节点（componentSetId） → 所有 children → 完整变体
错误路径：Figma MCP → 使用侧 Frame → 嵌套 Instance → 只看到部分变体
```

### 6.4 典型错误案例

> **[2026-03-19] ColorDot 漏掉 hover 变体**
>
> 错误：从 `5005:29748`（menu btn 使用侧）提取颜色面板，只看到 Default/selected 两个变体
> 根因：使用侧面板只展示了部分实例，未直接查 Component Set
> 修复：直接查 `5023:54209`（填充色atom Component Set） → 发现完整6个变体（Default/hover/selected × empty=true/false）
> 教训：提取变体必须从 Component Set 顶层节点出发

---

## §7 设计走查清单（Design QA Checklist）

每次实现后，按以下顺序逐项检查：

### 7.1 元素层面

- [ ] 所有图标已使用 IconPlaceholder（无法导出时），无文字替代
- [ ] 所有 TEXT 节点内容与设计稿文案完全一致
- [ ] 字体 family / size / weight / line-height 与 Figma textStyle 一致

### 7.2 尺寸层面

- [ ] 每个组件的 width / height 与 Figma 标注值相差不超过 0.5px
- [ ] 所有 padding / gap 值与 Figma globalVars 中的 layout token 一致
- [ ] border-radius 一致

### 7.3 Border 层面

- [ ] 有 Inside stroke 的组件：浏览器渲染尺寸 == Figma 标注尺寸
- [ ] 含 fill 子元素的结构性 border：使用 `outline` 而非 `border`
- [ ] 确认 box-shadow 是否该用 inset

### 7.4 布局层面

- [ ] 每行/列的元素数量与设计稿完全一致
- [ ] 所有 sizing 类型（hug/fixed/fill）已正确对应 CSS 实现
- [ ] fill 元素在 flex 容器内正确展开
- [ ] **所有元素明确 X+Y 两轴对齐**：flex 容器设置了 `align-items` 和 `justify-content`；绝对定位居中元素使用 `inset:0 + flex` 而非 `top/left` 坐标
- [ ] 绝对定位非居中偏移已验证：计算父容器 border 对坐标原点的影响

### 7.5 组件层面

- [ ] 所有 Component Set 变体均已实现（通过 componentSetId 逐一核对）
- [ ] 变体 prop 命名与 Figma 变体维度名称对应
- [ ] 嵌套组件已下钻到子 Component Set 独立核实

### 7.6 Token 层面

- [ ] 颜色值已绑定 CSS 变量（若设计稿有 token 定义）
- [ ] 未绑定 token 的硬编码值已列出清单

---

## §CHANGELOG

| 日期 | 版本 | 新增/修改内容 | 触发问题 |
|------|------|------------|---------|
| 2026-03-19 | v1.0 | 初版建立，整合6条核心还原规则 | 多轮 menu 组件质检 |
| 2026-03-19 | v1.1 | §1 图标规则：IconPlaceholder 规格固定（20px容器+18px圆圈+1.5px stroke） | 图标占位规格不统一 |
| 2026-03-19 | v1.2 | §2 border：新增「fill子元素容器用outline」规则 | 颜色面板5列变4列 |
| 2026-03-19 | v1.3 | §4 节点内容类型：TEXT才可用文字，IMAGE-SVG必须用IconPlaceholder | border面板线型用了文字 |
| 2026-03-19 | v1.4 | §5 排列数量：新增验证步骤和计算公式 | 颜色面板5列变4列 |
| 2026-03-19 | v1.5 | §3 尺寸：FocusBtn sizing从使用侧推断导致错误，规则明确必须查Component Set | FocusBtn width:100%错误 |
| 2026-03-19 | v1.6 | §6 组件：明确提取路径必须从Component Set顶层出发 | ColorDot漏hover变体 |
| 2026-03-19 | v1.7 | §5.5 对齐：居中意图必须用CSS居中，禁止字面翻译Figma x/y坐标；§7 QA清单补对齐验证项 | ColorDot check偏上偏左 |
| 2026-03-19 | v1.8 | §5.5 对齐：补充 Figma MCP 对齐数据返回机制说明（Auto Layout vs 绝对定位的数据差异），精化对照表判断条件 | 厘清 MCP 是否返回 align 属性 |

---

> **如何更新本文件**
>
> 1. 发现新的典型问题 → 在对应 §CHANGELOG 追加一行
> 2. 若问题属于已有规则的新案例 → 在对应章节末尾追加「典型错误案例」
> 3. 若问题属于全新规则类别 → 新建 §N 章节，并在 CHANGELOG 记录
> 4. 每条案例必须包含：错误描述 / 根因 / 修复方案 / 新增/强化的规则引用
