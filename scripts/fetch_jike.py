#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻动态自动获取脚本
使用方法：python scripts/fetch_jike.py
"""

import requests
import json
import yaml
from datetime import datetime
import os
import sys

# 即刻用户 ID
USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"

# 即刻 API 端点
JIKE_API = "https://api.ruguoapp.com/1.0/users/{}/posts"

def fetch_jike_posts(user_id, limit=20):
    """
    获取即刻用户的动态
    """
    url = JIKE_API.format(user_id)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    params = {
        'limit': limit,
        'loadMoreKey': None
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取即刻数据失败: {e}")
        return None

def parse_jike_post(post):
    """
    解析即刻动态数据
    """
    thought = {}

    # 日期时间
    created_at = post.get('createdAt')
    if created_at:
        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        thought['date'] = dt.strftime('%Y-%m-%d')
        thought['time'] = dt.strftime('%H:%M')

    # 内容
    content = post.get('content', '').strip()
    if content:
        thought['content'] = content

    # 图片
    pictures = post.get('pictures', [])
    if pictures:
        thought['images'] = [pic.get('picUrl') or pic.get('thumbnailUrl') for pic in pictures if pic]

    # 链接
    url_info = post.get('urlsInText', [])
    if url_info:
        url = url_info[0].get('url')
        title = url_info[0].get('title', '查看链接')
        if url:
            thought['link'] = url
            thought['link_title'] = title

    # 话题
    topic = post.get('topic')
    if topic:
        topic_name = topic.get('content')
        if topic_name and content:
            thought['content'] = f"#{topic_name}#\n\n{content}"

    return thought if thought else None

def update_thoughts_file(thoughts, output_file='_data/thoughts.yml'):
    """
    更新 thoughts.yml 文件
    """
    # 读取现有文件的注释头部
    header_lines = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith('#') or line.strip() == '':
                    header_lines.append(line)
                else:
                    break

    # 如果没有头部，添加默认头部
    if not header_lines:
        header_lines = [
            "# ============================================\n",
            "# Thoughts 数据文件 - 即刻动态（自动生成）\n",
            "# ============================================\n",
            "#\n",
            f"# 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"# 共 {len(thoughts)} 条动态\n",
            "#\n",
            "# ============================================\n",
            "\n"
        ]

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(header_lines)
        yaml.dump(thoughts, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"✅ 成功更新 {output_file}，共 {len(thoughts)} 条动态")

def main():
    print("🚀 开始获取即刻动态...")
    print(f"📱 用户 ID: {USER_ID}")

    # 获取动态
    posts = fetch_jike_posts(USER_ID, limit=50)

    if posts is None:
        print("\n💡 提示：即刻可能需要登录才能访问 API")
        print("请尝试方法二：使用浏览器开发者工具手动获取数据")
        sys.exit(1)

    if not posts:
        print("⚠️  没有获取到任何动态")
        sys.exit(1)

    print(f"📥 成功获取 {len(posts)} 条动态")

    # 解析动态
    thoughts = []
    for post in posts:
        thought = parse_jike_post(post)
        if thought:
            thoughts.append(thought)

    print(f"✨ 成功解析 {len(thoughts)} 条有效动态")

    # 更新文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_file = os.path.join(project_dir, '_data', 'thoughts.yml')

    update_thoughts_file(thoughts, output_file)

    print("\n✅ 完成！现在可以运行 'bundle exec jekyll serve' 查看效果")

if __name__ == '__main__':
    main()
