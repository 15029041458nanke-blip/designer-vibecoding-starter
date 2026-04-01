# Section Pattern Codex — 模块视觉模式手册

> **定位**：这是 style-foundation skill 的"设计师经验库"。
> 它记录了不同 section 类型的高质量视觉处理模式，来源于对真实优秀网站的拆解分析。
>
> **用途**：
> - Phase 2 提取时：作为"常规 vs 非常规"的对比基线，帮助识别亮点
> - Phase 3 生成时：为 Constitution 中的 Section Storyboard 提供模式参考
> - 0→1 实现时：当没有参考图时，从模式库中选择匹配风格方向的模式作为起点
>
> **维护方式**：每次用户提供优质参考图并完成拆解后，将新模式沉淀到对应类型下。

---

## 使用指南

每种 Section 类型下收录多种视觉处理模式（Pattern）。每个模式包含：

| 字段 | 说明 |
|------|------|
| **模式名称** | 简短的风格描述 |
| **来源** | 从哪个网站/参考图提取 |
| **视觉描述** | 七维度的简要描述 |
| **CSS 核心模式** | 关键实现代码片段 |
| **适用场景** | 什么风格/产品/行业适合用 |
| **避免用于** | 什么场景不适合 |

---

## Hero Section

> 页面首屏，抓注意力，传递核心信息。
> 通常占据 viewport 的 60-100%。

### 常规做法（基线）

大多数 Hero section 的视觉处理：
- 浅色/白色背景 + 居中大标题 + 副标题 + CTA 按钮
- 可能有右侧/下方的产品截图
- 文字通常是深色无衬线体

**如果参考图的 Hero 与此有明显差异，应标注为亮点。**

### Pattern A：全幅摄影背景 + 叠层标题

_来源：Framer (Kero Template), Hobbes, Giga AI_

**视觉描述**：
- ① 背景：全幅高清摄影（山脉/云海/自然场景），覆盖整个 viewport
- ② 叠层：深色半透明渐变叠层（从上到下加深，确保文字可读性）
- ③ 布局：居中单列，内容区窄（60%宽度）
- ④ 排版：白色大号衬线体标题（60px+），宽字间距；半透明白色副标题
- ⑤ 容器：无卡片，文字直接叠在背景上
- ⑥ 装饰：可能有底部渐隐过渡到下一 section
- ⑦ 产品 UI 截图可嵌入自然场景中，仿佛悬浮在环境里

**CSS 核心模式**：
```css
.hero {
  position: relative;
  min-height: 100vh;
  background: url('hero-photo.jpg') center/cover no-repeat;
}
.hero::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.5));
}
.hero-content {
  position: relative; z-index: 1;
  color: white;
  text-align: center;
}
.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 6vw, 5rem);
  letter-spacing: 0.05em;
}
/* UI 嵌入自然场景 */
.ui-in-nature {
  border-radius: 12px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.3);
  transform: perspective(1000px) rotateX(2deg);
}
```

**适用场景**：自然/有机/生活方式/旅行/高端消费品/企业级叙事
**避免用于**：极简工具类/开发者工具（会显得太"品牌向"）

### Pattern B：深色纯色背景 + 环境光晕 UI 容器

_来源：Linear, Neon, LangChain, Lovart.ai_

**视觉描述**：
- ① 背景：极深色纯色或微妙渐变（#0A0A0F 级别的近黑色）
- ② 叠层：可能有微妙的噪点纹理 + 极淡的径向渐变光晕
- ③ 布局：居中单列，上文字 + 下产品截图
- ④ 排版：白色大号无衬线标题，粗体，紧凑字间距；半透明白色副标题
- ⑤ 容器：产品截图带多层 box-shadow 形成环境光晕 + 1px 内发光边框
- ⑥ 装饰：可能有渐变光晕/射线效果、霓虹线条

**CSS 核心模式**：
```css
.hero {
  background: #0A0A0F;
  min-height: 100vh;
}
/* 环境光晕 UI 容器 */
.product-shot {
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.05),
    0 20px 50px rgba(0,0,0,0.5),
    0 0 100px rgba(99,102,241,0.1),
    inset 0 1px 0 rgba(255,255,255,0.1);
}
/* 微妙噪点纹理 */
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: url('noise.png') repeat;
  opacity: 0.03;
  pointer-events: none;
}
```

