#!/bin/bash

echo "🚀 开始推送到GitHub..."

# 添加所有更改
git add .

# 提交更改
git commit -m "Update website with latest changes"

# 推送到master分支
echo "📤 推送到master分支..."
git push origin master

# 推送到gh-pages分支
echo "📤 推送到gh-pages分支..."
git push origin gh-pages

echo "✅ 推送完成！"
echo "🌐 您的网站应该会在几分钟内更新：https://atinyhouse.github.io"
