#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 RSSHub 自动同步即刻动态
这个方法最简单可靠，不需要 Token，完全自动化！
"""

import feedparser
import yaml
from datetime import datetime
import os
import re

USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"
RSS_URL = f"https://rsshub.app/jike/user/{USER_ID}"

print("="*60)
print("🚀 通过 RSSHub 同步即刻动态")
print("="*60)
print()
print(f"RSS 地址: {RSS_URL}")
print(f"用户 ID: {USER_ID}")
print()

# 获取 RSS
print("📡 正在获取 RSS feed...")
try:
    feed = feedparser.parse(RSS_URL)

    if feed.bozo:
        print(f"⚠️  RSS 解析警告: {feed.bozo_exception}")

    if not feed.entries:
        print("❌ 没有获取到任何动态")
        print("\n可能的原因：")
        print("1. RSSHub 服务暂时不可用")
        print("2. 用户 ID 不正确")
        print("3. 网络连接问题")
        exit(1)

    print(f"✓ 成功获取 {len(feed.entries)} 条动态")

except Exception as e:
    print(f"❌ 获取失败: {e}")
    exit(1)

print()

# 解析动态
print("🔄 解析动态数据...")
new_thoughts = []

for entry in feed.entries:
    thought = {}

    # 日期时间
    if hasattr(entry, 'published_parsed'):
        dt = datetime(*entry.published_parsed[:6])
        thought['date'] = dt.strftime('%Y-%m-%d')
        thought['time'] = dt.strftime('%H:%M')
    elif hasattr(entry, 'updated_parsed'):
        dt = datetime(*entry.updated_parsed[:6])
        thought['date'] = dt.strftime('%Y-%m-%d')
        thought['time'] = dt.strftime('%H:%M')

    # 内容
    content = entry.get('summary', '') or entry.get('description', '')
    if content:
        # 清理 HTML 标签
        content = re.sub(r'<[^>]+>', '', content)
        content = content.strip()
        if content:
            thought['content'] = content

    # 标题作为话题
    title = entry.get('title', '')
    if title and title != content[:30]:
        thought['topic'] = title

    # 链接
    if hasattr(entry, 'link'):
        thought['jike_link'] = entry.link

    if 'date' in thought and 'content' in thought:
        new_thoughts.append(thought)

print(f"✓ 成功解析 {len(new_thoughts)} 条有效动态")
print()

# 读取现有数据
output_file = '../_data/thoughts.yml'
print(f"📂 读取现有数据: {output_file}")

existing_thoughts = []
if os.path.exists(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = []
            for line in f:
                if not line.strip().startswith('#'):
                    content.append(line)
            if content:
                existing_thoughts = yaml.safe_load(''.join(content)) or []
        print(f"✓ 现有 {len(existing_thoughts)} 条动态")
    except Exception as e:
        print(f"⚠️  读取失败: {e}")
        existing_thoughts = []
else:
    print("✓ 文件不存在，将创建新文件")

print()

# 合并去重
print("🔗 合并数据...")
thought_keys = set()

for t in existing_thoughts:
    key = f"{t.get('date')}_{t.get('time')}_{t.get('content', '')[:50]}"
    thought_keys.add(key)

new_count = 0
for t in new_thoughts:
    key = f"{t.get('date')}_{t.get('time')}_{t.get('content', '')[:50]}"
    if key not in thought_keys:
        existing_thoughts.append(t)
        thought_keys.add(key)
        new_count += 1

# 按时间排序
existing_thoughts.sort(
    key=lambda x: f"{x.get('date', '9999-99-99')} {x.get('time', '99:99')}",
    reverse=True
)

print(f"✓ 合并完成")
print(f"  - 总计: {len(existing_thoughts)} 条")
print(f"  - 新增: {new_count} 条")
print()

# 保存
print("💾 保存数据...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 sync_from_rss.py 自动生成
# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 数据来源: RSSHub
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
            width=1000
        )
    print("✓ 保存成功！")

except Exception as e:
    print(f"❌ 保存失败: {e}")
    exit(1)

print()
print("="*60)
print("✅ 同步完成！")
print("="*60)
print()
print(f"📊 统计:")
print(f"  - RSS 获取: {len(feed.entries)} 条")
print(f"  - 有效数据: {len(new_thoughts)} 条")
print(f"  - 新增动态: {new_count} 条")
print(f"  - 总计动态: {len(existing_thoughts)} 条")
print()

if new_count > 0:
    print("🎉 发现新动态！")
else:
    print("✓ 没有新动态，数据已是最新")

print()
print("💡 提示:")
print("  - 此脚本可通过 GitHub Actions 定时运行")
print("  - 建议每天运行 2-3 次")
print("  - RSS 通常包含最近 20-50 条动态")
