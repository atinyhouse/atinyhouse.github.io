#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻动态自动同步 - 最终版本
使用 RSSHub 公共服务，完全自动化

特点：
- 不需要 Token
- 不需要登录
- 完全自动化
- 可靠稳定
"""

import urllib.request
import json
import yaml
from datetime import datetime
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse
import hashlib

class HTMLStripper(HTMLParser):
    """移除 HTML 标签"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_text(self):
        return ''.join(self.text)

def strip_html(html):
    """清理 HTML 标签"""
    s = HTMLStripper()
    s.feed(html)
    return s.get_text()

def extract_images_from_description(description_text):
    """从 description 中提取图片 URL"""
    if not description_text:
        return []

    # 查找所有 img 标签中的 src
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    images = re.findall(img_pattern, description_text)

    # 过滤掉非图片链接
    valid_images = []
    for img in images:
        # 确保是有效的图片 URL
        if img and (img.startswith('http') or img.startswith('//')):
            # 如果是协议相对 URL，补全协议
            if img.startswith('//'):
                img = 'https:' + img
            valid_images.append(img)

    return valid_images

def download_image(url, save_path):
    """下载图片，返回是否成功"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://m.okjike.com/'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()

            # 检查是否是有效的图片数据（不是 JSON 错误）
            if len(data) < 100:
                # 可能是错误响应
                try:
                    json_data = json.loads(data)
                    if 'error' in json_data:
                        print(f"    ✗ 图片获取失败: {json_data.get('error')}")
                        return False
                except:
                    pass

            # 保存图片
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(data)

            return True

    except Exception as e:
        print(f"    ✗ 下载失败: {e}")
        return False

USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"

# 多个 RSSHub 镜像源（按优先级排序）
RSSHUB_INSTANCES = [
    "https://rsshub.app",
    "https://rss.miantiao.me",
    "https://rss.shab.fun",
    "https://rsshub.rssforever.com",
]

print("="*60)
print("🚀 即刻动态自动同步")
print("="*60)
print()
print(f"用户 ID: {USER_ID}")
print(f"可用镜像: {len(RSSHUB_INSTANCES)} 个")
print()

# 尝试从多个源获取 RSS
print("📡 正在获取 RSS feed...")
rss_data = None
successful_source = None

for instance in RSSHUB_INSTANCES:
    rsshub_url = f"{instance}/jike/user/{USER_ID}"
    print(f"  尝试: {instance}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(rsshub_url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            rss_data = response.read().decode('utf-8')
            successful_source = instance
            print(f"  ✓ 成功获取数据")
            break

    except Exception as e:
        print(f"  ✗ 失败: {e}")
        continue

if rss_data is None:
    print()
    print("❌ 所有 RSS 源都不可用")
    print()
    print("这通常是暂时性问题，可能的原因：")
    print("  - RSSHub 服务器维护")
    print("  - 网络连接问题")
    print("  - 即刻 API 暂时不可用")
    print()
    print("💡 建议：")
    print("  - 稍后会自动重试（每天 19:15）")
    print("  - 您的历史数据已保存，不会丢失")
    print("  - 可以稍后手动触发 workflow")
    print()
    # 在 GitHub Actions 中优雅退出，避免显示为失败
    import sys
    if os.getenv('GITHUB_ACTIONS'):
        print("⚠️  GitHub Actions: 优雅退出，等待下次重试")
        sys.exit(0)
    else:
        sys.exit(1)

print(f"✓ 使用数据源: {successful_source}")
print()

# 解析 RSS
print("🔄 解析 RSS 数据...")
try:
    root = ET.fromstring(rss_data)

    # 找到所有 item
    items = root.findall('.//item')

    if not items:
        print("⚠️  RSS 中没有找到动态")
        exit(0)

    print(f"✓ 找到 {len(items)} 条动态")

except Exception as e:
    print(f"❌ RSS 解析失败: {e}")
    exit(1)

print()

# 转换为 thoughts 格式
print("📝 转换数据格式...")
new_thoughts = []
total_images = 0

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(__file__))
images_dir = os.path.join(project_root, 'assets', 'thoughts')

for item in items:
    thought = {}

    # 日期时间
    pub_date = item.find('pubDate')
    if pub_date is not None and pub_date.text:
        try:
            # 解析 RSS 日期格式: Mon, 25 Oct 2025 10:30:00 +0800
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(pub_date.text)
            thought['date'] = dt.strftime('%Y-%m-%d')
            thought['time'] = dt.strftime('%H:%M')
            # 生成唯一 ID 用于图片文件名
            thought_id = dt.strftime('%Y%m%d%H%M%S')
        except:
            pass

    # 内容和图片
    description = item.find('description')
    if description is not None and description.text:
        description_text = description.text

        # 提取图片
        image_urls = extract_images_from_description(description_text)
        if image_urls:
            print(f"  [{thought.get('date')} {thought.get('time')}] 找到 {len(image_urls)} 张图片")
            images = []

            for idx, img_url in enumerate(image_urls, 1):
                # 生成文件名
                img_ext = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
                img_filename = f"{thought_id}-img{idx}{img_ext}"
                img_path = os.path.join(images_dir, img_filename)

                # 下载图片（如果不存在）
                if not os.path.exists(img_path):
                    print(f"    下载图片 {idx}/{len(image_urls)}...")
                    if download_image(img_url, img_path):
                        images.append(f"/assets/thoughts/{img_filename}")
                        total_images += 1
                        print(f"    ✓ 已保存: {img_filename}")
                else:
                    images.append(f"/assets/thoughts/{img_filename}")
                    print(f"    ✓ 已存在: {img_filename}")

            if images:
                thought['images'] = images

        # 提取文本内容
        content = strip_html(description_text)
        content = re.sub(r'\s+', ' ', content).strip()
        if content:
            thought['content'] = content

    # 标题
    title = item.find('title')
    if title is not None and title.text:
        title_text = title.text.strip()
        # 如果标题不是内容的开头部分，则作为话题
        content = thought.get('content', '')
        if title_text and content and not content.startswith(title_text[:20]):
            thought['topic'] = title_text

    # 链接
    link = item.find('link')
    if link is not None and link.text:
        thought['source_link'] = link.text

    if 'date' in thought and 'content' in thought:
        new_thoughts.append(thought)

print(f"✓ 成功转换 {len(new_thoughts)} 条动态")
if total_images > 0:
    print(f"✓ 下载了 {total_images} 张新图片")
print()

# 读取现有数据
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_data')
output_file = os.path.join(data_dir, 'thoughts.yml')

print(f"📂 读取现有数据...")

existing_thoughts = []
if os.path.exists(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = []
            for line in f:
                if not line.strip().startswith('#'):
                    lines.append(line)

            if lines:
                existing_thoughts = yaml.safe_load(''.join(lines)) or []

        print(f"✓ 读取到 {len(existing_thoughts)} 条现有动态")
    except Exception as e:
        print(f"⚠️  读取失败，将创建新文件: {e}")
else:
    print("✓ 文件不存在，将创建新文件")

print()

# 合并去重
print("🔗 合并数据...")

# 使用 source_link 作为主要唯一标识（最可靠）
# 如果没有 source_link，则用内容作为标识
existing_keys = {}  # key -> thought
for t in existing_thoughts:
    source_link = t.get('source_link', '')
    if source_link:
        key = f"link:{source_link}"
    else:
        # 对于没有 source_link 的，用日期+时间+内容前100字符
        content = ''.join(str(t.get('content', '')).split())[:100]
        key = f"content:{t.get('date', '')}_{t.get('time', '')}_{content}"
    existing_keys[key] = t

new_count = 0
for t in new_thoughts:
    # 确保时间是字符串格式（防止 YAML 解析问题）
    if 'time' in t:
        t['time'] = str(t['time'])

    source_link = t.get('source_link', '')
    if source_link:
        key = f"link:{source_link}"
    else:
        content = ''.join(str(t.get('content', '')).split())[:100]
        key = f"content:{t.get('date', '')}_{t.get('time', '')}_{content}"

    if key not in existing_keys:
        existing_thoughts.append(t)
        existing_keys[key] = t
        new_count += 1

# 按日期时间倒序排列
existing_thoughts.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

print(f"✓ 合并完成")
print(f"  总计: {len(existing_thoughts)} 条")
print(f"  新增: {new_count} 条")
print()

# 保存
print("💾 保存数据...")

os.makedirs(data_dir, exist_ok=True)

# 确保所有时间字段都是字符串类型
for thought in existing_thoughts:
    if 'time' in thought and thought['time'] is not None:
        thought['time'] = str(thought['time'])

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 sync_jike_simple.py 自动生成
# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 数据来源: RSSHub (https://rsshub.app)
#
# ============================================

"""

