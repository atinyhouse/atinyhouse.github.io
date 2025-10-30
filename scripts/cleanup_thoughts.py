#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 thoughts.yml 数据：
1. 去除重复的动态
2. 清理不存在的图片路径
3. 统一文字格式（压缩多余空行）
"""

import yaml
import os
import re
from datetime import datetime

print("="*60)
print("🧹 清理 Thoughts 数据")
print("="*60)
print()

# 读取 thoughts.yml
data_file = '_data/thoughts.yml'
print(f"📂 读取数据文件: {data_file}")

with open(data_file, 'r', encoding='utf-8') as f:
    lines = []
    for line in f:
        if not line.strip().startswith('#'):
            lines.append(line)

    if lines:
        thoughts = yaml.safe_load(''.join(lines)) or []

print(f"✓ 读取到 {len(thoughts)} 条动态")
print()

# 1. 去重（使用日期+压缩后的内容前100字符）
print("🔄 去除重复动态...")
unique_thoughts = {}

for thought in thoughts:
    # 先压缩内容的空白，用于比较
    content_normalized = re.sub(r'\s+', ' ', thought.get('content', '')).strip()
    # 使用日期+压缩后内容前100字符作为key
    key = f"{thought.get('date', '')}_{content_normalized[:100]}"

    if key not in unique_thoughts:
        unique_thoughts[key] = thought
    else:
        # 如果新的有图片而旧的没有，或者新的图片更多，则合并
        old = unique_thoughts[key]

        # 合并图片
        if 'images' in thought:
            if 'images' not in old:
                old['images'] = thought['images']
            else:
                # 合并图片列表
                old['images'].extend(thought['images'])

        # 保留内容更好（更短、格式更好）的版本
        if len(thought.get('content', '')) < len(old.get('content', '')):
            old['content'] = thought['content']

        # 保留有 source_link 的版本
        if 'source_link' in thought and 'source_link' not in old:
            old['source_link'] = thought['source_link']

        # 保留有 topic 的版本
        if 'topic' in thought and 'topic' not in old:
            old['topic'] = thought['topic']

thoughts = list(unique_thoughts.values())
print(f"✓ 去重后剩余 {len(thoughts)} 条")
print()

# 2. 清理图片路径（只保留存在的文件）
print("🖼️  清理图片路径...")
images_dir = '_pages/files/thoughts'
cleaned_images_count = 0

for thought in thoughts:
    if 'images' in thought:
        valid_images = []
        for img_path in thought['images']:
            # 转换为文件系统路径
            file_path = img_path.lstrip('/')

            if os.path.exists(file_path):
                valid_images.append(img_path)
            else:
                cleaned_images_count += 1
                print(f"  ✗ 移除不存在的图片: {os.path.basename(img_path)}")

        # 去重
        valid_images = list(dict.fromkeys(valid_images))

        if valid_images:
            thought['images'] = valid_images
        else:
            del thought['images']

print(f"✓ 清理了 {cleaned_images_count} 个无效图片路径")
print()

# 3. 统一文字格式
print("📝 统一文字格式...")
fixed_content_count = 0

for thought in thoughts:
    if 'content' in thought:
        content = thought['content']
        original_len = len(content)

        # 清理多余的空白
        content = re.sub(r'\n\s*\n+', '\n\n', content)  # 多个空行压缩成双换行
        content = re.sub(r'[ \t]+', ' ', content)  # 多个空格压缩成单个空格
        content = content.strip()

        if len(content) != original_len:
            thought['content'] = content
            fixed_content_count += 1

print(f"✓ 修复了 {fixed_content_count} 条动态的格式")
print()

# 4. 按时间倒序排列
thoughts.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

# 5. 保存
print("💾 保存清理后的数据...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件已清理：去重、清理无效图片、统一格式
# 清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open(data_file, 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        thoughts,
        f,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=float('inf')
    )

print(f"✓ 数据已保存")
print()

print("="*60)
print("✅ 清理完成！")
print("="*60)
print()
print(f"📊 最终统计:")
print(f"  - 总动态数: {len(thoughts)} 条")
print(f"  - 去重: 从 {len(list(unique_thoughts.values()))} 条开始")
print(f"  - 清理图片: {cleaned_images_count} 个无效路径")
print(f"  - 修复格式: {fixed_content_count} 条")
print()
