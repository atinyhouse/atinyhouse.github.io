#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻动态 JSON 解析脚本（从浏览器复制数据）

使用步骤：
1. 打开浏览器，访问你的即刻主页
2. 按 F12 打开开发者工具，切换到 Network（网络）标签
3. 刷新页面，找到名为 "posts" 或包含动态数据的请求
4. 右键 -> Copy -> Copy Response（复制响应内容）
5. 将复制的内容保存为 jike_data.json
6. 运行此脚本：python scripts/parse_jike_json.py jike_data.json
"""

import json
import yaml
from datetime import datetime
import os
import sys
import re

def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    # 移除多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def parse_jike_post(post):
    """
    解析单条即刻动态
    支持多种 JSON 格式
    """
    thought = {}

    # 尝试不同的日期字段名
    created_at = post.get('createdAt') or post.get('created_at') or post.get('createTime')
    if created_at:
        try:
            # 处理不同的时间格式
            if isinstance(created_at, str):
                # ISO 格式
                if 'T' in created_at:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                # 时间戳（毫秒）
                elif len(created_at) > 10:
                    dt = datetime.fromtimestamp(int(created_at) / 1000)
                # 时间戳（秒）
                else:
                    dt = datetime.fromtimestamp(int(created_at))
            elif isinstance(created_at, (int, float)):
                # 数字时间戳
                if created_at > 10000000000:  # 毫秒
                    dt = datetime.fromtimestamp(created_at / 1000)
                else:  # 秒
                    dt = datetime.fromtimestamp(created_at)
            else:
                dt = None

            if dt:
                thought['date'] = dt.strftime('%Y-%m-%d')
                thought['time'] = dt.strftime('%H:%M')
        except (ValueError, TypeError) as e:
            print(f"⚠️  时间解析失败: {e}")

    # 内容文本
    content = post.get('content') or post.get('text') or post.get('message', '')
    content = clean_text(content)
    if content:
        thought['content'] = content

    # 图片
    pictures = post.get('pictures') or post.get('images') or []
    if pictures:
        image_urls = []
        for pic in pictures:
            if isinstance(pic, str):
                image_urls.append(pic)
            elif isinstance(pic, dict):
                url = (pic.get('picUrl') or
                      pic.get('thumbnailUrl') or
                      pic.get('middlePicUrl') or
                      pic.get('url') or
                      pic.get('src'))
                if url:
                    image_urls.append(url)
        if image_urls:
            thought['images'] = image_urls

    # 链接
    urls = post.get('urlsInText') or post.get('urls') or []
    if urls and isinstance(urls, list) and len(urls) > 0:
        url_obj = urls[0]
        if isinstance(url_obj, dict):
            url = url_obj.get('url')
            title = url_obj.get('title') or url_obj.get('text') or '查看链接'
            if url:
                thought['link'] = url
                thought['link_title'] = title
        elif isinstance(url_obj, str):
            thought['link'] = url_obj
            thought['link_title'] = '查看链接'

    # 话题
    topic = post.get('topic')
    if topic and isinstance(topic, dict):
        topic_name = topic.get('content') or topic.get('name') or topic.get('title')
        if topic_name and content:
            thought['content'] = f"#{topic_name}#\n\n{content}"

    return thought if ('content' in thought or 'images' in thought) else None

def parse_json_file(json_file):
    """
    解析 JSON 文件
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {json_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return None

    # 尝试找到动态数据数组
    posts = None

    # 常见的数据结构
    if isinstance(data, list):
        posts = data
    elif isinstance(data, dict):
        # 尝试不同的字段名
        posts = (data.get('data') or
                data.get('posts') or
                data.get('items') or
                data.get('list'))

        # 如果 data 是字典，再深入一层
        if isinstance(posts, dict):
            posts = (posts.get('data') or
                    posts.get('posts') or
                    posts.get('items'))

    if not posts or not isinstance(posts, list):
        print("❌ 无法找到动态数据数组")
        print("💡 提示：请确保复制的是完整的 API 响应数据")
        return None

    return posts

def update_thoughts_file(thoughts, output_file='_data/thoughts.yml'):
    """
    更新 thoughts.yml 文件
    """
    # 创建目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 生成头部注释
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

    print(f"✅ 成功写入 {output_file}")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python scripts/parse_jike_json.py <json_file>")
        print("\n步骤说明：")
        print("1. 访问即刻主页: https://web.okjike.com/u/71A6B3C3-1382-4121-A17A-2A4C05CB55E8")
        print("2. F12 打开开发者工具 -> Network 标签")
        print("3. 刷新页面，找到包含动态数据的请求（通常是 userPost 或类似名称）")
        print("4. 右键该请求 -> Copy -> Copy Response")
        print("5. 保存为 jike_data.json")
        print("6. 运行: python scripts/parse_jike_json.py jike_data.json")
        sys.exit(1)

    json_file = sys.argv[1]

    print(f"📖 读取 JSON 文件: {json_file}")

    # 解析 JSON
    posts = parse_json_file(json_file)
    if not posts:
        sys.exit(1)

    print(f"📥 找到 {len(posts)} 条动态数据")

    # 解析每条动态
    thoughts = []
    for i, post in enumerate(posts, 1):
        thought = parse_jike_post(post)
        if thought:
            thoughts.append(thought)
            print(f"  ✓ 解析第 {i} 条: {thought.get('date', '未知日期')}")
        else:
            print(f"  ✗ 跳过第 {i} 条（无有效内容）")

    if not thoughts:
        print("❌ 没有解析到任何有效动态")
        sys.exit(1)

    print(f"\n✨ 成功解析 {len(thoughts)} 条有效动态")

    # 确定输出路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_file = os.path.join(project_dir, '_data', 'thoughts.yml')

    # 更新文件
    update_thoughts_file(thoughts, output_file)

    print("\n✅ 完成！")
    print("💡 下一步: 运行 'bundle exec jekyll serve' 查看效果")

if __name__ == '__main__':
    main()