# 自定义 YAML representer，确保时间字段用引号
def str_representer(dumper, data):
    """确保时间格式的字符串用引号包裹"""
    if ':' in str(data) and len(str(data)) <= 8:  # 可能是时间格式
        return dumper.represent_scalar('tag:yaml.org,2002:str', str(data), style="'")
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_representer)

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)
        yaml.dump(
            existing_thoughts,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=float('inf')
        )

    print(f"✓ 数据已保存到: {output_file}")

except Exception as e:
    print(f"❌ 保存失败: {e}")
    exit(1)

print()
print("="*60)
print("✅ 同步完成！")
print("="*60)
print()
print(f"📊 统计信息:")
print(f"  - RSS 获取: {len(items)} 条")
print(f"  - 有效数据: {len(new_thoughts)} 条")
print(f"  - 新增动态: {new_count} 条")
print(f"  - 下载图片: {total_images} 张")
print(f"  - 总计动态: {len(existing_thoughts)} 条")
print()

if new_count > 0:
    print(f"🎉 发现 {new_count} 条新动态！")
    print()
    print("最新动态预览:")
    for i, t in enumerate(new_thoughts[:3], 1):
        content_preview = t.get('content', '')[:60]
        print(f"  {i}. [{t.get('date')} {t.get('time')}] {content_preview}...")
else:
    print("✓ 没有新动态")

print()
print("💡 下一步:")
print("  - 本地预览: bundle exec jekyll serve")
print("  - 访问: http://localhost:4000/thoughts/")
