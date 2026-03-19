#!/usr/bin/env python3
"""
download-figma-icons.py  —  Figma REST API 图标批量下载脚本（方案 B · 兜底）

当 download_figma_images MCP 工具因路径沙箱无法写入时，改用本脚本。

用法:
    FIGMA_TOKEN="figd_xxx" python3 scripts/download-figma-icons.py
    或:
    python3 scripts/download-figma-icons.py --token figd_xxx

配置:
    修改下方 FILE_KEY 和 ICON_NODES 后运行：
    - FILE_KEY   : 从 Figma URL 获取，figma.com/design/<FILE_KEY>/...
    - ICON_NODES : { 'nodeId': '文件名（无扩展名）' }
                   nodeId 必须是 instance 节点 ID，不是 Component 定义节点
                   （Component 定义节点 API 返回 null）

踩坑记录:
    - API 返回的 key 是原始冒号格式（如 "5000:76419"），不是连字符
    - Component 定义节点返回 null → 改用对应的 instance 节点 ID
    - vite-plugin-svgr v4+: export { default as X } from '*.svg?react'
      (不是 ReactComponent)

输出:
    下载 SVG 到 src/assets/icons/
    打印 React 导入代码（src/components/icons/index.tsx）
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import argparse
from pathlib import Path

# ── 配置（项目使用前请修改这两个变量）────────────────────────────────────────
FILE_KEY = "YOUR_FIGMA_FILE_KEY"  # 从 Figma URL 获取

# 图标节点映射：Figma Instance Node ID → 输出文件名（无扩展名）
# 注意：必须是 instance 节点 ID，不是 Component 定义节点 ID
ICON_NODES: dict[str, str] = {
    # "5000:76419": "icon-fill-color",  # 示例：填充色图标
    # "5000:76314": "icon-border-color",  # 示例：边框颜色图标
}

SCRIPT_DIR = Path(__file__).parent
OUT_DIR = SCRIPT_DIR.parent / "src" / "assets" / "icons"


def figma_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def download_file(url: str, dest: Path) -> int:
    """下载文件，返回文件大小（bytes）"""
    req = urllib.request.Request(url, headers={"User-Agent": "figma-icon-dl/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return len(data)


def to_react_component_name(file_name: str) -> str:
    """icon-font-size → FontSizeIcon"""
    parts = file_name.replace("icon-", "").split("-")
    return "".join(p.capitalize() for p in parts) + "Icon"


def main():
    parser = argparse.ArgumentParser(
        description="Figma REST API 图标批量下载脚本（方案 B · 兜底）"
    )
    parser.add_argument("--token", default=os.environ.get("FIGMA_TOKEN", ""))
    args = parser.parse_args()

    token = args.token.strip()
    if not token:
        print("❌ 缺少 Figma Token，请设置环境变量 FIGMA_TOKEN 或传入 --token 参数")
        sys.exit(1)

    if FILE_KEY == "YOUR_FIGMA_FILE_KEY":
        print("❌ 请先修改脚本中的 FILE_KEY 变量（从 Figma URL 获取）")
        sys.exit(1)

    if not ICON_NODES:
        print("❌ ICON_NODES 为空，请先填入节点 ID 和文件名映射")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: 批量获取 SVG 下载 URL
    ids = ",".join(ICON_NODES.keys())
    api_url = (
        f"https://api.figma.com/v1/images/{FILE_KEY}"
        f"?ids={urllib.parse.quote(ids)}&format=svg"
        f"&svg_include_id=true&svg_simplify_stroke=true"
    )
    print(f"📡 请求 Figma Images API ({len(ICON_NODES)} 个节点)...")

    try:
        resp = figma_get(api_url, token)
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        sys.exit(1)

    if resp.get("err"):
        print(f"❌ Figma API 错误: {resp['err']}")
        sys.exit(1)

    images: dict = resp.get("images", {})
    print(f"✅ API 响应成功，共 {len(images)} 个下载链接\n")

    # Step 2: 下载每个 SVG
    success = []
    failed = []

    for node_id, file_name in ICON_NODES.items():
        # Figma API 直接使用原始 node id（含冒号）作为 key，不是连字符格式
        svg_url = images.get(node_id)

        if not svg_url:
            print(f"  ⚠️  {file_name} ({node_id}) — 未找到下载链接（可能是 Component 定义节点，需改用 instance 节点 ID）")
            failed.append(file_name)
            continue

        out_file = OUT_DIR / f"{file_name}.svg"
        try:
            size = download_file(svg_url, out_file)
            print(f"  ✅ {file_name}.svg  ({size:,} bytes)")
            success.append(file_name)
        except Exception as e:
            print(f"  ❌ {file_name} — 下载失败: {e}")
            failed.append(file_name)

    # Step 3: 结果汇总
    print(f"\n{'─' * 50}")
    print(f"完成: ✅ {len(success)} 个成功，❌ {len(failed)} 个失败")
    print(f"输出目录: {OUT_DIR}")

    # Step 4: 生成 React 导入代码（vite-plugin-svgr v4+ 写法）
    if success:
        print("\n🔧 请在 src/components/icons/index.tsx 中添加以下导入：\n")
        for file_name in success:
            comp = to_react_component_name(file_name)
            print(f"export {{ default as {comp} }} from '../../assets/icons/{file_name}.svg?react';")
        print()
        print("注意: 需要安装 vite-plugin-svgr v4+：npm install -D vite-plugin-svgr")
        print("      vite.config.ts: import svgr from 'vite-plugin-svgr'，plugins: [svgr(), react()]")
        print("      src/vite-env.d.ts: /// <reference types=\"vite-plugin-svgr/client\" />")


if __name__ == "__main__":
    main()
