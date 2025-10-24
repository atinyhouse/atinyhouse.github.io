# 即刻动态自动获取工具

## 方法一：直接 API 获取（推荐尝试）

```bash
# 安装依赖
pip3 install requests pyyaml

# 运行脚本
python3 scripts/fetch_jike.py
```

如果即刻 API 需要登录，会提示失败，请使用方法二。

---

## 方法二：浏览器开发者工具（最可靠）

### 步骤详解：

#### 1. 打开即刻主页
在浏览器中访问：
```
https://web.okjike.com/u/71A6B3C3-1382-4121-A17A-2A4C05CB55E8
```

#### 2. 打开开发者工具
- **Mac**: `Cmd + Option + I` 或 `F12`
- **Windows**: `F12` 或 `Ctrl + Shift + I`

#### 3. 切换到 Network 标签
点击开发者工具顶部的 **Network**（网络）标签

#### 4. 刷新页面
按 `Cmd + R` (Mac) 或 `F5` (Windows) 刷新页面

#### 5. 找到动态数据请求
在 Network 列表中找到包含动态数据的请求，通常名称包含：
- `userPost`
- `posts`
- `loadmore`

**识别方法**：
- 点击请求，在右侧预览（Preview）中查看
- 应该能看到你的即刻动态内容

#### 6. 复制响应数据
- 右键该请求
- 选择 **Copy** → **Copy Response**（复制响应）

#### 7. 保存为 JSON 文件
创建文件 `jike_data.json`，粘贴刚才复制的内容并保存

#### 8. 运行解析脚本
```bash
# 安装依赖（如果还没装）
pip3 install pyyaml

# 解析数据
python3 scripts/parse_jike_json.py jike_data.json
```

#### 9. 查看结果
脚本会自动更新 `_data/thoughts.yml` 文件。

---

## 方法三：浏览器控制台一键获取（最简单）

即将推出...

---

## 验证效果

### 启动本地预览：
```bash
cd /Users/didi/Desktop/b/atinyhouse.github.io
bundle exec jekyll serve
```

### 访问页面：
打开浏览器访问：http://localhost:4000/thoughts/

---

## 常见问题

### Q: 提示 "pip3: command not found"
安装 Python 3：
```bash
brew install python3
```

### Q: JSON 格式错误
确保复制的是完整的响应内容，包括开头的 `{` 和结尾的 `}`

### Q: 没有找到动态数据
尝试：
1. 确保登录了即刻账号
2. 多刷新几次页面
3. 查找不同名称的网络请求

### Q: 图片无法显示
即刻的图片链接是外部链接，需要网络访问。如果需要本地保存图片：
1. 下载图片到 `_pages/files/thoughts/` 目录
2. 手动修改 `thoughts.yml` 中的图片路径

---

## 更新动态

定期运行脚本即可更新最新的即刻动态：

```bash
# 方法一（如果可用）
python3 scripts/fetch_jike.py

# 方法二
python3 scripts/parse_jike_json.py jike_data.json
```

---

## 技术支持

如果遇到问题，请检查：
1. Python 版本（需要 3.6+）
2. 依赖包是否安装成功
3. JSON 文件格式是否正确