**适用场景**：SaaS/开发者工具/AI 产品/技术类
**避免用于**：消费品/儿童/自然有机类

### Pattern C：极致纯色留白 + 超轻字重

_来源：Supercommon_

**视觉描述**：
- ① 背景：纯黑或纯白，零装饰
- ② 叠层：无
- ③ 布局：居中单列，极致留白（上下 padding 占 viewport 30%+）
- ④ 排版：超大字号（clamp(3rem, 8vw, 6rem)）+ 超轻字重（100-200）+ 全小写。副标题同样极轻，opacity 0.5-0.7
- ⑤ 容器：无任何容器、卡片、按钮
- ⑥ 装饰：无。一切装饰都被视为噪音

**CSS 核心模式**：
```css
body { background: #000; color: #fff; }
h1 {
  font-weight: 100;
  font-size: clamp(3rem, 8vw, 6rem);
  letter-spacing: -0.02em;
  text-transform: lowercase;
}
p {
  font-weight: 200;
  font-size: 1rem;
  line-height: 1.8;
  max-width: 480px;
  margin: 0 auto;
  opacity: 0.7;
}
```

**适用场景**：精密工具/工匠品牌/极简主义产品/个人品牌
**避免用于**：需要快速传达多个卖点的 SaaS/电商

### Pattern D：品牌色渐变背景 + 动态光晕

_来源：GitBook, Lumen Template_

**视觉描述**：
- ① 背景：品牌色渐变（如橙色→黄色、紫色→蓝色），可能有动态光晕/光斑效果
- ② 叠层：无遮罩，渐变本身就是视觉主体
- ③ 布局：居中单列，标题 + 副标题 + CTA
- ④ 排版：白色或深色大号无衬线标题（取决于渐变明度）
- ⑤ 容器：CTA 按钮可能是半透明玻璃态
- ⑥ 装饰：动态光晕/光斑、微妙的粒子效果

**CSS 核心模式**：
```css
.hero {
  background: linear-gradient(135deg, #FF6B35, #FFB347);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}
/* 动态光晕 */
.hero::before {
  content: '';
  position: absolute;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,255,255,0.3), transparent 70%);
  top: -200px; right: -200px;
  border-radius: 50%;
  animation: float 8s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-30px, 20px); }
}
```

**适用场景**：品牌感强的产品/创意工具/文档平台
**避免用于**：企业级/金融/需要严肃感的产品

### Pattern E：新古典衬线体 + 品牌色背景

_来源：Everit (Screenshot Desktop 2)_

**视觉描述**：
- ① 背景：柔和的品牌色（丁香紫 #E8E0F0、薄荷绿、淡珊瑚等）
- ② 叠层：无
- ③ 布局：居中单列，杂志封面式排版
- ④ 排版：超大衬线体标题（80px+），字重 Regular（非 Bold），紧凑行高 1.1。副标题为小号无衬线体
- ⑤ 容器：CTA 按钮为深色实色圆角
- ⑥ 装饰：极少，靠排版本身的张力

**CSS 核心模式**：
```css
.hero {
  background-color: #E8E0F0;
  padding: 120px 0;
}
h1 {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 400;
  font-size: clamp(2rem, 5vw, 4.5rem);
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: #1A1A1A;
}
.subtitle {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.6;
  color: #6B7280;
}
```

**适用场景**：设计工具/创意平台/时尚/编辑类产品
**避免用于**：开发者工具/硬核技术产品

### Pattern F：终端/赛博朋克风

_来源：Terminal X_

**视觉描述**：
- ① 背景：纯黑 #000000，可能有扫描线效果
- ② 叠层：扫描线（repeating-linear-gradient 模拟 CRT）
- ③ 布局：居中单列
- ④ 排版：等宽字体（JetBrains Mono），荧光绿色（#00FF41），标题末尾有闪烁光标 `|`
- ⑤ 容器：无传统卡片，可能有 1px 荧光绿边框的终端窗口
- ⑥ 装饰：Glitch 效果（RGB 偏移）、扫描线、闪烁光标

