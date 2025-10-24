#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从即刻HTML导出文件导入动态和图片到Jekyll博客的thoughts.yml
"""

import os
import re
import shutil
import yaml
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

def parse_date(date_str):
    """解析日期字符串 2025/10/16 12:20:43"""
    try:
        dt = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
        return dt
    except Exception as e:
        print(f"日期解析失败: {date_str}, 错误: {e}")
        return datetime.now()

def copy_images(img_srcs, source_dir, target_dir, date_slug):
    """复制图片到目标目录并返回新的路径"""
    if not img_srcs:
        return []

    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)

    new_paths = []
    for img_src in img_srcs:
        # 提取文件名
        filename = img_src.split('/')[-1]

        # 源文件路径
        source_file = source_dir / filename

        if not source_file.exists():
            print(f"警告: 图片文件不存在: {source_file}")
            continue

        # 生成新文件名（带日期前缀避免冲突）
        new_filename = f"{date_slug}-{filename}"
        target_file = target_dir / new_filename

        # 复制文件
        try:
            shutil.copy2(source_file, target_file)
            # 返回相对路径
            relative_path = f"/_pages/files/thoughts/{new_filename}"
            new_paths.append(relative_path)
        except Exception as e:
            print(f"复制图片失败 {source_file} -> {target_file}: {e}")

    return new_paths

def clean_content(content_html):
    """清理HTML内容，转换为纯文本"""
    # 先将<br/><br/>或<br><br>转换为段落标记
    content = content_html.replace('<br/><br/>', '\n\n')
    content = content.replace('<br><br>', '\n\n')
    # 再将单个<br/>或<br>转换为换行
    content = content.replace('<br/>', '\n')
    content = content.replace('<br>', '\n')
    # 移除其他HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    # 清理多余的空行（连续3个以上换行变成2个）
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def parse_html_to_thoughts(html_file, source_image_dir, target_image_dir):
    """解析HTML文件，提取所有动态"""

    # 读取HTML文件
    print(f"开始读取HTML文件: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有动态
    posts = soup.find_all('div', class_='post-default')
    print(f"找到 {len(posts)} 篇动态")

    thoughts = []
    total_images = 0

    for idx, post in enumerate(posts):
        try:
            # 提取日期
            date_elem = post.find('span', class_='p-date')
            if not date_elem:
                print(f"跳过第 {idx+1} 篇: 未找到日期")
                continue

            date_str = date_elem.text.strip()
            dt = parse_date(date_str)

            # 提取内容
            content_elem = post.find('div', class_='p-content')
            if not content_elem:
                print(f"跳过 {date_str}: 未找到内容")
                continue

            content_html = content_elem.decode_contents()
            content = clean_content(content_html)

            # 跳过空内容
            if not content:
                print(f"跳过 {date_str}: 内容为空")
                continue

            # 提取图片
            images = []
            pics_div = post.find('div', class_='p-pics')
            if pics_div:
                img_tags = pics_div.find_all('img', class_='p-pic')
                for img in img_tags:
                    src = img.get('src', '')
                    if src:
                        images.append(src)

            # 提取链接（如果有）
            link = None
            link_title = None
            link_elem = post.find('a', class_='p-link')
            if link_elem:
                link = link_elem.get('href', '')
                link_title = link_elem.text.strip()

            # 生成日期slug用于图片文件名
            date_slug = dt.strftime('%Y%m%d%H%M%S')

            # 复制图片
            image_paths = copy_images(images, source_image_dir, target_image_dir, date_slug)
            total_images += len(image_paths)

            # 创建thought条目
            thought = {
                'date': dt.strftime('%Y-%m-%d'),
                'time': dt.strftime('%H:%M'),
                'content': content
            }

            # 添加图片（如果有）
            if image_paths:
                thought['images'] = image_paths

            # 添加链接（如果有）
            if link:
                thought['link'] = link
                if link_title:
                    thought['link_title'] = link_title

            thoughts.append(thought)

            if (idx + 1) % 20 == 0:
                print(f"已处理 {idx + 1} 篇动态...")

        except Exception as e:
            print(f"处理第 {idx+1} 篇动态失败: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n成功解析 {len(thoughts)} 篇动态，复制 {total_images} 张图片")
    return thoughts

def write_thoughts_yml(thoughts, output_file):
    """将thoughts数据写入YAML文件"""

    # 按日期倒序排序
    thoughts_sorted = sorted(thoughts, key=lambda x: x['date'], reverse=True)

    # 读取YAML文件头部注释
    header_comments = """# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 import_jike_from_html.py 自动生成
# 生成时间: {generation_time}
#
# 使用说明：
# 1. 每条动态以 "- date:" 开头
# 2. content 支持 Markdown 格式
# 3. 图片已自动保存到 _pages/files/thoughts/ 目录
# 4. 数据会自动按日期倒序排列，按月份分组显示
#
# ============================================

""".format(generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 手动写入YAML，保持多行格式
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header_comments)

        for thought in thoughts_sorted:
            f.write(f"- date: '{thought['date']}'\n")
            f.write(f"  time: '{thought['time']}'\n")

            # 使用 | 保持多行格式
            f.write("  content: |\n")
            # 每行都缩进4个空格
            for line in thought['content'].split('\n'):
                f.write(f"    {line}\n")

            # 添加图片
            if 'images' in thought and thought['images']:
                f.write("  images:\n")
                for img in thought['images']:
                    f.write(f"  - {img}\n")

            # 添加链接
            if 'link' in thought:
                f.write(f"  link: {thought['link']}\n")
                if 'link_title' in thought:
                    f.write(f"  link_title: {thought['link_title']}\n")

            f.write("\n")

    print(f"\n已写入 {len(thoughts_sorted)} 条动态到 {output_file}")

def main():
    # 文件路径
    html_file = Path("/Users/didi/Desktop/jocker.html")
    source_image_dir = Path("/Users/didi/Desktop/jocker_files")
    target_image_dir = Path("/Users/didi/Desktop/b/atinyhouse.github.io/_pages/files/thoughts")
    output_yml = Path("/Users/didi/Desktop/b/atinyhouse.github.io/_data/thoughts.yml")

    # 确保目录存在
    target_image_dir.mkdir(parents=True, exist_ok=True)
    output_yml.parent.mkdir(parents=True, exist_ok=True)

    # 解析HTML并提取thoughts
    thoughts = parse_html_to_thoughts(html_file, source_image_dir, target_image_dir)

    # 写入YAML文件
    if thoughts:
        write_thoughts_yml(thoughts, output_yml)
        print("\n" + "="*50)
        print("导入完成！")
        print(f"共导入 {len(thoughts)} 条动态")
        print(f"YAML文件: {output_yml}")
        print(f"图片目录: {target_image_dir}")
        print("="*50)
    else:
        print("\n没有可导入的动态！")

if __name__ == "__main__":
    main()
