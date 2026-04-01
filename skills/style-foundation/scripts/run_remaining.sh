#!/bin/bash
# 跑完剩余 8 张图片分析，每次间隔 15 秒（RPM=20 足够）
cd "$(dirname "$0")/.."
export GEMINI_MODEL="gemini-2.5-flash-lite"
SCRIPT="scripts/analyze_cases.py"
CASES="references/cases"

FILES=(
  "a0615357f88beedc-supercommon-systems.webp|Supercommon"
  "abcc524af73f5123-obvious-ai.webp|Obviously AI"
  "c7209067f01d22dc-joinspread-app.webp|Spread"
  "dc3d60eb37168934-linear-app.webp|Linear"
  "e947ef71932c45d4-framer-link.webp|Framer"
  "f761cc5a0d6f345e-www-terminal-x-ai.jpg|Terminal X"
  "fc9451bcd8d9bfb8-www-hihobbes-com.webp|Hobbes"
  "fe12f6dec70abd57-screenshot-desktop.webp|Screenshot Desktop 2"
)

TOTAL=${#FILES[@]}
OK=0
FAIL=0

for i in "${!FILES[@]}"; do
  IFS='|' read -r FILE NAME <<< "${FILES[$i]}"
  NUM=$((i + 1))
  echo ""
  echo "========== [$NUM/$TOTAL] $NAME =========="
  python3 "$SCRIPT" --file "$CASES/$FILE" --name "$NAME"
  if [ $? -eq 0 ]; then
    OK=$((OK + 1))
  else
    FAIL=$((FAIL + 1))
  fi
  
  if [ $NUM -lt $TOTAL ]; then
    echo "⏳ 等待 15 秒..."
    sleep 15
  fi
done

echo ""
echo "========================================="
echo "全部完成: $OK 成功, $FAIL 失败"
echo "========================================="
