#!/bin/bash
# 快速测试即刻同步

cd "$(dirname "$0")"

echo "🔍 测试即刻 API 连接..."
echo ""

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoicnVMZk40Vkk1K28xb2hvbzNIbzZSVGpDTlNcL1FYZ3JLQm16NUd4MVA4MWs4d0s0djFDUDB2NU02ZGgyTFd4dE8zMVhiejErMmxWbTV1c2F2aGQ3ODcyTExhQUZsXC9ZaFwvbG1zdGQxMkwzaE5pMHhtaWlFcDhXUjlySFJOTVJJbVZKMnV2MmVXaHFEb0wzcDBTV2VUOThscmhqdEI1aWFLVmVoeHZDYjZKM3VWWjM4Tmo5ME1BSVU4K0dxczY4OXhGMWNvckorQkJCRHNPUUVPeHhtUWMwNmVQYlJJbXVXenR2QUtHSmVcL2U0OVV5T0M1TEp6aTl1ZXZvdldGMVVyOXJTQVJXN1hsbDlvamdwVDVJbWVRZjkwTE1aWlAwQmN5bHltY2wyUTdYWlowdENHVW91U0tSdlwvV1IzdkswdUFwQzE5UU9cL1JXUzg4dlM3S0I3NUx4NGV5M2ZieDVDNDRiOVwvTWs3Z25tOUNPND0iLCJ2IjozLCJpdiI6InVmdUZsNDBzNGVZUldoNUZJc1dVdnc9PSIsImlhdCI6MTc2MTM4MTQ2Mi45NTl9.zIFuEr1-gUghwtaGf54IUPcacLT6A-LEBjt2Jd-b2y8"

# 测试 GraphQL API
curl -s -X POST https://web-api.okjike.com/api/graphql \
  -H "Content-Type: application/json" \
  -H "x-jike-access-token: $TOKEN" \
  -d '{"operationName":"GetUserProfile","query":"query GetUserProfile($username: String!) { userProfile(username: $username) { username screenName } }","variables":{"username":"71A6B3C3-1382-4121-A17A-2A4C05CB55E8"}}' \
  | python3 -m json.tool 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ API 连接成功！"
    echo "💡 您的 Token 是有效的"
else
    echo ""
    echo "❌ API 连接失败"
    echo "建议使用方案 A：Jocker 扩展"
fi
