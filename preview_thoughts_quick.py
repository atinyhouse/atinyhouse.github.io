#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速生成thoughts页面预览
"""

import yaml
from pathlib import Path

# 读取thoughts数据
thoughts_file = Path("_data/thoughts.yml")
with open(thoughts_file, 'r', encoding='utf-8') as f:
    content = f.read()
    # 移除注释部分
    yaml_content = '\n'.join([line for line in content.split('\n') if not line.strip().startswith('#')])
    thoughts = yaml.safe_load(yaml_content)

# 生成HTML
html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thoughts - 即刻动态预览</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #fcfcfc;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 680px;
            margin: 0 auto;
            padding: 48px 24px;
        }
        .header {
            text-align: center;
            margin-bottom: 64px;
            padding-bottom: 32px;
            border-bottom: 1px solid #e0e0e0;
        }
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 16px;
        }
        .subtitle {
            font-size: 1rem;
            color: #666;
        }
        .timeline {
            position: relative;
        }
        .timeline::before {
            content: '';
            position: absolute;
            left: 20px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #e0e0e0;
        }
        .thought-item {
            position: relative;
            margin-bottom: 40px;
            padding-left: 56px;
        }
        .thought-item::before {
            content: '';
            position: absolute;
            left: 14px;
            top: 8px;
            width: 14px;
            height: 14px;
            background: #fcfcfc;
            border: 3px solid #999;
            border-radius: 50%;
        }
        .thought-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
        }
        .thought-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        .thought-date {
            font-size: 0.875rem;
            color: #999;
            margin-bottom: 12px;
            font-weight: 500;
        }
        .thought-content {
            font-size: 1rem;
            line-height: 1.7;
            color: #333;
            white-space: pre-wrap;
            margin-bottom: 12px;
        }
        .thought-images {
            margin-top: 16px;
            display: grid;
            gap: 12px;
        }
        .thought-images.single { grid-template-columns: 1fr; }
        .thought-images.double { grid-template-columns: repeat(2, 1fr); }
        .thought-images.multiple { grid-template-columns: repeat(3, 1fr); }
        .thought-image {
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
            aspect-ratio: 1;
            object-fit: cover;
            cursor: pointer;
        }
        .thought-link {
            margin-top: 16px;
            padding: 12px 16px;
            background: #f5f5f5;
            border-radius: 8px;
            text-decoration: none;
            display: block;
            color: #0066cc;
            border: 1px solid transparent;
        }
        .thought-link:hover {
            border-color: #0066cc;
            background: #e8e8e8;
        }
        .month-divider {
            display: flex;
            align-items: center;
            gap: 16px;
            margin: 48px 0 32px 0;
            padding-left: 56px;
        }
        .month-divider::before,
        .month-divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #e0e0e0;
        }
        .month-divider span {
            font-size: 1.1rem;
            font-weight: 600;
            color: #666;
            white-space: nowrap;
        }
        .stats {
            text-align: center;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-bottom: 32px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Thoughts</h1>
            <p class="subtitle">一些碎碎念，来自即刻</p>
        </div>

        <div class="stats">
            共 {total_count} 条动态，{total_images} 张图片
        </div>

        <div class="timeline">
"""

# 按月份分组
from collections import defaultdict
from datetime import datetime

months = defaultdict(list)
total_images = 0

for thought in thoughts:
    if thought:
        month_key = thought['date'][:7]  # YYYY-MM
        months[month_key].append(thought)
        if 'images' in thought:
            total_images += len(thought['images'])

# 按月份倒序
sorted_months = sorted(months.keys(), reverse=True)

html = html.replace('{total_count}', str(len(thoughts)))
html = html.replace('{total_images}', str(total_images))

# 生成每个月的内容
for idx, month in enumerate(sorted_months):
    if idx > 0:
        year, month_num = month.split('-')
        html += f'''
            <div class="month-divider">
                <span>{year}年{month_num}月</span>
            </div>
        '''

    # 该月的所有thoughts，按日期倒序
    month_thoughts = sorted(months[month], key=lambda x: x['date'], reverse=True)

    for thought in month_thoughts:
        date_obj = datetime.strptime(thought['date'], '%Y-%m-%d')
        date_str = f"{date_obj.month}月{date_obj.day}日"
        if 'time' in thought:
            date_str += f" {thought['time']}"

        html += f'''
            <div class="thought-item">
                <div class="thought-card">
                    <div class="thought-date">{date_str}</div>
                    <div class="thought-content">{thought['content']}</div>
        '''

        # 添加图片
        if 'images' in thought and thought['images']:
            img_count = len(thought['images'])
            grid_class = 'single' if img_count == 1 else ('double' if img_count == 2 else 'multiple')
            html += f'<div class="thought-images {grid_class}">'
            for img_path in thought['images']:
                # 修正路径：去掉开头的斜杠，使其成为相对路径
                fixed_path = img_path.lstrip('/')
                html += f'<img src="{fixed_path}" alt="图片" class="thought-image" loading="lazy">'
            html += '</div>'

        # 添加链接
        if 'link' in thought and thought['link']:
            link_title = thought.get('link_title', '查看链接')
            html += f'''
                <a href="{thought['link']}" class="thought-link" target="_blank">
                    {link_title}
                </a>
            '''

        html += '''
                </div>
            </div>
        '''

html += """
        </div>
    </div>

    <script>
    // 图片点击放大
    document.querySelectorAll('.thought-image').forEach(img => {
        img.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; display: flex; align-items: center; justify-content: center; cursor: zoom-out;';

            const modalImg = document.createElement('img');
            modalImg.src = this.src;
            modalImg.style.cssText = 'max-width: 90%; max-height: 90%; object-fit: contain;';

            modal.appendChild(modalImg);
            document.body.appendChild(modal);

            modal.addEventListener('click', () => {
                document.body.removeChild(modal);
            });
        });
    });
    </script>
</body>
</html>
"""

# 写入文件
output_file = Path("preview_thoughts_quick.html")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"预览文件已生成: {output_file.absolute()}")
