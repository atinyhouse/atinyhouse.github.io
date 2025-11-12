#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 thoughts.yml 中不存在的图片引用
"""

import os
import yaml
from pathlib import Path

def main():
    print("="*60)
    print("🧹 清理不存在的图片引用")
    print("="*60)
    print()

    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent

    # 数据文件
    data_file = project_dir / "_data" / "thoughts.yml"
    images_dir = project_dir / "assets" / "thoughts"

    # 读取 thoughts 数据
    print("📖 读取 thoughts 数据...")
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if not line.strip().startswith('#')]
        thoughts = yaml.safe_load(''.join(lines)) or []

    print(f"✓ 读取了 {len(thoughts)} 条 thoughts")
    print()

    # 检查并清理不存在的图片
    print("🔍 检查图片文件...")
    removed_count = 0
    affected_thoughts = 0

    for thought in thoughts:
        if 'images' not in thought:
            continue

        original_count = len(thought['images'])
        valid_images = []

        for img_path in thought['images']:
            # 移除开头的 /
            img_path_clean = img_path.lstrip('/')
            full_path = project_dir / img_path_clean

            if full_path.exists():
                valid_images.append(img_path)
            else:
                removed_count += 1
                print(f"  ✗ 移除不存在的图片: {img_path}")

        # 更新图片列表
        if len(valid_images) != original_count:
            affected_thoughts += 1
            if valid_images:
                thought['images'] = valid_images
            else:
                # 如果没有有效图片了，删除 images 字段
                del thought['images']
                print(f"    删除了 thought 的 images 字段: {thought.get('date')} {thought.get('time')}")

    print()
    print(f"✓ 检查完成")
    print(f"  移除了 {removed_count} 个不存在的图片引用")
    print(f"  影响了 {affected_thoughts} 条 thoughts")
    print()

    if removed_count > 0:
        # 保存更新后的数据
        print("💾 保存更新...")

        header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 sync_jike_simple.py 自动生成
# 更新时间: 已清理不存在的图片引用
# 数据来源: RSSHub (https://rsshub.app)
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

        print("✓ 数据已保存")
    else:
        print("✓ 没有需要清理的图片引用")

    print()
    print("="*60)
    print("✅ 清理完成！")
    print("="*60)

if __name__ == "__main__":
    main()
