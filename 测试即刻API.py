#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即刻 API 测试脚本 - 诊断问题
"""

import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoicnVMZk40Vkk1K28xb2hvbzNIbzZSVGpDTlNcL1FYZ3JLQm16NUd4MVA4MWs4d0s0djFDUDB2NU02ZGgyTFd4dE8zMVhiejErMmxWbTV1c2F2aGQ3ODcyTExhQUZsXC9ZaFwvbG1zdGQxMkwzaE5pMHhtaWlFcDhXUjlySFJOTVJJbVZKMnV2MmVXaHFEb0wzcDBTV2VUOThscmhqdEI1aWFLVmVoeHZDYjZKM3VWWjM4Tmo5ME1BSVU4K0dxczY4OXhGMWNvckorQkJCRHNPUUVPeHhtUWMwNmVQYlJJbXVXenR2QUtHSmVcL2U0OVV5T0M1TEp6aTl1ZXZvdldGMVVyOXJTQVJXN1hsbDlvamdwVDVJbWVRZjkwTE1aWlAwQmN5bHltY2wyUTdYWlowdENHVW91U0tSdlwvV1IzdkswdUFwQzE5UU9cL1JXUzg4dlM3S0I3NUx4NGV5M2ZieDVDNDRiOVwvTWs3Z25tOUNPND0iLCJ2IjozLCJpdiI6InVmdUZsNDBzNGVZUldoNUZJc1dVdnc9PSIsImlhdCI6MTc2MTM4MTQ2Mi45NTl9.zIFuEr1-gUghwtaGf54IUPcacLT6A-LEBjt2Jd-b2y8"
USER_ID = "71A6B3C3-1382-4121-A17A-2A4C05CB55E8"

print("="*60)
print("🔍 即刻 API 诊断测试")
print("="*60)
print()
print(f"Token: {TOKEN[:20]}...{TOKEN[-20:]}")
print(f"用户ID: {USER_ID}")
print()

# 测试不同的 API 端点
endpoints_to_test = [
    {
        "name": "GraphQL API",
        "url": "https://web-api.okjike.com/api/graphql",
        "method": "POST",
        "headers": {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-jike-access-token': TOKEN,
        },
        "data": {
            "operationName": "GetUserProfile",
            "query": """query GetUserProfile($username: String!) {
              userProfile(username: $username) {
                username
                screenName
              }
            }""",
            "variables": {"username": USER_ID}
        }
    },
    {
        "name": "REST API v1",
        "url": f"https://api.ruguoapp.com/1.0/users/{USER_ID}/posts",
        "method": "GET",
        "headers": {
            'User-Agent': 'Mozilla/5.0',
            'x-jike-access-token': TOKEN,
        },
        "params": {"limit": 5}
    }
]

success = False

for i, endpoint in enumerate(endpoints_to_test, 1):
    print(f"\n[{i}/{len(endpoints_to_test)}] 测试：{endpoint['name']}")
    print(f"URL: {endpoint['url']}")
    print("-" * 60)

    try:
        if endpoint['method'] == 'POST':
            response = requests.post(
                endpoint['url'],
                headers=endpoint['headers'],
                json=endpoint.get('data'),
                timeout=10
            )
        else:
            response = requests.get(
                endpoint['url'],
                headers=endpoint['headers'],
                params=endpoint.get('params'),
                timeout=10
            )

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            print("✅ 请求成功！")
            try:
                data = response.json()
                print("\n响应数据预览:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                print("...")
                print("\n🎉 找到可用的 API 端点！")
                success = True
                break
            except Exception as e:
                print(f"⚠️  JSON 解析失败: {e}")
                print(response.text[:200])
        else:
            print(f"❌ 请求失败")
            print("错误信息:")
            print(response.text[:300])

    except Exception as e:
        print(f"❌ 请求异常: {e}")

if not success:
    print("\n" + "="*60)
    print("❌ 所有 API 端点都失败了")
    print("="*60)
    print("\n可能的原因：")
    print("1. Token 无效或已过期")
    print("2. 即刻 API 已更改")
    print("3. 需要额外的认证参数")
else:
    print("\n" + "="*60)
    print("✅ 诊断完成 - 找到可用的 API")
    print("="*60)
