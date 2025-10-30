#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面清理重复问题：
1. 删除9月29日（与9月28日重复）
2. 删除单个动态内重复的图片（按文件大小去重）
3. 删除重复的图片文件
"""

import yaml
import os
from datetime import datetime
from collections import defaultdict

print("="*60)
print("🧹 全面清理重复问题")
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

# 1. 删除9月29日（与9月28日重复）
print("🗑️  删除重复动态...")
thoughts_fixed = []
removed_posts = []

for t in thoughts:
    # 删除9月29日（与9月28日图片完全相同）
    if t.get('date') == '2025-09-29' and t.get('time') == '02:40':
        print(f"  ✗ 删除: {t.get('date')} {t.get('time')} (与9月28日图片重复)")
        removed_posts.append(t)
        continue

    thoughts_fixed.append(t)

print(f"✓ 删除了 {len(removed_posts)} 条重复动态")
print()

# 2. 清理每个动态内重复的图片（按文件大小去重）
print("📷 清理单个动态内的重复图片...")
cleaned_image_count = 0
images_to_delete = []

for t in thoughts_fixed:
    if 'images' not in t:
        continue

    images = t.get('images', [])
    if len(images) <= 1:
        continue

    # 按文件大小分组
    size_groups = defaultdict(list)
    for img in images:
        img_path = img.lstrip('/')
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            size_groups[size].append(img)
        else:
            # 文件不存在，直接移除
            images_to_delete.append(img)

    # 检查是否有重复
    unique_images = []
    seen_sizes = set()

    for img in images:
        img_path = img.lstrip('/')
        if not os.path.exists(img_path):
            continue

        size = os.path.getsize(img_path)

        if size not in seen_sizes:
            # 第一次见到这个大小，保留
            unique_images.append(img)
            seen_sizes.add(size)
        else:
            # 重复的图片，标记删除
            print(f"  ✗ {t.get('date')} {t.get('time')}: 移除重复图片 {os.path.basename(img_path)}")
            images_to_delete.append(img)
            cleaned_image_count += 1

    # 更新图片列表
    if len(unique_images) != len(images):
        t['images'] = unique_images
        print(f"    {t.get('date')} {t.get('time')}: {len(images)} 张 -> {len(unique_images)} 张")

print(f"✓ 清理了 {cleaned_image_count} 张重复图片")
print()

# 3. 删除物理文件
print("🗑️  删除重复的图片文件...")
deleted_files = 0

for img in images_to_delete:
    img_path = img.lstrip('/')
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f"  ✗ 删除文件: {os.path.basename(img_path)}")
        deleted_files += 1

print(f"✓ 删除了 {deleted_files} 个文件")
print()

# 4. 保存
print("💾 保存清理后的数据...")

thoughts_fixed.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已全面清理：删除重复动态、去除重复图片
# 清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open('_data/thoughts.yml', 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        thoughts_fixed,
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
print(f"  - 原始动态: {len(thoughts)} 条")
print(f"  - 删除动态: {len(removed_posts)} 条")
print(f"  - 清理图片: {cleaned_image_count} 张")
print(f"  - 删除文件: {deleted_files} 个")
print(f"  - 最终动态: {len(thoughts_fixed)} 条")
print()
