#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复自动同步产生的重复问题
"""

import yaml
import os
from datetime import datetime
from collections import defaultdict

print("="*60)
print("🔧 修复自动同步产生的重复")
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

# 去重策略：
# 1. 使用日期+时间作为唯一标识
# 2. 如果同一日期时间有多条，保留信息最完整的那条（有link的优先，图片多的优先）
print("🗑️  去除重复动态...")

unique_thoughts = {}
duplicate_images = []

for t in thoughts:
    key = f"{t.get('date', '')}_{t.get('time', '')}"

    if key not in unique_thoughts:
        unique_thoughts[key] = t
    else:
        # 合并信息，保留最完整的版本
        old = unique_thoughts[key]

        # 优先保留有外部链接的版本
        if 'link' in t and 'link' not in old:
            print(f"  ✓ 保留有链接的版本: {t.get('date')} {t.get('time')}")
            unique_thoughts[key] = t
            # 但要合并图片
            if 'images' in old:
                if 'images' not in t:
                    t['images'] = old['images']
                else:
                    t['images'].extend(old['images'])
        elif 'link' in old and 'link' not in t:
            # 保留old，但合并图片
            if 'images' in t:
                if 'images' not in old:
                    old['images'] = t['images']
                else:
                    old['images'].extend(t['images'])
        else:
            # 都没有link或都有link，保留内容更长的（格式更好的）
            old_len = len(old.get('content', ''))
            new_len = len(t.get('content', ''))

            # 检查是否有段落（包含双换行符）
            old_has_paragraphs = '\n\n' in old.get('content', '')
            new_has_paragraphs = '\n\n' in t.get('content', '')

            if new_has_paragraphs and not old_has_paragraphs:
                print(f"  ✓ 保留有段落格式的版本: {t.get('date')} {t.get('time')}")
                unique_thoughts[key] = t
                # 合并图片
                if 'images' in old:
                    if 'images' not in t:
                        t['images'] = old['images']
                    else:
                        t['images'].extend(old['images'])
            elif old_has_paragraphs or (old_len >= new_len):
                # 保留old，合并图片
                if 'images' in t:
                    if 'images' not in old:
                        old['images'] = t['images']
                    else:
                        old['images'].extend(t['images'])
            else:
                # 用new替换old，但合并图片
                if 'images' in old:
                    if 'images' not in t:
                        t['images'] = old['images']
                    else:
                        t['images'].extend(old['images'])
                unique_thoughts[key] = t

        print(f"  ✗ 合并重复: {t.get('date')} {t.get('time')}")

thoughts = list(unique_thoughts.values())
print(f"✓ 去重后剩余 {len(thoughts)} 条")
print()

# 清理每个动态内重复的图片
print("📷 清理单个动态内的重复图片...")
cleaned_count = 0

for t in thoughts:
    if 'images' not in t or len(t['images']) <= 1:
        continue

    images = t['images']

    # 按文件大小去重
    size_groups = defaultdict(list)
    for img in images:
        img_path = img.lstrip('/')
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            size_groups[size].append(img)
        else:
            duplicate_images.append(img)

    # 保留第一个
    unique_images = []
    seen_sizes = set()

    for img in images:
        img_path = img.lstrip('/')
        if not os.path.exists(img_path):
            continue

        size = os.path.getsize(img_path)
        if size not in seen_sizes:
            unique_images.append(img)
            seen_sizes.add(size)
        else:
            print(f"  ✗ {t.get('date')} {t.get('time')}: 移除重复图片 {os.path.basename(img_path)}")
            duplicate_images.append(img)
            cleaned_count += 1

    if len(unique_images) != len(images):
        t['images'] = unique_images
        print(f"    {t.get('date')} {t.get('time')}: {len(images)} 张 -> {len(unique_images)} 张")

print(f"✓ 清理了 {cleaned_count} 张重复图片")
print()

# 删除重复的图片文件
print("🗑️  删除重复的图片文件...")
deleted_count = 0

for img in duplicate_images:
    img_path = img.lstrip('/')
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f"  ✗ 删除: {os.path.basename(img_path)}")
        deleted_count += 1

print(f"✓ 删除了 {deleted_count} 个文件")
print()

# 排序
thoughts.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

# 保存
print("💾 保存清理后的数据...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已修复自动同步产生的重复问题
# 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open('_data/thoughts.yml', 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        thoughts,
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
print(f"  - 最终动态: {len(thoughts)} 条")
print(f"  - 清理图片: {cleaned_count} 张")
print(f"  - 删除文件: {deleted_count} 个")
print()