**CSS 核心模式**：
```css
.hero { background: #000; font-family: 'JetBrains Mono', monospace; }
.cursor { animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }
/* 扫描线 */
.scanlines::after {
  content: '';
  position: absolute; inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,255,65,0.03) 2px, rgba(0,255,65,0.03) 4px
  );
  pointer-events: none;
}
/* Glitch */
.glitch {
  text-shadow: 2px 0 #ff0000, -2px 0 #00ff00;
  animation: glitch 3s infinite;
}
@keyframes glitch {
  0%, 95% { text-shadow: none; }
  96% { text-shadow: 2px 0 #ff0000, -2px 0 #00ff00; }
  97% { text-shadow: -2px 0 #ff0000, 2px 0 #00ff00; }
  100% { text-shadow: none; }
}
```

**适用场景**：金融科技/加密货币/黑客工具/终端产品
**避免用于**：消费品/健康/教育/需要亲和力的产品

### Pattern G：手绘插画背景 + 个性化文案

_来源：Belle Duffner, Callbaba_

**视觉描述**：
- ① 背景：浅色底（米白/浅粉）+ 散布的手绘插画元素（云朵、星星、人物剪影等）
- ② 叠层：无
- ③ 布局：居中单列，文字居中
- ④ 排版：友好的无衬线体，中等字重，个性化文案（"Hello! I'm..."）
- ⑤ 容器：CTA 按钮为温暖色调实色圆角
- ⑥ 装饰：手绘插画是核心视觉元素，增加亲和力和个性

**CSS 核心模式**：
```css
.hero {
  background: #FFF8F0;
  position: relative;
  overflow: hidden;
}
.illustration {
  position: absolute;
  opacity: 0.6;
  /* 散布在不同位置 */
}
.illustration.cloud { top: 10%; left: 5%; }
.illustration.star { top: 20%; right: 10%; }
.illustration.heart { bottom: 15%; left: 15%; }
```

**适用场景**：个人品牌/创意工作室/儿童产品/健康/生活方式
**避免用于**：企业级/金融/需要严肃感的产品

---

## How it Works Section

> 分步骤解释产品运作方式。通常 3-5 步。
> 目标是降低理解成本。

### 常规做法（基线）

大多数 How it Works section：
- 白色/浅灰背景
- 3-4 个步骤水平排列（或编号垂直列表）
- 每步一个图标/数字 + 标题 + 描述
- 偶尔有连接线/箭头

**如果参考图用了全幅摄影背景、暗色容器、内嵌 UI 截图等，应标注为亮点。**

### Pattern A：全幅摄影背景 + 暗色玻璃态卡片

_来源：Junior.ai (test1-revised), Giga AI_

**视觉描述**：
- ① 背景：全幅自然摄影（森林/天空/水面），低饱和度
- ② 叠层：深色半透明叠层（rgba(0,0,0,0.6-0.75)）
- ③ 布局：横向排列 3 张卡片
- ④ 排版：白色标题 + 半透明白色描述
- ⑤ 容器：玻璃态卡片（backdrop-filter: blur + 半透明背景 + 细白边框）
- ⑥ 装饰：卡片内可能嵌入 mock UI 界面截图

**CSS 核心模式**：
```css
.how-it-works {
  background: url('atmosphere.jpg') center/cover;
  position: relative;
}
.how-it-works::after {
  content: ''; position: absolute; inset: 0;
  background: rgba(15, 25, 10, 0.75);
}
.step-card {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
}
```

**适用场景**：需要建立"品质感"/"氛围感"的产品
**避免用于**：信息密度高的企业级产品（会牺牲可读性）

### Pattern B：虚线连接 + 手绘涂鸦注释

_来源：Obviously AI_

**视觉描述**：
- ① 背景：浅色（白/浅灰）
- ② 叠层：无
- ③ 布局：3 步骤横向排列，步骤间有虚线/箭头连接
- ④ 排版：无衬线体标题 + 描述
- ⑤ 容器：每步可能有轻边框卡片
- ⑥ 装饰：手绘涂鸦风格的箭头、圆圈、下划线注释，打破 SaaS 冰冷感

**CSS 核心模式**：
```css
.step-connector {
  border-top: 2px dashed #ccc;
  position: absolute;
  width: 100%;
  top: 50%;
}
.doodle-annotation {
  position: absolute;
  background: url('doodle-arrow.svg') no-repeat;
  width: 60px; height: 40px;
  transform: rotate(-15deg);
  opacity: 0.6;
}
```

**适用场景**：SaaS 产品需要增加亲和力/教育类/入门引导
**避免用于**：高端/奢侈品/需要严肃感的产品

### Pattern C：终端命令行式步骤

_来源：Terminal X_

