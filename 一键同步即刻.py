#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻动态一键同步脚本 - 小白专用版
只需要粘贴 Token，自动完成所有操作
"""

import os
import sys

def main():
    print("="*60)
    print("🌟 即刻动态一键同步工具 - 小白专用版")
    print("="*60)
    print()

    # 检查是否在正确的目录
    if not os.path.exists('scripts/sync_jike_v2.py'):
        print("❌ 错误：请在博客根目录运行此脚本")
        print("当前目录:", os.getcwd())
        print()
        print("正确的运行方式：")
        print("  cd /Users/caoxiaolu/atinyhouse.github.io")
        print("  python 一键同步即刻.py")
        sys.exit(1)

    print("📋 第一步：获取即刻 Token")
    print()
    print("请按照以下步骤操作：")
    print("  1. 打开 https://web.okjike.com/u/71A6B3C3-1382-4121-A17A-2A4C05CB55E8")
    print("  2. 按 F12 打开开发者工具")
    print("  3. 点击 Network（网络）标签")
    print("  4. 按 Command+R 刷新页面")
    print("  5. 找到包含 'graphql' 的请求")
    print("  6. 在右侧 Headers 中找到 'x-jike-access-token'")
    print("  7. 复制那个很长的 token（以 eyJ 开头）")
    print()

    # 获取 token
    token = input("👉 请粘贴您的 Token 到这里，然后按回车：").strip()

    if not token:
        print("\n❌ Token 不能为空！")
        sys.exit(1)

    if not token.startswith('eyJ'):
        print("\n⚠️  警告：Token 通常以 'eyJ' 开头，请检查是否复制正确")
        confirm = input("是否继续？(y/n): ").strip().lower()
        if confirm != 'y':
            sys.exit(0)

    print()
    print("✓ Token 已获取")
    print()

    # 设置环境变量
    os.environ['JIKE_ACCESS_TOKEN'] = token
    os.environ['JIKE_USER_ID'] = '71A6B3C3-1382-4121-A17A-2A4C05CB55E8'

    # 检查依赖
    print("📦 第二步：检查 Python 依赖...")
    print()

    try:
        import requests
        import yaml
        import pytz
        print("✓ 所有依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print()
        print("正在自动安装依赖...")
        os.system('pip install -q requests PyYAML pytz')
        print("✓ 依赖安装完成")

    print()

    # 运行同步
    print("🚀 第三步：开始同步即刻动态...")
    print("="*60)
    print()

    # 切换到 scripts 目录并运行
    os.chdir('scripts')
    result = os.system('python sync_jike_v2.py')
    os.chdir('..')

    print()
    print("="*60)

    if result == 0:
        print("✅ 同步成功！")
        print()
        print("🎉 下一步：")
        print("  1. 运行: bundle exec jekyll serve")
        print("  2. 访问: http://localhost:4000/thoughts/")
        print("  3. 查看您的即刻动态时间线")
        print()
        print("💡 提示：")
        print("  - 如需再次同步，直接运行：python 一键同步即刻.py")
        print("  - Token 会在约 30 天后过期，届时需重新获取")
    else:
        print("❌ 同步失败")
        print()
        print("可能的原因：")
        print("  1. Token 已过期或无效")
        print("  2. 网络连接问题")
        print("  3. 即刻 API 服务异常")
        print()
        print("建议：")
        print("  - 重新获取 Token 并再次运行")
        print("  - 查看上方的错误信息")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消操作")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
