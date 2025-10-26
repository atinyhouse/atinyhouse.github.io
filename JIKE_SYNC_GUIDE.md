# 即刻动态自动同步 - 快速开始指南

## ✨ 系统已准备就绪！

您的博客已经配置了自动同步即刻动态的功能。

## 🎯 立即开始

### 步骤 1: 获取即刻 Token

1. 访问 https://web.okjike.com 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` 标签
4. 刷新页面
5. 找到包含 `graphql` 的请求
6. 查看 Request Headers 中的 `x-jike-access-token`

### 步骤 2: 本地测试（可选）

```bash
# 安装依赖
cd scripts
pip install -r requirements.txt

# 设置环境变量
export JIKE_ACCESS_TOKEN="你的token"

# 运行同步
python sync_jike_v2.py

# 预览博客
cd ..
bundle exec jekyll serve
```

访问 http://localhost:4000/thoughts/ 查看效果

### 步骤 3: 配置 GitHub Actions（自动化）

1. 进入 GitHub 仓库：https://github.com/atinyhouse/atinyhouse.github.io
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加：
   - Name: `JIKE_ACCESS_TOKEN`
   - Value: 你的 token

### 步骤 4: 启用自动同步

1. 确保新文件已提交到 GitHub
2. GitHub Actions 会自动每天运行 3 次（9:00, 15:00, 21:00）
3. 也可以手动触发：
   - 进入 `Actions` 标签
   - 选择 `Sync Jike Thoughts`
   - 点击 `Run workflow`

## 📁 新增文件列表

```
✅ scripts/sync_jike_v2.py          # 同步脚本
✅ scripts/requirements.txt         # Python 依赖
✅ scripts/.env.example             # 环境变量示例
✅ scripts/README.md                # 详细文档
✅ .github/workflows/sync-jike.yml  # GitHub Actions 配置
```

## 🔗 相关链接

- 即刻个人主页: https://web.okjike.com/u/71A6B3C3-1382-4121-A17A-2A4C05CB55E8
- Thoughts 页面: https://atinyhouse.github.io/thoughts/
- 详细文档: scripts/README.md

## ⚡ 快速命令

```bash
# 本地同步
cd scripts && python sync_jike_v2.py

# 查看 Actions 日志
gh run list --workflow="sync-jike.yml"

# 手动触发同步
gh workflow run sync-jike.yml
```

## ❓ 需要帮助？

查看 `scripts/README.md` 了解：
- 详细使用说明
- 常见问题解答
- 故障排查指南

---

生成时间: 2025-10-25
