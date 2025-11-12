#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将HEIC图片转换为JPG格式
"""

import subprocess
from pathlib import Path
import yaml

def convert_heic_to_jpg(heic_file):
    """使用sips命令将HEIC转换为JPG"""
    jpg_file = heic_file.with_suffix('.jpg')

    if jpg_file.exists():
        print(f"跳过（已存在）: {jpg_file.name}")
        return jpg_file

    try:
        # 使用macOS的sips命令转换
        subprocess.run([
            'sips', '-s', 'format', 'jpeg',
            str(heic_file),
            '--out', str(jpg_file)
        ], check=True, capture_output=True)
        print(f"转换成功: {heic_file.name} -> {jpg_file.name}")
        return jpg_file
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {heic_file.name}, 错误: {e}")
        return None

def main():
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent

    # 图片目录
    image_dir = project_dir / "assets" / "thoughts"

    # 查找所有HEIC文件
    heic_files = list(image_dir.glob("*.heic"))
    print(f"找到 {len(heic_files)} 个HEIC文件")

    if not heic_files:
        print("没有需要转换的HEIC文件")
        return

    # 转换所有HEIC文件
    converted = []
    for heic_file in heic_files:
        jpg_file = convert_heic_to_jpg(heic_file)
        if jpg_file:
            converted.append((heic_file, jpg_file))

    print(f"\n成功转换 {len(converted)} 个文件")

    # 更新thoughts.yml中的路径
    thoughts_file = project_dir / "_data" / "thoughts.yml"

    with open(thoughts_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换.heic为.jpg
    updated_content = content.replace('.heic', '.jpg')

    with open(thoughts_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"\n已更新 {thoughts_file}")
    print("所有HEIC图片已转换为JPG格式！")

if __name__ == "__main__":
    main()
