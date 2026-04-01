#!/usr/bin/env python3
"""
Section Storyboard 批量分析脚本
使用 Gemini API 对设计参考图做 Section-First 三层递进分析，
结果自动追加到 section-pattern-codex-cases.md

用法：
  python3 analyze_cases.py                          # 分析 cases/ 文件夹下所有图片
  python3 analyze_cases.py --folder /path/to/images # 指定图片文件夹
  python3 analyze_cases.py --file one-image.png     # 分析单张图片
  python3 analyze_cases.py --url https://junior.ai  # 自动截图并分析（需要 playwright）
  python3 analyze_cases.py --urls urls.txt           # 批量截图分析（每行一个 URL）
  python3 analyze_cases.py --dry-run                # 只显示会分析哪些图片，不调 API
"""

import os
import sys
import json
import base64
import time
import argparse
import ssl
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBEcTLJgm5blgKYJncpvqHtbqBI8q2eG88")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# 默认图片文件夹（相对于脚本所在目录的上级）
DEFAULT_CASES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "cases")

# 截图保存文件夹
SCREENSHOTS_FOLDER = os.path.join(DEFAULT_CASES_FOLDER, "screenshots")

# 输出文件
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "section-pattern-codex-cases.md")

# 支持的图片格式
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

# 请求间隔（秒），避免触发限流
REQUEST_INTERVAL = 4

# 截图视口宽度（像素）
VIEWPORT_WIDTH = 1440

# 截图最大高度限制（像素），避免超长页面截图过大
MAX_SCREENSHOT_HEIGHT = 12000


# ============================================================
# 分析 Prompt
# ============================================================

ANALYSIS_PROMPT = """你是一位受过专业训练的视觉风格分析师，采用 Section-First 三层递进方法论。
请对这张设计参考图（Landing Page 截图）做完整的三层递进分析。

## 第一层：Section Storyboard（100% 忠实拆解）

从上到下逐 section 分析这张图。

步骤 1：识别所有 section 的类型，使用以下分类：
Hero / Value Proposition / Features / How it Works / Testimonial /
Brands / Stats / Pricing / Case Study / Resources / FAQ /
Call to Action / Footer / About Us / Video-Demo / Comparison / Timeline / Navigation

步骤 2：对每个 section，按以下七个维度描述（全部覆盖，没有的写"无"）：

① 背景处理：全幅摄影/纯色/渐变/视频/纹理？具体描述内容、色调、氛围
② 叠层与遮罩：半透明叠层？颜色和透明度？渐变遮罩？
③ 内容布局：居中单列/左右分栏/网格卡片？内容区宽度？对齐方式？
④ 排版细节：标题字体类型（衬线/无衬线）、字号感受（特大/大/中）、字重、颜色；副标题/描述
⑤ 容器与卡片：是否有卡片？实色/半透明/玻璃态/线框？圆角、阴影、内部结构
⑥ 装饰与细节：装饰元素？分割线？section 间过渡方式（硬切/渐变/波浪/重叠）
⑦ 与前后 section 的关系：明暗对比？密度变化？情绪变化？

步骤 3：画页面节奏图（ASCII）：
```
Section:  [S1]    [S2]    [S3]    ...
明暗:     [浅/深]  [浅/深]  [浅/深]
密度:     低/中/高
```

## 第二层：亮点标注与设计逻辑

Q1：记忆点 — 如果只能记住这个设计的一个画面，是哪个？为什么？

Q2：亮眼模块（标注 2-3 个）— 对每个输出：
- what: 做了什么不寻常的事
- how: 通过什么视觉手段实现
- why: 为什么有效
- css_pattern: 核心 CSS 实现模式（给出可用的代码）
- priority: 实现时最需要抓住的关键点

Q3：页面叙事总结 — 这个页面如何引导用户从首屏到 CTA？

## 第三层：全局原子 Token

提取全局 Token，注意区分深色/浅色 section：

```yaml
colors:
  surface_light: { hex: "#xxx", note: "浅色 section 背景" }
  surface_dark: { hex: "#xxx", note: "深色 section 背景" }
  primary: { hex: "#xxx", note: "品牌色" }
  accent: { hex: "#xxx", note: "强调色" }
  text_on_light: { hex: "#xxx" }
  text_on_dark: { hex: "#xxx" }

typography:
  heading: "字体分类 + 特征"
  body: "字体分类 + 特征"

form:
  border_radius: "具体描述"
  decoration: "具体描述"
```

情感关键词：3-5 个词
风格一句话总结：一句话定义视觉身份

---
请用中文输出，格式清晰，使用 markdown 格式。描述要具体到可据此还原，不要抽象概括。"""