**视觉描述**：
- ① 背景：纯黑
- ② 叠层：扫描线效果
- ③ 布局：垂直排列，每步以终端命令行形式展示（`$ step-1 --init`）
- ④ 排版：等宽字体，荧光绿色
- ⑤ 容器：终端窗口框（深灰背景 + 顶部三个圆点）
- ⑥ 装饰：Glitch 边缘效果

**CSS 核心模式**：
```css
.terminal-step {
  font-family: 'JetBrains Mono', monospace;
  color: #00FF41;
  padding: 16px 24px;
  border-left: 2px solid rgba(0,255,65,0.3);
}
.terminal-step::before {
  content: '$ ';
  opacity: 0.5;
}
```

**适用场景**：开发者工具/CLI 产品/技术文档
**避免用于**：非技术用户产品

---

## Value Proposition Section

> 传递独特价值，说服用户。

### 常规做法（基线）

- 浅色背景
- 大标题 + 2-3 个价值点（图标+文字）
- 或左文字右图的分栏布局

### Pattern A：居中窄列 + 哲理化文案

_来源：Anthropic, TryHolo, Hobbes_

**视觉描述**：
- ① 背景：浅色（白/米白）
- ② 布局：居中窄列（max-width: 640px），纯文字
- ③ 排版：大号标题（哲理化/愿景化文案，如"You deserve to live fully, longer, and better"）+ 较长的描述段落
- ④ 留白：上下 padding 极大（100px+），营造"呼吸感"
- ⑤ 无图片、无卡片、无装饰——纯靠文字力量

**CSS 核心模式**：
```css
.value-prop {
  max-width: 640px;
  margin: 0 auto;
  padding: 120px 24px;
  text-align: center;
}
.value-prop h2 {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 24px;
}
.value-prop p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #6B7280;
}
```

**适用场景**：需要建立情感连接/品牌理念传达/使命驱动型产品
**避免用于**：需要快速展示功能的工具类产品

### Pattern B：文本渐隐效果

_来源：Hobbes_

**视觉描述**：
- ① 背景：白色
- ② 布局：居中窄列
- ③ 排版：大号标题文字使用渐隐效果——从完全不透明渐变到透明，暗示"无限延伸"
- ④ 这是一个微妙但极具记忆点的排版技巧

**CSS 核心模式**：
```css
.fade-text {
  background: linear-gradient(to right, #1A1A1A 0%, #1A1A1A 60%, transparent 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 600;
}
```

**适用场景**：企业级/AI 产品/需要传达"无限可能"的场景
**避免用于**：需要完整阅读所有文字的场景

---

## Features Section

> 展示产品功能和卖点。

### 常规做法（基线）

- 白色/浅色背景
- 网格布局（2x2 或 3x3）
- 每个 feature 一个卡片（图标+标题+描述）
- 或交替左右的图文展示（bento grid）

### Pattern A：深色 1px 内发光卡片网格

_来源：Linear, Lovart.ai_

**视觉描述**：
- ① 背景：极深色（#0A0A0F）
- ② 布局：Bento Grid，卡片大小不一
- ③ 卡片：背景 rgba(255,255,255,0.03)，1px 边框 rgba(255,255,255,0.06)，顶部内高光 inset 0 1px 0 rgba(255,255,255,0.05)
- ④ 卡片内嵌产品 UI 截图/动画
- ⑤ Hover 时边框亮度增加

**CSS 核心模式**：
```css
.feature-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
  padding: 32px;
  transition: border-color 0.3s;
}
.feature-card:hover {
  border-color: rgba(255,255,255,0.12);
}
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.bento-grid .span-2 { grid-column: span 2; }
```

**适用场景**：SaaS/开发者工具/AI 产品/技术类
**避免用于**：浅色系/消费品/需要亲和力的产品

### Pattern B：白瓷砖新拟态卡片网格

_来源：Spread_

**视觉描述**：
- ① 背景：浅灰白（#F5F5F5）
- ② 布局：极高密度 Bento Grid（4 列），卡片大小不一（1x1, 2x1, 1x2, 2x2）
- ③ 卡片：纯白背景，多层柔和外投影 + 顶部 1px 白色内高光，模拟"白瓷砖"凸起质感
- ④ 卡片内嵌产品 UI 截图、图表、数据可视化
- ⑤ 全浅色一致性——不使用深色 section，靠投影创造层次

