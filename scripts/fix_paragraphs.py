#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复thoughts.yml中的段落格式，正确处理HTML中的分段
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date(date_str):
    """解析日期字符串"""
    try:
        dt = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
        return dt
    except:
        return datetime.now()

def clean_content_with_paragraphs(content_html):
    """清理HTML内容，保留段落分隔"""
    # 先将<br><br>替换为段落标记
    content = content_html.replace('<br><br>', '\n\n')
    # 将剩余的单个<br>替换为换行（保留诗歌形式）
    content = content.replace('<br>', '\n')
    # 移除其他HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    # 清理多余空白（但保留段落间的双换行）
    content = re.sub(r' +', ' ', content)  # 多个空格变成一个
    content = re.sub(r'\n{3,}', '\n\n', content)  # 3个以上换行变成两个
    # 清理每行首尾空白
    lines = []
    for line in content.split('\n'):
        lines.append(line.strip())
    return '\n'.join(lines)

# 读取HTML
html_file = Path("/Users/didi/Desktop/jocker.html")
print(f"读取HTML文件: {html_file}")

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
posts = soup.find_all('div', class_='post-default')

print(f"找到 {len(posts)} 篇动态\n")

# 读取现有的thoughts.yml来匹配日期
output_file = Path("/Users/didi/Desktop/b/atinyhouse.github.io/_data/thoughts.yml")

# 创建日期到内容的映射
date_to_content = {}

for post in posts:
    date_elem = post.find('span', class_='p-date')
    content_elem = post.find('div', class_='p-content')

    if date_elem and content_elem:
        date_str = date_elem.text.strip()
        dt = parse_date(date_str)
        date_key = dt.strftime('%Y-%m-%d-%H-%M')

        content_html = content_elem.decode_contents()
        content_clean = clean_content_with_paragraphs(content_html)

        date_to_content[date_key] = content_clean

print(f"解析完成，共 {len(date_to_content)} 条动态")

# 读取现有YAML文件
with open(output_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 重新生成YAML，保留头部注释
output_lines = []
in_content = False
current_date_key = None
skip_until_next = False

for i, line in enumerate(lines):
    # 保留注释和头部
    if line.strip().startswith('#') or (i < 20 and line.strip() == ''):
        output_lines.append(line)
        continue

    # 检测到新的条目
    if line.startswith('- date:'):
        in_content = False
        skip_until_next = False
        output_lines.append(line)

        # 提取日期
        date_match = re.search(r"'(\d{4}-\d{2}-\d{2})'", line)
        if date_match:
            current_date = date_match.group(1)
            # 读取下一行的时间
            if i+1 < len(lines) and 'time:' in lines[i+1]:
                time_match = re.search(r"'?(\d{1,2}:\d{2})'?", lines[i+1])
                if time_match:
                    current_time = time_match.group(1)
                    current_date_key = f"{current_date}-{current_time.replace(':', '-')}"

    elif line.strip().startswith('time:'):
        output_lines.append(line)

    elif line.strip() == 'content: |':
        in_content = True
        output_lines.append(line)

        # 如果找到对应的日期，用新内容替换
        if current_date_key and current_date_key in date_to_content:
            new_content = date_to_content[current_date_key]
            for content_line in new_content.split('\n'):
                output_lines.append(f"    {content_line}\n")
            skip_until_next = True

    elif in_content and skip_until_next:
        # 跳过旧的内容行，直到遇到images或下一个条目
        if line.strip().startswith('images:') or line.strip().startswith('link:') or line.startswith('- date:'):
            in_content = False
            skip_until_next = False
            output_lines.append(line)

    else:
        output_lines.append(line)

# 写回文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"\n✅ 已更新 {output_file}")
print("所有段落格式已修复！")
