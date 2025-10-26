#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Jocker 导出的 CSV 文件导入即刻动态
这是最简单可靠的方法！
"""

import csv
import yaml
from datetime import datetime
import os
import sys

def main():
    print("="*60)
    print("📥 从 Jocker CSV 导入即刻动态")
    print("="*60)
    print()

    # 查找 CSV 文件
    print("📂 正在查找 CSV 文件...")
    csv_files = []

    # 检查几个常见位置
    locations = [
        os.path.expanduser("~/Downloads"),  # 下载文件夹
        ".",  # 当前目录
    ]

    for location in locations:
        if os.path.exists(location):
            files = [f for f in os.listdir(location) if f.endswith('.csv') and 'jike' in f.lower() or 'jocker' in f.lower()]
            for f in files:
                csv_files.append(os.path.join(location, f))

    if not csv_files:
        print("❌ 没有找到 Jocker 导出的 CSV 文件")
        print()
        print("请确保：")
        print("1. 已安装 Jocker Chrome 扩展")
        print("2. 访问即刻主页并导出 CSV")
        print("3. CSV 文件在下载文件夹中")
        print()
        csv_path = input("或者，请输入 CSV 文件的完整路径：").strip()
        if not csv_path or not os.path.exists(csv_path):
            print("文件不存在，退出")
            sys.exit(1)
    else:
        print(f"✓ 找到 {len(csv_files)} 个 CSV 文件：")
        for i, f in enumerate(csv_files, 1):
            print(f"  {i}. {os.path.basename(f)}")

        if len(csv_files) == 1:
            csv_path = csv_files[0]
            print(f"\n使用: {os.path.basename(csv_path)}")
        else:
            choice = input("\n请选择文件编号（默认 1）：").strip() or "1"
            csv_path = csv_files[int(choice) - 1]

    print()

    # 读取 CSV
    print("📖 读取 CSV 文件...")
    thoughts = []

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                thought = {}

                # 日期时间
                date_str = row.get('发布时间') or row.get('时间') or row.get('date')
                if date_str:
                    try:
                        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        thought['date'] = dt.strftime('%Y-%m-%d')
                        thought['time'] = dt.strftime('%H:%M')
                    except:
                        # 尝试其他格式
                        try:
                            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            thought['date'] = dt.strftime('%Y-%m-%d')
                            thought['time'] = dt.strftime('%H:%M')
                        except:
                            continue

                # 内容
                content = row.get('内容') or row.get('content') or row.get('正文')
                if content and content.strip():
                    thought['content'] = content.strip()

                # 主题
                topic = row.get('主题') or row.get('topic')
                if topic:
                    thought['topic'] = topic

                if 'date' in thought and 'content' in thought:
                    thoughts.append(thought)

        print(f"✓ 成功读取 {len(thoughts)} 条动态")

    except Exception as e:
        print(f"❌ 读取失败: {e}")
        sys.exit(1)

    if not thoughts:
        print("❌ 没有找到有效的动态数据")
        sys.exit(1)

    print()

    # 保存到 thoughts.yml
    print("💾 保存到 _data/thoughts.yml...")

    output_file = '_data/thoughts.yml'
    os.makedirs('_data', exist_ok=True)

    # 读取现有数据
    existing_thoughts = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = []
                for line in f:
                    if not line.strip().startswith('#'):
                        content.append(line)
                if content:
                    existing_thoughts = yaml.safe_load(''.join(content)) or []
        except:
            pass

    # 合并去重
    thought_keys = set()
    for t in existing_thoughts:
        key = f"{t.get('date')}_{t.get('time')}_{t.get('content', '')[:30]}"
        thought_keys.add(key)

    new_count = 0
    for t in thoughts:
        key = f"{t.get('date')}_{t.get('time')}_{t.get('content', '')[:30]}"
        if key not in thought_keys:
            existing_thoughts.append(t)
            new_count += 1

    # 按时间排序
    existing_thoughts.sort(
        key=lambda x: f"{x.get('date', '9999-99-99')} {x.get('time', '99:99')}",
        reverse=True
    )

    # 保存
    header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 本文件由 从Jocker导入.py 生成
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 共 {len(existing_thoughts)} 条动态
#
# ============================================

"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)
        yaml.dump(existing_thoughts, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"✓ 保存成功！")
    print(f"  - 总计: {len(existing_thoughts)} 条")
    print(f"  - 新增: {new_count} 条")
    print()

    print("="*60)
    print("✅ 导入完成！")
    print("="*60)
    print()
    print("🎉 下一步：")
    print("  1. 运行: bundle exec jekyll serve")
    print("  2. 访问: http://localhost:4000/thoughts/")
    print()
    print("💡 以后如需更新：")
    print("  1. 在 Jocker 中导出新的 CSV")
    print("  2. 再次运行: python3 从Jocker导入.py")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
