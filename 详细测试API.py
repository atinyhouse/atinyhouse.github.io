#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试即刻 API - 找出真正的调用方式
"""

import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoicnVMZk40Vkk1K28xb2hvbzNIbzZSVGpDTlNcL1FYZ3JLQm16NUd4MVA4MWs4d0s0djFDUDB2NU02ZGgyTFd4dE8zMVhiejErMmxWbTV1c2F2aGQ3ODcyTExhQUZsXC9ZaFwvbG1zdGQxMkwzaE5pMHhtaWlFcDhXUjlySFJOTVJJbVZKMnV2MmVXaHFEb0wzcDBTV2VUOThscmhqdEI1aWFLVmVoeHZDYjZKM3VWWjM4Tmo5ME1BSVU4K0dxczY4OXhGMWNvckorQkJCRHNPUUVPeHhtUWMwNmVQYlJJbXVXenR2QUtHSmVcL2U0OVV5T0M1TEp6aTl1ZXZvdldGMVVyOXJTQVJXN1hsbDlvamdwVDVJbWVRZjkwTE1aWlAwQmN5bHltY2wyUTdYWlowdENHVW91U0tSdlwvV1IzdkswdUFwQzE5UU9cL1JXUzg4dlM3S0I3NUx4NGV5M2ZieDVDNDRiOVwvTWs3Z25tOUNPND0iLCJ2IjozLCJpdiI6InVmdUZsNDBzNGVZUldoNUZJc1dVdnc9PSIsImlhdCI6MTc2MTM4MTQ2Mi45NTl9.zIFuEr1-gUghwtaGf54IUPcacLT6A-LEBjt2Jd-b2y8"
USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"

print("="*70)
print("🔬 详细测试即刻 API")
print("="*70)
print()

# 测试多种可能的配置
test_configs = [
    {
        "name": "GraphQL - 完整 headers",
        "url": "https://web-api.okjike.com/api/graphql",
        "method": "POST",
        "headers": {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json',
            'Origin': 'https://web.okjike.com',
            'Referer': 'https://web.okjike.com/',
            'x-jike-access-token': TOKEN,
        },
        "json_data": {
            "operationName": "UserFeeds",
            "query": """query UserFeeds($username: String!) {
                userProfile(username: $username) {
                    username
                    screenName
                    briefIntro
                }
            }""",
            "variables": {"username": USER_ID}
        }
    },
    {
        "name": "GraphQL - 获取动态列表",
        "url": "https://web-api.okjike.com/api/graphql",
        "method": "POST",
        "headers": {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'x-jike-access-token': TOKEN,
        },
        "json_data": {
            "operationName": "UserFeeds",
            "query": """query UserFeeds($username: String!, $loadMoreKey: JSON) {
                userProfile(username: $username) {
                    username
                    feeds(loadMoreKey: $loadMoreKey, limit: 10) {
                        nodes {
                            ... on OriginalPost {
                                id
                                content
                                createdAt
                            }
                        }
                    }
                }
            }""",
            "variables": {"username": USER_ID, "loadMoreKey": None}
        }
    },
    {
        "name": "REST API - ruguoapp",
        "url": f"https://api.ruguoapp.com/1.0/users/{USER_ID}/posts",
        "method": "GET",
        "headers": {
            'User-Agent': 'Jike/5.0.0 (com.ruguoapp.jike; build:5.0.0; iOS 15.0.0) Alamofire/5.0.0',
            'Accept': 'application/json',
            'x-jike-access-token': TOKEN,
            'App-Version': '5.0.0',
            'platform': 'ios',
        },
        "params": {"limit": 10}
    },
]

success = False

for i, config in enumerate(test_configs, 1):
    print(f"\n[{i}/{len(test_configs)}] 测试: {config['name']}")
    print(f"URL: {config['url']}")
    print("-" * 70)

    try:
        if config['method'] == 'POST':
            resp = requests.post(
                config['url'],
                headers=config['headers'],
                json=config.get('json_data'),
                timeout=15
            )
        else:
            resp = requests.get(
                config['url'],
                headers=config['headers'],
                params=config.get('params'),
                timeout=15
            )

        print(f"状态码: {resp.status_code}")

        if resp.status_code == 200:
            print("✅ 请求成功！")
            try:
                data = resp.json()
                print("\n📦 响应数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:800])

                # 检查是否有数据
                if data and not data.get('errors'):
                    print("\n🎉 找到可用的 API！")
                    success = True

                    # 保存成功的配置
                    with open('成功的API配置.json', 'w', encoding='utf-8') as f:
                        json.dump({
                            'config': config,
                            'response_sample': str(data)[:500]
                        }, f, indent=2, ensure_ascii=False)

                    print("✓ 配置已保存到: 成功的API配置.json")
                    break
                else:
                    print("⚠️  有错误:", data.get('errors'))

            except Exception as e:
                print(f"⚠️  JSON 解析失败: {e}")
                print("原始响应:", resp.text[:500])
        else:
            print(f"❌ 失败")
            print("响应:", resp.text[:400])

    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)

if success:
    print("✅ 测试完成 - 找到可用方案！")
    print("\n下一步: 我将基于此创建自动同步脚本")
else:
    print("❌ 所有方法都失败了")
    print("\n可能的原因:")
    print("1. Token 格式正确但权限不足")
    print("2. 需要额外的 Cookie 或 Refresh Token")
    print("3. 即刻 API 需要特殊的签名算法")
    print("\n建议方案: 使用浏览器自动化（Puppeteer/Playwright）")

print("="*70)
