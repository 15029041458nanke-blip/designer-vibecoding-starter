#!/bin/bash
# sync-to-github.sh
# 将 designer-vibecoding-starter 工具包完整同步到独立 GitHub 仓库
# 使用方法：在项目根目录执行 bash skills/designer-vibecoding-starter/scripts/sync-to-github.sh

set -e

REPO_URL="https://github.com/15029041458nanke-blip/designer-vibecoding-starter.git"
WORK_DIR="/tmp/starter-sync-$$"
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"

echo "📦 同步 designer-vibecoding-starter 到 GitHub..."
echo "   本地来源: $SKILL_ROOT"
echo "   目标仓库: $REPO_URL"
echo ""

# 克隆线上仓库到临时目录
git clone "$REPO_URL" "$WORK_DIR"

# 同步 designer-vibecoding-starter 自身文件
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
  "$SKILL_ROOT/agents/"     "$WORK_DIR/agents/"
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
  "$SKILL_ROOT/references/" "$WORK_DIR/references/"
cp "$SKILL_ROOT/SKILL.md"        "$WORK_DIR/SKILL.md"
cp "$SKILL_ROOT/WORKING_SPEC.md" "$WORK_DIR/WORKING_SPEC.md"
cp "$SKILL_ROOT/CHANGE_REPORT.md" "$WORK_DIR/CHANGE_REPORT.md"

# 同步 scripts（排除本文件和 pycache）
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='sync-to-github.sh' \
  "$SKILL_ROOT/scripts/" "$WORK_DIR/scripts/"

# 同步 agent-context
mkdir -p "$WORK_DIR/agent-context"
cp "$PROJECT_ROOT/agent-context/design-role-rules.md" "$WORK_DIR/agent-context/"
cp "$PROJECT_ROOT/agent-context/current-workflow.md"  "$WORK_DIR/agent-context/"

# 同步所有依赖 skills
for skill in style-foundation design-analysis requirements-refinement \
             two-stage-review systematic-debugging writing-plans architecture-check; do
  if [ -d "$PROJECT_ROOT/skills/$skill" ]; then
    rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
      "$PROJECT_ROOT/skills/$skill/" "$WORK_DIR/skills/$skill/"
    echo "  ✓ skills/$skill"
  fi
done

# 提交并推送
cd "$WORK_DIR"
git add .
if git diff --cached --quiet; then
  echo "✅ 无变更，无需推送"
else
  MSG="sync: $(date '+%Y-%m-%d %H:%M') — 从主仓库同步最新内容"
  git commit -m "$MSG"
  git push origin main
  echo "✅ 推送成功！"
fi

# 清理临时目录
rm -rf "$WORK_DIR"
echo ""
echo "🎉 完成！线上仓库已是最新版本："
echo "   $REPO_URL"