**CSS 核心模式**：
```css
.ceramic-card {
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow:
    0 1px 2px rgba(0,0,0,0.04),
    0 4px 8px rgba(0,0,0,0.04),
    0 12px 24px rgba(0,0,0,0.06),
    inset 0 1px 0 rgba(255,255,255,1);
  padding: 24px;
}
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 12px;
}
.span-2x1 { grid-column: span 2; }
.span-1x2 { grid-row: span 2; }
.span-2x2 { grid-column: span 2; grid-row: span 2; }
```

**适用场景**：数据产品/仪表盘/组件库展示/需要高信息密度的产品
**避免用于**：极简主义/需要大量留白的品牌页

### Pattern C：图片叠加文字卡片

_来源：TryHolo_

**视觉描述**：
- ① 背景：白色
- ② 布局：3 列等宽卡片
- ③ 卡片：全幅图片作为背景，底部深色渐变遮罩，白色文字叠加在底部
- ④ 图片内容与功能主题相关（生活场景/产品使用场景）

**CSS 核心模式**：
```css
.feature-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px;
  color: #fff;
}
.feature-card::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
  z-index: 1;
}
.feature-card img {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  z-index: 0;
}
.feature-card h3, .feature-card p {
  position: relative;
  z-index: 2;
}
```

**适用场景**：生活方式/健康/旅行/需要情感共鸣的产品
**避免用于**：纯技术产品/开发者工具

### Pattern D：玻璃态功能卡片

_来源：Lumen Template_

**视觉描述**：
- ① 背景：渐变色或深色
- ② 布局：网格或列表
- ③ 卡片：半透明背景 + backdrop-filter: blur + 细白边框，模拟毛玻璃效果
- ④ 卡片内有图标 + 标题 + 描述

**CSS 核心模式**：
```css
.glass-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 32px;
}
```

**适用场景**：现代 SaaS/AI 产品/需要"未来感"的产品
**避免用于**：需要高对比度/无障碍优先的产品

### Pattern E：左右分栏交替展示

_来源：Anthropic, ElevenLabs, Keytail.ai_

**视觉描述**：
- ① 背景：浅色
- ② 布局：左文字右图 → 右文字左图 → 交替
- ③ 每个功能占一个完整的 section 高度
- ④ 图片为产品 UI 截图或数据可视化
- ⑤ 文字侧有小标签（"FEATURE"）+ 大标题 + 描述

**CSS 核心模式**：
```css
.feature-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
  padding: 80px 0;
}
.feature-row:nth-child(even) {
  direction: rtl;
}
.feature-row:nth-child(even) > * {
  direction: ltr;
}
```

**适用场景**：通用，适合大多数产品
**避免用于**：需要高密度展示的场景

---

## Testimonial Section

> 用户评价，建立社会认证。

### 常规做法（基线）

- 浅色背景
- 卡片排列或走马灯
- 引号装饰 + 用户头像 + 姓名/公司

### Pattern A：居中大号引言 + 头像

_来源：TryHolo, Anthropic_

**视觉描述**：
- ① 背景：浅色
- ② 布局：居中窄列
- ③ 排版：大号引言文字（24-32px），字重 Medium，深色。引号装饰
- ④ 下方为圆形头像 + 姓名 + 职位
- ⑤ 信息密度低，留白充裕

**CSS 核心模式**：
```css
.testimonial {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  padding: 100px 24px;
}
.testimonial blockquote {
  font-size: clamp(1.25rem, 2.5vw, 1.75rem);
  font-weight: 500;
  line-height: 1.5;
  color: #1A1A1A;
  position: relative;
  padding-left: 40px;
}
.testimonial blockquote::before {
  content: '\201C';
  position: absolute;
  left: 0; top: -10px;
  font-size: 60px;
  color: #1A1A1A;
  opacity: 0.3;
}
.testimonial .avatar {
  width: 48px; height: 48px;
  border-radius: 50%;
  margin: 24px auto 8px;
}
```

**适用场景**：通用
**避免用于**：需要展示大量评价的场景（用卡片网格更好）

### Pattern B：高饱和度渐变背景引言

_来源：Linear_

**视觉描述**：
- ① 背景：高饱和度渐变（紫→蓝→青），在全深色页面中形成唯一的"色彩爆发"
- ② 布局：居中窄列
- ③ 排版：白色大号引言，字重 Medium
- ④ 这个 section 的核心价值是打破深色页面的视觉疲劳

