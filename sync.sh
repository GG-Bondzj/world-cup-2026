#!/bin/bash
# 世界杯网站同步脚本：将 world_cup/ 的更新同步到根目录并推送到 GitHub Pages

set -e
cd "$(dirname "$0")"

echo "🔍 检查文件差异..."
CHANGED=0
for f in world_cup/*.html; do
    base=$(basename "$f")
    if ! diff -q "world_cup/$base" "$base" >/dev/null 2>&1; then
        echo "  📝 更新: $base"
        cp "world_cup/$base" "$base"
        CHANGED=1
    fi
done

if [ "$CHANGED" -eq 0 ]; then
    echo "✅ 所有文件已是最新，无需同步"
    exit 0
fi

echo ""
echo "📦 提交更新..."
git add *.html world_cup/*.html
git commit -m "自动同步世界杯赛程更新 $(date '+%Y-%m-%d %H:%M')"

echo ""
echo "🚀 推送到 GitHub..."
git push origin master

echo ""
echo "✅ 同步完成！固定地址: https://gg-bondzj.github.io/world-cup-2026/"
