#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻动态自动同步脚本 V2
使用即刻 GraphQL API 获取动态并同步到博客

使用方法：
1. 设置环境变量：
   export JIKE_ACCESS_TOKEN="your_access_token"
   export JIKE_USER_ID="71A6B3C3-1382-4121-A17A-2A4C05CB55E8"

2. 运行脚本：
   python scripts/sync_jike_v2.py

作者: Claude Code
更新时间: 2025-10-25
"""

import requests
import json
import yaml
from datetime import datetime
import os
import sys
from pathlib import Path
import time
import hashlib
from urllib.parse import urlparse

# ============================================
# 配置
# ============================================

# 即刻用户 ID（从环境变量或默认值获取）
USER_ID = os.getenv('JIKE_USER_ID', '71A6B3C3-1382-4121-A17A-2A4C05CB55E8')

# 即刻 GraphQL API 端点
JIKE_API = "https://web-api.okjike.com/api/graphql"

# 图片保存目录
IMAGES_DIR = "_pages/files/thoughts"

# 每次获取的数量
FETCH_LIMIT = 50

# ============================================
# 即刻 API 调用
# ============================================

def get_jike_token():
    """从环境变量获取即刻 token"""
    token = os.getenv('JIKE_ACCESS_TOKEN')
    if not token:
        print("❌ 错误：未设置 JIKE_ACCESS_TOKEN 环境变量")
        print("\n请先设置：")
        print("  export JIKE_ACCESS_TOKEN='your_token'")
        print("\n获取 token 的方法：")
        print("  1. 访问 https://web.okjike.com")
        print("  2. 登录账号")
        print("  3. 打开浏览器开发者工具 (F12)")
        print("  4. 在 Network 标签中找到任意 API 请求")
        print("  5. 查看 Request Headers 中的 x-jike-access-token")
        sys.exit(1)
    return token

def fetch_user_posts(token, user_id, limit=50, load_more_key=None):
    """
    使用 GraphQL 获取用户动态
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-jike-access-token': token,
    }

    # GraphQL 查询
    query = """
    query GetUserProfile($username: String!) {
      userProfile(username: $username) {
        username
        screenName
        briefIntro
        feeds(limit: 50, loadMoreKey: null) {
          nodes {
            ... on OriginalPost {
              id
              type
              content
              createdAt
              pictures {
                picUrl
                thumbnailUrl
              }
              urlsInText {
                url
                title
              }
              topic {
                content
              }
            }
            ... on Repost {
              id
              type
              content
              createdAt
              target {
                ... on OriginalPost {
                  content
                  pictures {
                    picUrl
                    thumbnailUrl
                  }
                }
              }
            }
          }
          pageInfo {
            loadMoreKey
            hasNextPage
          }
        }
      }
    }
    """

    variables = {
        "username": user_id
    }

    payload = {
        "operationName": "GetUserProfile",
        "query": query,
        "variables": variables
    }

    try:
        response = requests.post(
            JIKE_API,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            print(f"❌ API 错误: {data['errors']}")
            return None, None

        user_profile = data.get('data', {}).get('userProfile', {})
        feeds = user_profile.get('feeds', {})
        nodes = feeds.get('nodes', [])
        page_info = feeds.get('pageInfo', {})

        return nodes, page_info.get('loadMoreKey')

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print(f"响应内容: {response.text[:500]}")
        return None, None

# ============================================
# 数据解析
# ============================================

def parse_post(post):
    """
    解析即刻动态数据
    """
    thought = {}

    # 日期时间
    created_at = post.get('createdAt')
    if created_at:
        # 处理时间格式
        try:
            # 移除毫秒部分的多余位数
            if '.' in created_at:
                parts = created_at.split('.')
                created_at = parts[0] + '.' + parts[1][:6] + parts[1][-1]

            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            # 转换为北京时间 (UTC+8)
            import pytz
            beijing_tz = pytz.timezone('Asia/Shanghai')
            dt_beijing = dt.astimezone(beijing_tz)

            thought['date'] = dt_beijing.strftime('%Y-%m-%d')
            thought['time'] = dt_beijing.strftime('%H:%M')
        except Exception as e:
            print(f"⚠️  时间解析失败: {created_at}, 错误: {e}")
            return None

    # 内容
    content = post.get('content', '').strip()

    # 如果是转发，获取原始内容
    if post.get('type') == 'REPOST':
        target = post.get('target', {})
        if target:
            original_content = target.get('content', '')
            if content and original_content:
                content = f"{content}\n\n// 转发：\n{original_content}"
            elif original_content:
                content = original_content

    if content:
        thought['content'] = content

    # 图片
    pictures = post.get('pictures', [])
    if not pictures and post.get('type') == 'REPOST':
        target = post.get('target', {})
        pictures = target.get('pictures', [])

    if pictures:
        # 只保留图片 URL，稍后下载
        thought['images_urls'] = []
        for pic in pictures:
            pic_url = pic.get('picUrl') or pic.get('thumbnailUrl')
            if pic_url:
                thought['images_urls'].append(pic_url)

    # 链接
    urls = post.get('urlsInText', [])
    if urls:
        url = urls[0].get('url')
        title = urls[0].get('title', '查看链接')
        if url:
            thought['link'] = url
            thought['link_title'] = title

    # 话题
    topic = post.get('topic')
    if topic:
        topic_name = topic.get('content', '')
        if topic_name:
            thought['topic'] = topic_name

    # 动态 ID（用于去重）
    post_id = post.get('id')
    if post_id:
        thought['id'] = post_id

    return thought if 'content' in thought or 'images_urls' in thought else None

# ============================================
# 图片下载
# ============================================

def download_image(url, save_dir):
    """
    下载图片并返回本地路径
    """
    try:
        # 创建保存目录
        os.makedirs(save_dir, exist_ok=True)

        # 生成文件名（使用 URL 的 hash）
        url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
        ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
        filename = f"{url_hash}{ext}"
        filepath = os.path.join(save_dir, filename)

        # 如果文件已存在，直接返回
        if os.path.exists(filepath):
            return f"/{filepath}"

        # 下载图片
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"/{filepath}"

    except Exception as e:
        print(f"⚠️  图片下载失败: {url}, 错误: {e}")
        return url  # 下载失败则使用原始 URL

# ============================================
# 数据管理
# ============================================

def load_existing_thoughts(file_path):
    """加载现有的 thoughts 数据"""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 跳过注释行
            content = []
            for line in f:
                if not line.strip().startswith('#'):
                    content.append(line)

            if not content:
                return []

            data = yaml.safe_load(''.join(content))
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"⚠️  读取现有数据失败: {e}")
        return []

