#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用去重脚本 - 清理所有重复的 thoughts
"""

import yaml
import os
from datetime import datetime

# 文件路径
data_file = '_data/thoughts.yml'

print("="*60)
print("🧹 清理所有重复的 Thoughts")
print("="*60)
print()

# 读取文件
print("📂 读取文件...")
with open(data_file, 'r', encoding='utf-8') as f:
    lines = [line for line in f if not line.strip().startswith('#')]
    thoughts = yaml.safe_load(''.join(lines)) or []

print(f"✓ 读取到 {len(thoughts)} 条记录")
print()

# 去重
print("🔍 查找并删除重复...")
seen = {}
unique = []
duplicates_removed = 0

for t in thoughts:
    date = t.get('date', '')
    time = str(t.get('time', '')).strip()

    # 使用日期+时间作为唯一键
    key = f"{date}_{time}"

    if key in seen:
        # 重复了，比较哪个更好
        old = seen[key]

        # 计算分数 - 保留最完整的版本
        old_score = 0
        new_score = 0

        # 有图片加分
        old_images = len(old.get('images', []))
        new_images = len(t.get('images', []))
        old_score += old_images * 2
        new_score += new_images * 2

        # 有分段加分（检查换行符）
        old_content = str(old.get('content', ''))
        new_content = str(t.get('content', ''))

        # YAML的 | 格式会保留换行，这是我们想要的
        if '\n\n' in old_content:
            old_score += 10
        if '\n\n' in new_content:
            new_score += 10

        # 内容长度
        old_score += len(old_content) // 100
        new_score += len(new_content) // 100

        if new_score > old_score:
            # 新的更好，替换旧的
            idx = unique.index(old)
            unique[idx] = t
            seen[key] = t
            print(f"  替换: {date} {time} (旧:{old_score} 新:{new_score})")
        else:
            # 旧的更好或相等，跳过新的
            print(f"  跳过: {date} {time} (保留旧的 {old_score} >= {new_score})")

        duplicates_removed += 1
    else:
        # 第一次见到，添加
        seen[key] = t
        unique.append(t)

print()
print(f"✓ 去重完成")
print(f"  原始记录: {len(thoughts)}")
print(f"  删除重复: {duplicates_removed}")
print(f"  最终记录: {len(unique)}")
print()

# 排序
print("📊 排序...")
unique.sort(
    key=lambda x: (x.get('date', '0000-00-00'), str(x.get('time', '00:00'))),
    reverse=True
)
print("✓ 已按日期时间倒序排列")
print()

# 保存
print("💾 保存文件...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已清理所有重复条目
# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open(data_file, 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        unique,
        f,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=float('inf')
    )

print(f"✓ 已保存到: {data_file}")
print()
print("="*60)
print("✅ 清理完成！")
print("="*60)
