#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级去重脚本 - 只使用 source_link 去重，更快更可靠
"""

import yaml
import os
from datetime import datetime

data_file = '_data/thoughts.yml'

print("="*60)
print("🧹 轻量级去重 - 基于 source_link")
print("="*60)
print()

# 读取文件
print("📂 读取文件...")
with open(data_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取注释header
header_lines = []
data_lines = []
for line in content.split('\n'):
    if line.strip().startswith('#') or (not data_lines and not line.strip()):
        header_lines.append(line)
    else:
        data_lines.append(line)

# 解析YAML数据
thoughts = yaml.safe_load('\n'.join(data_lines)) or []
print(f"✓ 读取到 {len(thoughts)} 条记录")
print()

# 去重 - 只基于 source_link
print("🔍 去重...")
seen_links = {}
unique = []
duplicates = 0

for i, t in enumerate(thoughts):
    link = t.get('source_link', '')

    # 确保时间是字符串
    if 'time' in t and t['time'] is not None:
        t['time'] = str(t['time'])

    if link:
        if link in seen_links:
            # 重复了
            old_idx = seen_links[link]
            old = unique[old_idx]

            # 简单比较：保留有更多字段的
            old_score = len([k for k, v in old.items() if v])
            new_score = len([k for k, v in t.items() if v])

            if new_score > old_score:
                unique[old_idx] = t
                print(f"  替换: {link[:70]}")
            else:
                print(f"  跳过: {link[:70]}")

            duplicates += 1
        else:
            seen_links[link] = len(unique)
            unique.append(t)
    else:
        # 没有 source_link 的也保留
        unique.append(t)

print()
print(f"✓ 去重完成")
print(f"  原始: {len(thoughts)} 条")
print(f"  删除: {duplicates} 条")
print(f"  保留: {len(unique)} 条")
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
print("💾 保存...")

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已清理所有重复条目
# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

# 自定义 YAML representer
def str_representer(dumper, data):
    if ':' in str(data) and len(str(data)) <= 8:
        return dumper.represent_scalar('tag:yaml.org,2002:str', str(data), style="'")
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_representer)

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
print("✅ 完成！")
print("="*60)