def merge_thoughts(existing, new_thoughts):
    """
    合并新旧数据，去重并按时间排序
    """
    # 创建 ID 到 thought 的映射
    thought_map = {}

    # 先添加现有数据
    for thought in existing:
        # 使用 date + time + content 的前50字符作为唯一标识
        key = f"{thought.get('date')}_{thought.get('time')}_{thought.get('content', '')[:50]}"
        thought_map[key] = thought

    # 添加新数据
    new_count = 0
    for thought in new_thoughts:
        key = f"{thought.get('date')}_{thought.get('time')}_{thought.get('content', '')[:50]}"
        if key not in thought_map:
            thought_map[key] = thought
            new_count += 1

    # 转换为列表并按日期时间排序
    all_thoughts = list(thought_map.values())
    all_thoughts.sort(
        key=lambda x: f"{x.get('date', '9999-99-99')} {x.get('time', '99:99')}",
        reverse=True
    )

    return all_thoughts, new_count

def save_thoughts(thoughts, file_path):
    """保存 thoughts 数据"""
    # 创建文件头部
    header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 sync_jike_v2.py 自动生成
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# 使用说明：
# 1. 每条动态以 "- date:" 开头
# 2. content 支持 Markdown 格式
# 3. 图片已自动保存到 _pages/files/thoughts/ 目录
# 4. 数据会自动按日期倒序排列，按月份分组显示
#
# ============================================

"""

    # 保存文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header)
            # 清理数据中的临时字段
            clean_thoughts = []
            for thought in thoughts:
                clean_thought = {k: v for k, v in thought.items() if k != 'images_urls' and k != 'id'}
                clean_thoughts.append(clean_thought)

            yaml.dump(
                clean_thoughts,
                f,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=1000
            )

        print(f"✅ 成功保存 {len(thoughts)} 条动态到 {file_path}")
        return True

    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

# ============================================
# 主流程
# ============================================

def main():
    print("="*60)
    print("🚀 即刻动态同步脚本 V2")
    print("="*60)
    print()

    # 获取 token
    token = get_jike_token()
    print(f"✓ Token: {token[:10]}...{token[-10:]}")
    print(f"✓ 用户 ID: {USER_ID}")
    print()

    # 获取动态
    print("📥 开始获取即刻动态...")
    posts, load_more_key = fetch_user_posts(token, USER_ID, limit=FETCH_LIMIT)

    if posts is None:
        print("\n❌ 获取失败，请检查：")
        print("  1. Token 是否正确")
        print("  2. 用户 ID 是否正确")
        print("  3. 网络连接是否正常")
        sys.exit(1)

    if not posts:
        print("⚠️  没有获取到任何动态")
        sys.exit(0)

    print(f"✓ 成功获取 {len(posts)} 条动态")
    print()

    # 解析动态
    print("🔄 解析动态数据...")
    new_thoughts = []
    for post in posts:
        thought = parse_post(post)
        if thought:
            new_thoughts.append(thought)

    print(f"✓ 成功解析 {len(new_thoughts)} 条有效动态")
    print()

    # 下载图片
    print("📷 下载图片...")
    for thought in new_thoughts:
        if 'images_urls' in thought:
            images = []
            for url in thought['images_urls']:
                local_path = download_image(url, IMAGES_DIR)
                images.append(local_path)
                print(f"  ✓ {os.path.basename(local_path)}")

            thought['images'] = images
            time.sleep(0.5)  # 避免请求过快

    print()

    # 加载现有数据
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    data_file = project_dir / '_data' / 'thoughts.yml'

    print("📂 读取现有数据...")
    existing_thoughts = load_existing_thoughts(data_file)
    print(f"✓ 现有 {len(existing_thoughts)} 条动态")
    print()

    # 合并数据
    print("🔗 合并数据...")
    all_thoughts, new_count = merge_thoughts(existing_thoughts, new_thoughts)
    print(f"✓ 合并完成: 总共 {len(all_thoughts)} 条，新增 {new_count} 条")
    print()

    # 保存数据
    print("💾 保存数据...")
    if save_thoughts(all_thoughts, data_file):
        print()
        print("="*60)
        print("✅ 同步完成！")
        print(f"📊 统计: 总计 {len(all_thoughts)} 条，本次新增 {new_count} 条")
        print()
        print("💡 下一步：")
        print("  1. 运行 'bundle exec jekyll serve' 预览")
        print("  2. 访问 http://localhost:4000/thoughts/ 查看效果")
        print("="*60)
    else:
        print("\n❌ 同步失败")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
