#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将即刻动态导入为Jekyll博客文章
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

def clean_title(text):
    """从内容中提取合适的标题"""
    if not text or text.strip() == "":
        return "即刻动态"

    # 移除表情符号和特殊字符
    text = text.strip()

    # 只保留文字，最多取前30个字符作为标题
    # 移除换行符
    text = text.replace('\n', ' ').replace('\r', ' ')

    # 如果内容太短（比如只有emoji），返回默认标题
    if len(text) < 3:
        return "即刻动态"

    # 取前30个字符
    title = text[:30]

    # 如果结尾不是标点符号，找最后一个空格或标点截断
    if len(text) > 30:
        # 找最后一个标点或空格
        for i in range(len(title)-1, 0, -1):
            if title[i] in '，。！？；：、 ':
                title = title[:i]
                break
        title += "..."

    return title.strip()

def generate_filename(date_str, title):
    """生成Jekyll文章的文件名"""
    # 解析日期
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    date_prefix = dt.strftime('%Y-%m-%d')

    # 清理标题用于文件名
    # 移除特殊字符，保留中文、英文、数字
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    safe_title = safe_title[:50]  # 限制长度

    if not safe_title or safe_title == '-':
        safe_title = "jike-post"

    return f"{date_prefix}-{safe_title}.md"

def create_jekyll_post(date_str, topic, content, output_dir):
    """创建Jekyll格式的文章"""

    # 生成标题
    title = clean_title(content)

    # 如果标题太短或者就是emoji，使用主题作为标题的一部分
    if len(title) < 5 or title == "即刻动态":
        if topic and len(topic) > 0:
            title = f"{topic}"
        else:
            title = "即刻动态"

    # 生成文件名
    filename = generate_filename(date_str, title)
    filepath = output_dir / filename

    # 如果文件已存在，添加序号
    counter = 1
    while filepath.exists():
        base_name = filename.replace('.md', '')
        filename = f"{base_name}-{counter}.md"
        filepath = output_dir / filename
        counter += 1

    # 解析日期用于front matter
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

    # 根据主题确定标签
    tag = "Life"
    if "音乐" in topic or "演出" in topic:
        tag = "Music"
    elif "摄影" in topic or "拍照" in topic:
        tag = "Photography"
    elif "日记" in topic:
        tag = "Diary"
    elif "产品" in topic or "Apple" in topic or "苹果" in topic:
        tag = "Tech"

    # 创建front matter
    front_matter = f"""---
layout: post
title: "{title}"
author: "Lucca"
comments: false
tags: {tag}
excerpt_separator: <!--more-->
sticky: false
hidden: false
source: jike
topic: "{topic}"
date: {dt.strftime('%Y-%m-%d %H:%M:%S +0800')}
---

"""

    # 处理内容
    # 如果内容很短，直接显示；如果很长，添加摘要分隔符
    if len(content) > 200:
        # 找第一个换行或者前100个字符作为摘要
        summary_end = content.find('\n\n')
        if summary_end > 0 and summary_end < 200:
            content_with_more = content[:summary_end] + "\n\n<!--more-->\n\n" + content[summary_end:]
        else:
            # 在第一个段落结束处插入
            content_with_more = content[:100] + "\n\n<!--more-->\n\n" + content[100:]
    else:
        content_with_more = content + "\n\n<!--more-->"

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content_with_more)
        f.write("\n")

    return filename

def main():
    # 文件路径
    csv_file = Path("/Users/didi/Downloads/2025-10-24-所有动态-jocker-backup.csv")
    output_dir = Path("/Users/didi/Desktop/b/atinyhouse.github.io/_posts")

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 统计信息
    total_count = 0
    success_count = 0
    error_count = 0

    # 读取CSV文件
    print(f"开始读取CSV文件: {csv_file}")

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_count += 1

            try:
                date_str = row['发布时间']
                topic = row['主题']
                content = row['内容']

                # 跳过空内容
                if not content or content.strip() == "":
                    print(f"跳过空内容: {date_str}")
                    continue

                # 创建文章
                filename = create_jekyll_post(date_str, topic, content, output_dir)
                success_count += 1

                if success_count % 50 == 0:
                    print(f"已处理 {success_count} 篇文章...")

            except Exception as e:
                error_count += 1
                print(f"处理失败 (行 {total_count}): {e}")
                continue

    # 输出统计信息
    print("\n" + "="*50)
    print(f"处理完成！")
    print(f"总共读取: {total_count} 条")
    print(f"成功转换: {success_count} 篇")
    print(f"失败: {error_count} 篇")
    print(f"输出目录: {output_dir}")
    print("="*50)

if __name__ == "__main__":
    main()