**CSS 核心模式**：
```css
.quote-section {
  background: linear-gradient(135deg, #7C3AED, #3B82F6, #06B6D4);
  padding: 120px 24px;
}
.quote-section blockquote {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: 500;
  color: white;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}
```

**适用场景**：深色系页面中需要"视觉呼吸"的位置
**避免用于**：浅色系页面（会显得突兀）

---

## Call to Action Section

> 最终转化推动。

### 常规做法（基线）

- 深色/品牌色背景
- 大标题 + 副标题 + 按钮
- 内容居中，简洁

### Pattern A：全幅摄影背景 + 首尾呼应

_来源：Hobbes, Framer (Kero Template)_

**视觉描述**：
- ① 背景：全幅自然摄影（日落/云海/星空），与 Hero 的摄影主题呼应
- ② 叠层：深色半透明叠层
- ③ 布局：居中单列
- ④ 排版：白色大号标题 + CTA 按钮
- ⑤ 与 Hero 形成叙事闭环——"从这里开始，到这里行动"

**CSS 核心模式**：
```css
.cta {
  position: relative;
  min-height: 60vh;
  background: url('sunset.jpg') center/cover;
  display: flex;
  align-items: center;
  justify-content: center;
}
.cta::after {
  content: '';
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.5);
}
.cta-content {
  position: relative; z-index: 1;
  text-align: center;
  color: white;
}
```

**适用场景**：品牌页/企业级/需要情感收尾的页面
**避免用于**：工具类/开发者文档

### Pattern B：色彩包夹回归

_来源：Everit (Screenshot Desktop 2)_

**视觉描述**：
- ① 背景：与 Hero 相同的品牌色（如丁香紫），形成"品牌色-白色-白色-品牌色"的包夹结构
- ② 布局：居中单列
- ③ 排版：衬线体大标题 + CTA 按钮
- ④ 核心价值：首尾色彩一致创造叙事闭环和品牌记忆

**CSS 核心模式**：
```css
/* Hero 和 CTA 使用相同背景色 */
.hero, .cta { background-color: #E8E0F0; }
/* 中间所有 section 使用白色 */
.content-sections { background-color: #FFFFFF; }
```

**适用场景**：品牌感强的产品/编辑类/设计类
**避免用于**：需要多种背景色变化的长页面

### Pattern C：品牌色实色背景

_来源：Obviously AI_

**视觉描述**：
- ① 背景：品牌主色（蓝色/紫色等）实色填充
- ② 布局：居中单列
- ③ 排版：白色大标题 + 白色/半透明 CTA 按钮
- ④ 简洁直接，无装饰

**CSS 核心模式**：
```css
.cta {
  background: #2563EB;
  padding: 100px 24px;
  text-align: center;
  color: white;
}
.cta h2 {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: 700;
  margin-bottom: 24px;
}
.cta .btn {
  background: white;
  color: #2563EB;
  padding: 16px 32px;
  border-radius: 8px;
  font-weight: 600;
}
```

**适用场景**：通用 SaaS
**避免用于**：极简主义/需要微妙感的品牌

---

## Pricing Section

> 价格方案展示。

### 常规做法（基线）

- 2-3 列定价卡片
- 推荐方案高亮（边框/背景色/角标）
- 功能对比列表

### Pattern A：渐变背景 + 玻璃态定价卡片

_来源：Lumen Template_

**视觉描述**：
- ① 背景：柔和渐变（紫→蓝）
- ② 卡片：玻璃态（半透明 + blur），推荐方案有更亮的边框或实色背景
- ③ 价格数字特大号，功能列表用勾选图标

**CSS 核心模式**：
```css
.pricing {
  background: linear-gradient(135deg, #667eea, #764ba2);
  padding: 100px 24px;
}
.pricing-card {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px;
  padding: 40px;
  color: white;
}
.pricing-card.recommended {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.3);
  transform: scale(1.05);
}
.price {
  font-size: 3rem;
  font-weight: 700;
}
```

**适用场景**：现代 SaaS/需要视觉吸引力的定价页
**避免用于**：企业级/需要严肃对比的场景

### Pattern B：白底卡片 + 推荐方案深色高亮

_来源：TryHolo_

**视觉描述**：
- ① 背景：白色
- ② 卡片：白色背景 + 轻微阴影，推荐方案使用深色/品牌色背景反转
- ③ 功能列表前有勾选图标，支付方式图标

