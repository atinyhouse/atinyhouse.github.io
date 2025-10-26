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

USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"
RSSHUB_URL = f"https://rsshub.app/jike/user/{USER_ID}"

print("="*60)
print("🚀 即刻动态自动同步")
print("="*60)
print()
print(f"用户 ID: {USER_ID}")
print(f"RSS 源: {RSSHUB_URL}")
print()

# 获取 RSS
print("📡 正在获取 RSS feed...")
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    req = urllib.request.Request(RSSHUB_URL, headers=headers)

    with urllib.request.urlopen(req, timeout=30) as response:
        rss_data = response.read().decode('utf-8')

    print("✓ RSS 获取成功")

except Exception as e:
    print(f"❌ RSS 获取失败: {e}")
    print()
    print("备用方案：")
    print("由于您已有大量历史数据，可以暂时跳过本次同步")
    print("建议稍后重试或检查网络连接")
    exit(1)

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
        except:
            pass

    # 内容
    description = item.find('description')
    if description is not None and description.text:
        content = strip_html(description.text)
        content = re.sub(r'\s+', ' ', content).strip()
        if content:
            thought['content'] = content

    # 标题
    title = item.find('title')
    if title is not None and title.text:
        title_text = title.text.strip()
        # 如果标题不是内容的开头部分，则作为话题
        if title_text and content and not content.startswith(title_text[:20]):
            thought['topic'] = title_text

    # 链接
    link = item.find('link')
    if link is not None and link.text:
        thought['source_link'] = link.text

    if 'date' in thought and 'content' in thought:
        new_thoughts.append(thought)

print(f"✓ 成功转换 {len(new_thoughts)} 条动态")
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

# 使用日期+时间+内容前100字符作为唯一标识
existing_keys = set()
for t in existing_thoughts:
    key = f"{t.get('date', '')}_{t.get('time', '')}_{t.get('content', '')[:100]}"
    existing_keys.add(key)

new_count = 0
for t in new_thoughts:
    key = f"{t.get('date', '')}_{t.get('time', '')}_{t.get('content', '')[:100]}"
    if key not in existing_keys:
        existing_thoughts.append(t)
        existing_keys.add(key)
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
