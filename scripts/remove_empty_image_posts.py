#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除图片为空的重复动态
这些是由于合并时图片全部重复导致的空图片列表动态
"""

import yaml
from datetime import datetime

print("="*60)
print("🗑️  删除空图片的重复动态")
print("="*60)
print()

# 读取数据
with open('_data/thoughts.yml', 'r', encoding='utf-8') as f:
    lines = []
    for line in f:
        if not line.strip().startswith('#'):
            lines.append(line)
    thoughts = yaml.safe_load(''.join(lines)) or []

print(f"当前数据: {len(thoughts)} 条")
print()

# 删除符合以下条件的动态：
# 1. images 字段存在但为空列表
# 2. 同一date有另一条相同content但有图片的动态
print("🔍 查找空图片的重复动态...")

# 按日期分组
from collections import defaultdict
by_date = defaultdict(list)
for t in thoughts:
    date = t.get('date', '')
    by_date[date].append(t)

to_remove = []
for date, posts in by_date.items():
    if len(posts) == 1:
        continue

    # 检查是否有内容相同但一个有图片一个没图片的
    for i, p1 in enumerate(posts):
        for j, p2 in enumerate(posts):
            if i >= j:
                continue

            # 内容相同
            if p1.get('content') == p2.get('content'):
                p1_has_images = 'images' in p1 and len(p1['images']) > 0
                p2_has_images = 'images' in p2 and len(p2['images']) > 0

                # 一个有图片一个没图片，删除没图片的
                if p1_has_images and not p2_has_images:
                    print(f"  ✗ 删除: {date} {p2.get('time')} (无图片，保留 {p1.get('time')} 有图片的版本)")
                    to_remove.append((date, p2.get('time')))
                elif p2_has_images and not p1_has_images:
                    print(f"  ✗ 删除: {date} {p1.get('time')} (无图片，保留 {p2.get('time')} 有图片的版本)")
                    to_remove.append((date, p1.get('time')))

# 删除
thoughts_cleaned = []
for t in thoughts:
    key = (t.get('date'), t.get('time'))
    if key not in to_remove:
        thoughts_cleaned.append(t)

print(f"✓ 删除了 {len(to_remove)} 条空图片动态")
print()

# 排序
thoughts_cleaned.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

# 保存
print("💾 保存清理后的数据...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已删除空图片的重复动态
# 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open('_data/thoughts.yml', 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        thoughts_cleaned,
        f,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=float('inf')
    )

print("✓ 保存完成")
print()

print("="*60)
print("✅ 清理完成！")
print("="*60)
print()
print(f"📊 统计:")
print(f"  - 原始数据: {len(thoughts)} 条")
print(f"  - 删除动态: {len(to_remove)} 条")
print(f"  - 最终数据: {len(thoughts_cleaned)} 条")
print()
