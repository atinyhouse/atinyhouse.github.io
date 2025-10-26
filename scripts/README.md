# 即刻动态同步脚本 V2

自动同步即刻动态到博客 Thoughts 页面的工具。

## 📋 功能特性

- ✅ 自动获取即刻最新动态（使用 GraphQL API）
- ✅ 自动下载图片到本地
- ✅ 智能去重，不会重复添加
- ✅ 支持 GitHub Actions 定时运行
- ✅ 完整的时间线展示

## 🚀 快速开始

### 方法一：本地手动同步（推荐）

1. **安装依赖**
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

2. **获取即刻 Access Token**

   打开浏览器访问 [即刻网页版](https://web.okjike.com)：

   - 登录你的账号
   - 按 F12 打开开发者工具
   - 切换到 Network 标签
   - 刷新页面或点击任意链接
   - 在请求列表中找到任意 `graphql` 请求
   - 查看 Request Headers 中的 `x-jike-access-token`
   - 复制这个 token

3. **设置环境变量**
   ```bash
   export JIKE_ACCESS_TOKEN="你的token"
   export JIKE_USER_ID="71A6B3C3-1382-4121-A17A-2A4C05CB55E8"
   ```

4. **运行同步脚本**
   ```bash
   python sync_jike_v2.py
   ```

5. **预览效果**
   ```bash
   cd ..
   bundle exec jekyll serve
   ```

   访问 http://localhost:4000/thoughts/ 查看效果

### 方法二：GitHub Actions 自动同步

1. **设置 GitHub Secrets**

   在 GitHub 仓库页面：
   - 进入 `Settings` → `Secrets and variables` → `Actions`
   - 点击 `New repository secret`
   - 添加以下 secrets：
     - `JIKE_ACCESS_TOKEN`: 你的即刻 access token
     - `JIKE_USER_ID`: 你的即刻用户 ID（默认：71A6B3C3-1382-4121-A17A-2A4C05CB55E8）

2. **启用 GitHub Actions**

   - 确保 `.github/workflows/sync-jike.yml` 文件已提交
   - GitHub Actions 会在以下时间自动运行：
     - 每天北京时间 9:00, 15:00, 21:00
   - 也可以手动触发：
     - 进入仓库的 `Actions` 标签
     - 选择 `Sync Jike Thoughts` 工作流
     - 点击 `Run workflow`

3. **查看运行结果**

   - 在 `Actions` 标签中查看运行日志
   - 同步成功后会自动提交到 gh-pages 分支

## 📁 文件说明

```
scripts/
├── sync_jike_v2.py       # 主同步脚本（✅ 推荐使用）
├── fetch_jike.py         # 旧版脚本（已过时）
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量示例
└── README.md             # 本文件

_data/
└── thoughts.yml          # 即刻动态数据（YAML 格式）

_pages/
├── thoughts.html         # Thoughts 展示页面
└── files/
    └── thoughts/         # 图片存储目录

.github/
└── workflows/
    └── sync-jike.yml     # GitHub Actions 配置
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 是否必需 | 默认值 |
|--------|------|----------|--------|
| `JIKE_ACCESS_TOKEN` | 即刻访问令牌 | ✅ 是 | - |
| `JIKE_USER_ID` | 即刻用户 ID | ❌ 否 | 71A6B3C3-1382-4121-A17A-2A4C05CB55E8 |

### 同步频率

默认配置为每天 3 次（北京时间 9:00, 15:00, 21:00）。

如需修改频率，编辑 `.github/workflows/sync-jike.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 1,7,13 * * *'  # UTC 时间，需要减 8 小时
```

## 📊 数据格式

`_data/thoughts.yml` 使用以下格式：

```yaml
- date: '2025-10-25'
  time: '14:30'
  content: |
    这是一条即刻动态的内容
    支持多行文本
  images:
    - /_pages/files/thoughts/image1.jpg
    - /_pages/files/thoughts/image2.jpg
  link: 'https://example.com'
  link_title: '链接标题'
```

## 🐛 故障排查

### Token 获取失败

**问题**: 找不到 `x-jike-access-token` header

**解决方法**:
1. 确保已登录即刻网页版
2. 刷新页面，确保有网络请求
3. 查找包含 `graphql` 的请求
4. Token 通常以 `eyJ` 开头

### 图片下载失败

**问题**: 部分图片无法显示

**解决方法**:
1. 检查 `_pages/files/thoughts/` 目录权限
2. 确保网络连接稳定
3. 图片 URL 可能已过期，重新运行同步

### GitHub Actions 运行失败

**问题**: Actions 显示红色 ❌

**解决方法**:
1. 检查 Secrets 是否正确设置
2. 查看 Actions 日志中的错误信息
3. Token 可能已过期，需要重新获取

## 💡 常见问题

**Q: Token 会过期吗？**

A: 会的。即刻的 Token 有效期约为 30 天。过期后需要重新获取并更新 GitHub Secrets。

**Q: 如何修改同步的动态数量？**

A: 编辑 `sync_jike_v2.py` 中的 `FETCH_LIMIT` 变量（默认 50 条）。

**Q: 可以同步其他用户的动态吗？**

A: 可以，但需要修改 `JIKE_USER_ID` 环境变量。注意：私密账号可能无法访问。

**Q: 图片占用空间太大怎么办？**

A: 可以考虑：
1. 使用图床服务（如七牛云、腾讯云 COS）
2. 压缩图片质量
3. 定期清理旧图片

## 📝 更新日志

### v2.0 (2025-10-25)
- ✨ 使用新的 GraphQL API
- ✨ 支持图片自动下载到本地
- ✨ 智能去重和合并
- ✨ 完整的 GitHub Actions 支持
- ✨ 更好的错误处理和日志

### v1.0 (2024-10-24)
- 初始版本
- 基础的数据获取功能

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢即刻提供的优质社交平台
- 感谢 Jekyll 静态博客框架
- 感谢 Claude Code 提供的开发支持