# ============================================================
# 工具函数
# ============================================================

def get_mime_type(ext: str) -> str:
    """根据扩展名返回 MIME 类型"""
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return mime_map.get(ext.lower(), "image/png")


def encode_image(image_path: str) -> tuple[str, str]:
    """读取图片并返回 (base64_data, mime_type)"""
    ext = Path(image_path).suffix.lower()
    mime_type = get_mime_type(ext)
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, mime_type


def call_gemini(image_b64: str, mime_type: str, prompt: str) -> str:
    """调用 Gemini API 做多模态分析"""
    payload = {
        "contents": [{
            "parts": [
                {
                    "inlineData": {
                        "mimeType": mime_type,
                        "data": image_b64,
                    }
                },
                {
                    "text": prompt,
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 16384,
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GEMINI_API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    # SSL 绕过（部分网络环境需要）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            # 提取文本内容
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                texts = [p["text"] for p in parts if "text" in p]
                return "\n".join(texts)
            return "[错误] Gemini 返回了空结果"
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        if e.code == 429:
            return f"[限流] 429 Too Many Requests - 请等待几分钟后重试\n{body}"
        return f"[HTTP 错误] {e.code}: {body}"
    except Exception as e:
        return f"[错误] {type(e).__name__}: {e}"


def find_images(folder: str) -> list[str]:
    """扫描文件夹，返回所有支持的图片路径"""
    images = []
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"❌ 文件夹不存在: {folder}")
        return images

    for f in sorted(folder_path.iterdir()):
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(str(f))
    return images


def parse_case_name(image_path: str) -> str:
    """从文件名提取案例名称"""
    stem = Path(image_path).stem
    # 将连字符和下划线替换为空格，首字母大写
    return stem.replace("-", " ").replace("_", " ").title()


def load_metadata(folder: str) -> dict:
    """加载 metadata.json（如果存在），获取网站 URL 等信息"""
    meta_path = os.path.join(folder, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ============================================================
# URL 截图功能
# ============================================================

def url_to_filename(url: str) -> str:
    """将 URL 转为合法文件名"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    # 用域名作为文件名主体
    domain = parsed.netloc.replace("www.", "")
    # 如果有路径，附加路径部分
    path_part = parsed.path.strip("/").replace("/", "-")
    name = domain
    if path_part:
        name = f"{domain}-{path_part}"
    # 清理非法字符
    name = "".join(c if c.isalnum() or c in "-_." else "-" for c in name)
    # 去掉连续的横杠
    while "--" in name:
        name = name.replace("--", "-")
    return name.strip("-")


def url_to_case_name(url: str) -> str:
    """从 URL 生成可读的案例名称"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    # 提取主域名（去掉 TLD）
    parts = domain.split(".")
    if len(parts) >= 2:
        name = parts[-2]  # 取主域名
    else:
        name = domain
    return name.capitalize()


def capture_screenshot(url: str, output_path: str, viewport_width: int = VIEWPORT_WIDTH) -> bool:
    """
    用 Playwright 截取网页全页截图。
    返回 True 表示成功，False 表示失败。
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  ❌ 未安装 playwright，请运行：")
        print("     pip3 install playwright && playwright install chromium")
        return False

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": viewport_width, "height": 900},
                device_scale_factor=2,  # 2x 高清截图
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            print(f"  🌐 正在加载: {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception:
                # networkidle 超时时降级为 load
                print(f"  ⚠️  networkidle 超时，降级为 load 事件")
                try:
                    page.goto(url, wait_until="load", timeout=20000)
                except Exception as e:
                    print(f"  ❌ 页面加载失败: {e}")
                    browser.close()
                    return False

            # 等待额外渲染（动画/懒加载）
            page.wait_for_timeout(2000)

            # 关闭可能的 cookie 弹窗或 overlay
            _dismiss_overlays(page)

            # 滚动到底部触发懒加载，然后回到顶部
            _scroll_full_page(page)

            # 获取页面实际高度
            page_height = page.evaluate("() => document.documentElement.scrollHeight")
            clipped_height = min(page_height, MAX_SCREENSHOT_HEIGHT)

            if page_height > MAX_SCREENSHOT_HEIGHT:
                print(f"  ⚠️  页面很长 ({page_height}px)，截图限制为 {MAX_SCREENSHOT_HEIGHT}px")

            # 全页截图
            print(f"  📸 截图中... ({viewport_width}x{clipped_height}px)")
            page.screenshot(
                path=output_path,
                full_page=True if page_height <= MAX_SCREENSHOT_HEIGHT else False,
                clip={"x": 0, "y": 0, "width": viewport_width, "height": clipped_height}
                if page_height > MAX_SCREENSHOT_HEIGHT else None,
                type="png",
            )

            browser.close()

        file_size = os.path.getsize(output_path) / 1024
        print(f"  ✅ 截图已保存: {os.path.basename(output_path)} ({file_size:.0f} KB)")
        return True

    except Exception as e:
        print(f"  ❌ 截图失败: {type(e).__name__}: {e}")
        return False


def _dismiss_overlays(page):
    """尝试关闭常见的 cookie 弹窗和遮罩"""
    dismiss_selectors = [
        # Cookie 同意按钮
        "button:has-text('Accept')",
        "button:has-text('Got it')",
        "button:has-text('OK')",
        "button:has-text('I agree')",
        "button:has-text('Close')",
        "[class*='cookie'] button",
        "[id*='cookie'] button",
        "[class*='consent'] button",
        "[class*='banner'] button[class*='close']",
        # 通用关闭按钮
        "[aria-label='Close']",
        "[aria-label='Dismiss']",
    ]
    for selector in dismiss_selectors:
        try:
            el = page.query_selector(selector)
            if el and el.is_visible():
                el.click()
                page.wait_for_timeout(500)
                break  # 只关闭第一个找到的
        except Exception:
            continue


def _scroll_full_page(page):
    """滚动到底部触发懒加载内容，然后回顶部"""
    try:
        page.evaluate("""
            async () => {
                const delay = ms => new Promise(r => setTimeout(r, ms));
                const height = document.documentElement.scrollHeight;
                const step = window.innerHeight;
                for (let y = 0; y < height; y += step) {
                    window.scrollTo(0, y);
                    await delay(300);
                }
                // 回到顶部
                window.scrollTo(0, 0);
                await delay(500);
            }
        """)
    except Exception:
        pass


def process_urls(urls: list[str], dry_run: bool = False) -> list[dict]:
    """
    对 URL 列表做截图，返回 [{path, name, url}, ...] 供后续分析。
    截图保存在 cases/screenshots/ 下。
    """
    os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)

    tasks = []
    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        # 确保有协议
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        filename = url_to_filename(url) + ".png"
        filepath = os.path.join(SCREENSHOTS_FOLDER, filename)
        case_name = url_to_case_name(url)

        tasks.append({
            "url": url,
            "path": filepath,
            "name": case_name,
            "filename": filename,
        })

    if not tasks:
        print("❌ 没有有效的 URL")
        return []

    print(f"\n📋 待截图 {len(tasks)} 个网站:")
    for i, t in enumerate(tasks, 1):
        print(f"   {i}. {t['name']} — {t['url']}")

    if dry_run:
        print("\n🏃 Dry run 模式，不执行截图和分析")
        return []

    print(f"\n⏱️  预计耗时: {len(tasks) * 25:.0f} 秒")
    print(f"   (每个 ~15 秒截图 + ~10 秒分析)")
    print()

    completed = []
    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}/{len(tasks)}] 截图: {task['name']} ({task['url']})")

        # 如果已有截图且不超过 1 天，跳过截图
        if os.path.exists(task["path"]):
            age_hours = (time.time() - os.path.getmtime(task["path"])) / 3600
            if age_hours < 24:
                file_size = os.path.getsize(task["path"]) / 1024
                print(f"  ⏭️  使用已有截图 ({file_size:.0f} KB, {age_hours:.1f}h 前)")
                completed.append(task)
                continue
            else:
                print(f"  🔄 截图已过期 ({age_hours:.0f}h)，重新截取")

        success = capture_screenshot(task["url"], task["path"])
        if success:
            completed.append(task)
        else:
            print(f"  ⚠️  跳过此 URL")

    return completed


# ============================================================
# 主流程
# ============================================================

def analyze_single(image_path: str, case_name: str = None, url: str = None) -> str:
    """分析单张图片，返回格式化的 markdown"""
    if case_name is None:
        case_name = parse_case_name(image_path)

    file_size = os.path.getsize(image_path) / 1024  # KB
    print(f"  📸 读取图片: {os.path.basename(image_path)} ({file_size:.0f} KB)")

    image_b64, mime_type = encode_image(image_path)
    print(f"  🤖 调用 Gemini API 分析中...")

    result = call_gemini(image_b64, mime_type, ANALYSIS_PROMPT)

    # 检查是否有错误
    if result.startswith("[错误]") or result.startswith("[限流]") or result.startswith("[HTTP"):
        print(f"  ⚠️  {result[:80]}")
        return None

    # 格式化输出
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    url_line = f"\n**来源**: [{url}]({url})" if url else ""
    file_line = f"\n**文件**: `{os.path.basename(image_path)}`"

    output = f"""


---

## 📋 案例：{case_name}

_分析时间：{timestamp}_{url_line}{file_line}

{result}
"""
    return output


def write_results(results: list[str], output_path: str, success_count: int):
    """将分析结果写入输出文件"""
    if not results:
        return

    header = f"""# Section Pattern Codex — 案例分析结果

> 由 `analyze_cases.py` 自动生成
> 分析模型：{GEMINI_MODEL}
> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}
> 分析数量：{success_count} 个案例

---
"""
    # 如果文件已存在，追加内容；否则创建新文件
    if os.path.exists(output_path):
        with open(output_path, "a", encoding="utf-8") as f:
            for r in results:
                f.write(r)
        print(f"\n📝 追加写入: {output_path}")
    else:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
            for r in results:
                f.write(r)
        print(f"\n📝 创建文件: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Section Storyboard 批量分析脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 分析本地图片
  python3 analyze_cases.py --file screenshot.png --name "Junior.ai"
  python3 analyze_cases.py --folder ./my-references/

  # 自动截图并分析网站
  python3 analyze_cases.py --url https://junior.ai
  python3 analyze_cases.py --url https://linear.app --url https://vercel.com
  python3 analyze_cases.py --urls urls.txt

  # 预览模式
  python3 analyze_cases.py --url https://junior.ai --dry-run
        """,
    )
    parser.add_argument("--folder", default=DEFAULT_CASES_FOLDER, help="图片文件夹路径")
    parser.add_argument("--file", help="分析单张图片")
    parser.add_argument("--output", default=OUTPUT_FILE, help="输出 markdown 文件路径")
    parser.add_argument("--dry-run", action="store_true", help="只显示会分析哪些图片/URL")
    parser.add_argument("--url", action="append", dest="urls", help="网站 URL（可多次使用）")
    parser.add_argument("--urls", dest="urls_file", help="包含 URL 列表的文件（每行一个）")
    parser.add_argument("--name", help="单张图片/单个 URL 的案例名称")
    args = parser.parse_args()

    print("=" * 60)
    print("🎨 Section Storyboard 批量分析")
    print(f"   模型: {GEMINI_MODEL}")
    print(f"   输出: {args.output}")
    print("=" * 60)

    # ---- URL 模式 ----
    url_list = []

    # 从 --url 参数收集
    if args.urls:
        url_list.extend(args.urls)

    # 从 --urls 文件收集
    if args.urls_file:
        if not os.path.exists(args.urls_file):
            print(f"❌ URL 文件不存在: {args.urls_file}")
            sys.exit(1)
        with open(args.urls_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    url_list.append(line)

    if url_list:
        # URL 截图模式
        print(f"\n🌐 URL 截图模式")
        tasks = process_urls(url_list, dry_run=args.dry_run)

        if args.dry_run:
            sys.exit(0)

        if not tasks:
            print("❌ 没有成功的截图")
            sys.exit(1)

        # 分析截图
        results = []
        success_count = 0
        fail_count = 0

        for i, task in enumerate(tasks, 1):
            # 如果只有一个 URL 且指定了 --name，使用指定名称
            case_name = args.name if len(tasks) == 1 and args.name else task["name"]

            print(f"\n[{i}/{len(tasks)}] 分析: {case_name}")
            result = analyze_single(task["path"], case_name, task["url"])

            if result:
                results.append(result)
                success_count += 1
                print(f"  ✅ 完成")
            else:
                fail_count += 1
                print(f"  ❌ 分析失败")

            # 请求间隔
            if i < len(tasks):
                print(f"  ⏳ 等待 {REQUEST_INTERVAL} 秒...")
                time.sleep(REQUEST_INTERVAL)

        write_results(results, args.output, success_count)

        print(f"\n{'=' * 60}")
        print(f"🎉 分析完成!")
        print(f"   ✅ 成功: {success_count}")
        if fail_count:
            print(f"   ❌ 失败: {fail_count}")
        print(f"   📄 结果: {args.output}")
        print(f"   📸 截图: {SCREENSHOTS_FOLDER}")
        print(f"{'=' * 60}")
        sys.exit(0)

    # ---- 图片模式（原有逻辑） ----

    # 单张模式
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        images = [args.file]
    else:
        # 确保文件夹存在
        os.makedirs(args.folder, exist_ok=True)
        images = find_images(args.folder)

    if not images:
        print(f"\n📂 文件夹 {args.folder} 中没有找到图片")
        print(f"   支持格式: {', '.join(SUPPORTED_EXTENSIONS)}")
        print(f"\n💡 提示:")
        print(f"   1. 本地图片: 把截图放到 cases/ 文件夹中")
        print(f"   2. 在线网站: 使用 --url https://example.com 自动截图分析")
        sys.exit(0)

    # 加载 metadata
    metadata = load_metadata(args.folder) if not args.file else {}

    print(f"\n📋 找到 {len(images)} 张图片:")
    for i, img in enumerate(images, 1):
        basename = os.path.basename(img)
        meta = metadata.get(basename, {})
        name = meta.get("name", parse_case_name(img))
        size = os.path.getsize(img) / 1024
        print(f"   {i}. {name} ({size:.0f} KB) — {basename}")

    if args.dry_run:
        print("\n🏃 Dry run 模式，不调用 API")
        sys.exit(0)

    print(f"\n⏱️  预计耗时: {len(images) * (REQUEST_INTERVAL + 10):.0f} 秒")
    print(f"   (每张 ~10 秒分析 + {REQUEST_INTERVAL} 秒间隔)")
    print()

    # 逐张分析
    results = []
    success_count = 0
    fail_count = 0

    for i, img_path in enumerate(images, 1):
        basename = os.path.basename(img_path)
        meta = metadata.get(basename, {})
        case_name = args.name if args.file and args.name else meta.get("name", parse_case_name(img_path))
        url_info = meta.get("url") if not args.file else None

        print(f"\n[{i}/{len(images)}] 分析: {case_name}")
        result = analyze_single(img_path, case_name, url_info)

        if result:
            results.append(result)
            success_count += 1
            print(f"  ✅ 完成")
        else:
            fail_count += 1
            print(f"  ❌ 失败")

        # 请求间隔（最后一张不等待）
        if i < len(images):
            print(f"  ⏳ 等待 {REQUEST_INTERVAL} 秒...")
            time.sleep(REQUEST_INTERVAL)

    write_results(results, args.output, success_count)

    # 总结
    print(f"\n{'=' * 60}")
    print(f"🎉 分析完成!")
    print(f"   ✅ 成功: {success_count}")
    if fail_count:
        print(f"   ❌ 失败: {fail_count}")
    print(f"   📄 结果: {args.output}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