**CSS 核心模式**：
```css
.pricing-card {
  background: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  padding: 40px;
}
.pricing-card.recommended {
  background: #1A1A1A;
  color: #FFFFFF;
}
```

**适用场景**：通用
**避免用于**：深色系页面

---

## Stats / Metrics Section

> 数据展示，建立信任。

### 常规做法（基线）

- 3-4 个大号数字 + 单位 + 描述
- 通常水平排列
- 可能有简单的分割线

### Pattern A：黑白极端反转

_来源：Terminal X_

**视觉描述**：
- ① 在全深色页面中，Stats section 突然切换为纯白背景
- ② 黑色大号等宽数字 + 描述
- ③ 这种黑白硬切是整个页面最强的视觉冲击
- ④ 核心价值：用极端对比让数据成为不可忽视的焦点

**CSS 核心模式**：
```css
/* 在深色页面中的白色 Stats section */
.stats {
  background: #FFFFFF;
  color: #000000;
  padding: 80px 24px;
}
.stat-number {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
}
```

**适用场景**：深色系页面中需要强调数据的位置
**避免用于**：浅色系页面（失去对比效果）

### Pattern B：混淆文本暗示数据安全

_来源：TryHolo_

**视觉描述**：
- ① 深色背景
- ② 标题为白色粗体，下方的"数据"文本使用半透明白色 + 乱码内容
- ③ 视觉上暗示加密和隐私保护

**CSS 核心模式**：
```css
.obfuscated-text {
  font-family: monospace;
  color: rgba(255,255,255,0.5);
  font-size: 3em;
  font-weight: bold;
  text-align: center;
  word-break: break-all;
}
```

**适用场景**：安全/隐私/金融产品
**避免用于**：需要展示真实数据的场景

---

## Brands / Logos Section

> Logo 墙，展示合作伙伴/客户。

### 常规做法（基线）

- 单行或双行 logo 排列
- 灰度/降低对比度处理
- 极简背景

### Pattern A：灰度 Logo 墙 + "Trusted by" 标签

_来源：Obviously AI, Linear, ElevenLabs_

**视觉描述**：
- ① 背景：与上下 section 一致（浅色或深色）
- ② Logo 全部灰度处理（filter: grayscale(1)），降低视觉权重
- ③ 上方有小标签 "Trusted by leading teams" 或类似文案
- ④ Logo 间距均匀，可能有无限滚动动画

**CSS 核心模式**：
```css
.brands {
  padding: 40px 0;
  text-align: center;
}
.brands .label {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #6B7280;
  margin-bottom: 24px;
}
.brands img {
  filter: grayscale(1);
  opacity: 0.5;
  height: 24px;
  margin: 0 24px;
  transition: opacity 0.3s;
}
.brands img:hover {
  opacity: 1;
  filter: grayscale(0);
}
/* 无限滚动 */
.brands-track {
  display: flex;
  animation: scroll 30s linear infinite;
}
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

**适用场景**：通用
**避免用于**：无

---

## FAQ Section

> 常见问题。

### 常规做法（基线）

- 手风琴/折叠面板
- 浅色背景
- 居中窄列

### Pattern A：极简手风琴 + 细分割线

_来源：TryHolo_

**视觉描述**：
- ① 背景：白色
- ② 布局：居中窄列（max-width: 720px）
- ③ 问题间用细分割线分隔
- ④ 问题右侧有 + 图标（展开时变 -）
- ⑤ 底部可能有"查看全部"按钮

**CSS 核心模式**：
```css
.faq-item {
  border-bottom: 1px solid #E5E7EB;
  padding: 20px 0;
}
.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 500;
  font-size: 1.1rem;
}
.faq-icon {
  font-size: 1.5rem;
  transition: transform 0.3s;
}
.faq-item.open .faq-icon {
  transform: rotate(45deg);
}
.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.faq-item.open .faq-answer {
  max-height: 500px;
}
```

**适用场景**：通用
**避免用于**：无

---

## Footer Section

> 页脚导航。

### 常规做法（基线）

- 深色背景
- 多列链接 + logo + 版权信息
- 社交媒体图标

### Pattern A：深色多列 + 社交图标

_来源：Anthropic, TryHolo, ElevenLabs_

**视觉描述**：
- ① 背景：深灰/近黑（#1A1A1A）
- ② 布局：左侧 Logo + 右侧多列链接
- ③ 底部版权信息 + 社交媒体图标
- ④ 链接为浅灰色，hover 变白

**CSS 核心模式**：
```css
.footer {
  background: #1A1A1A;
  color: #9CA3AF;
  padding: 64px 24px 32px;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr repeat(4, 1fr);
  gap: 48px;
}
.footer a {
  color: #9CA3AF;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}
.footer a:hover { color: #FFFFFF; }
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  margin-top: 48px;
  padding-top: 24px;
  font-size: 0.75rem;
}
```

**适用场景**：通用
**避免用于**：无

---

## Navigation Section

> 顶部导航栏。

### 常规做法（基线）

- 固定在顶部
- 左侧 Logo + 右侧导航链接 + CTA 按钮
- 白色/透明背景

### Pattern A：透明导航 + 滚动后变实色

_来源：多个案例通用模式_

**CSS 核心模式**：
```css
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 16px 24px;
  background: transparent;
  transition: background 0.3s, backdrop-filter 0.3s;
}
.nav.scrolled {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
```

---

## 跨 Section 模式

> 不属于单个 section，而是多个 section 之间的关系模式。

### 明暗交替节奏

最常见的页面节奏模式：

| 模式 | 节奏 | 来源 | 适用场景 |
|------|------|------|---------|
| 经典交替 | 浅→浅→深→浅→浅→深 | TryHolo, Giga AI | 通用 |
| 全深色 | 深→深→深→深→深 | Supercommon, Akash Tyagi | 极简/作品集/暗黑科技 |
| 全浅色 | 浅→浅→浅→浅→浅 | Spread, Obviously AI | 高密度信息/SaaS |
| 深色+色彩爆发 | 深→深→**彩**→深→深 | Linear | 深色系需要"呼吸"时 |
| 色彩包夹 | **彩**→浅→浅→浅→**彩** | Everit | 品牌感强/编辑风 |
| 黑白硬切 | 深→深→**浅**→深→深 | Terminal X | 需要极端对比/数据强调 |

### Section 过渡方式

| 方式 | 描述 | CSS | 适用场景 |
|------|------|-----|---------|
| 硬切 | 直接颜色切换 | `background-color` 变化 | 大多数情况 |
| 渐变过渡 | 上一 section 底部渐变到下一 section 颜色 | `linear-gradient` | 柔和的品牌页 |
| 波浪/曲线 | SVG 波浪形分割 | `clip-path` 或 SVG | 有机/自然风格 |
| 撕裂纸张 | 不规则边缘 | SVG mask | 手工/复古风格 |
| 重叠 | 下一 section 的内容向上伸入上一 section | `margin-top: -80px` | 现代/动感 |

### 白底托黑卡 vs 黑底托白卡

两种经典的容器-背景对比策略：

**白底托黑卡**（来源：Hobbes）：
```css
.section { background: #FFFFFF; }
.dark-card {
  background: #1A1A1A;
  color: #FFFFFF;
  border-radius: 20px;
  padding: 48px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
```

**黑底托白卡**（来源：Akash Tyagi）：
```css
.section { background: #121212; }
.light-card {
  background: #FFFFFF;
  color: #1A1A1A;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
```

### 排版策略

| 策略 | 描述 | 来源 | 适用场景 |
|------|------|------|---------|
| 衬线+无衬线混排 | 标题用衬线体，正文用无衬线体 | Everit, Framer | 编辑风/高端/新古典 |
| 纯无衬线 | 全站无衬线体 | Linear, Obviously AI, Spread | 现代/科技/SaaS |
| 等宽字体主导 | 标题和正文都用等宽字体 | Terminal X | 开发者/终端/赛博朋克 |
| 超轻字重 | font-weight: 100-200 | Supercommon | 极简/精密工具/工匠 |
| 全小写 | text-transform: lowercase | Supercommon | 极简/谦逊/工匠 |

---

_本文档为活文档，随标杆案例拆解持续丰富。_
_最后更新：2026-04-01_
_案例数量：28（20 自动分析 + 8 手动分析）_
_Pattern 数量：Hero 7 / How it Works 3 / Value Proposition 2 / Features 5 / Testimonial 2 / CTA 3 / Pricing 2 / Stats 2 / Brands 1 / FAQ 1 / Footer 1 / Nav 1 / 跨 Section 6_
