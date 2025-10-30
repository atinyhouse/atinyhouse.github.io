#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 thoughts 数据的格式问题：
1. 删除真正重复的内容（8月31）
2. 从源数据恢复10月16日的段落格式
"""

import yaml
import re
from datetime import datetime

print("="*60)
print("🔧 修复 Thoughts 数据格式")
print("="*60)
print()

# 读取当前数据
with open('_data/thoughts.yml', 'r', encoding='utf-8') as f:
    lines = []
    for line in f:
        if not line.strip().startswith('#'):
            lines.append(line)
    thoughts = yaml.safe_load(''.join(lines)) or []

print(f"当前数据: {len(thoughts)} 条")
print()

# 1. 删除8月31日的重复条目
print("🗑️  删除重复内容...")
thoughts_fixed = []
removed_count = 0

for t in thoughts:
    # 删除8月31日的条目（保留9月1日）
    if t.get('date') == '2025-08-31' and t.get('time') == '16:09':
        print(f"  ✗ 删除: {t.get('date')} {t.get('time')} (与9月1日重复)")
        removed_count += 1
        continue

    thoughts_fixed.append(t)

print(f"✓ 删除了 {removed_count} 条重复")
print()

# 2. 恢复10月16日的段落格式
print("📝 恢复10月16日的段落格式...")

# 原始内容（从即刻获取的正确格式）
oct16_formatted = """昨天晚上，睡前刷短视频的时候，看到一个视频是一张写满答案的数学考卷，有一句文案：

"少女时代的淤青，
产生于深夜的自我怀疑，
为什么不聪明。"

突然感觉有点被打动，眼眶湿润。可能是由于家里还有一个高中生的妹妹，我也感觉自己好像还没有走出高中生活的漩涡。

妹妹和我一样，选择了文科。在分科前，她度过了相当艰难的一段时间。是听不懂的物理课，跟不上节奏的数学课，是很多次拿到手的难以置信的分数。不知道哭了多少次、灰心丧气了多少次。

即使很多人说理科更好选专业、更好就业，即使大部分她的同学都选择理科，即使选了文科班会被打上没那么聪明的标签，她还是很坚决地选了文科。

进入文科班之后，她状态好了很多。不用再上物理课了，也有更多时间学习数学。

每天晚上大概十二点左右的时候，她都会给我发信息。主要是给我拍照片，晚自习结束后，她回到小小的房间里，又学习了什么。很认真、很踏实的妹妹。

我也通常会发一两句类似于"棒棒哒、辛苦了"之类的话鼓励她。高中的数学我当然已经几乎全部忘光，我所能帮助她的也只是给她鼓励和安慰而已。

只不过看到她每一天的深夜都发给我的题目照片，我下意识地就会浮现出，远在千里之外的此时此刻，在只有青春期才会亮起的台灯下面，她在低着头认真的思考、做题。

不知道她是否也会像这个俗套文案里说的，质疑自己是否不聪明。

我很想告诉她，我那个时候，也有很多题不会做，也很羡慕身边的同学能解除非常复杂的数学题，我也觉得自己没有那么聪明。我反复的在此后的人生用各种情形来验证自己是否足够聪明、足够够格。

可是我现在觉得好像是否聪明真的不重要，努力的过程很重要，遇到困难产生的信心和韧性很重要，对生活的轻松愉快的心情很重要。

少女时代的淤青只是成长的一个注脚，淤青总有一天会消失的，和少女时代一起。"""

# 替换10月16日的内容
for t in thoughts_fixed:
    if t.get('date') == '2025-10-16' and t.get('time') == '04:20':
        old_len = len(t.get('content', ''))
        t['content'] = oct16_formatted
        new_len = len(t['content'])
        print(f"  ✓ 更新: {t.get('date')} {t.get('time')}")
        print(f"    原长度: {old_len} -> 新长度: {new_len}")
        print(f"    段落数: {t['content'].count(chr(10) + chr(10)) + 1}")

print()

# 3. 保存
print("💾 保存修复后的数据...")

thoughts_fixed.sort(
    key=lambda x: (x.get('date', '0000-00-00'), x.get('time', '00:00')),
    reverse=True
)

header = f"""# ============================================
# Thoughts 数据文件 - 即刻动态
# ============================================
#
# 已修复：删除重复、恢复段落格式
# 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ============================================

"""

with open('_data/thoughts.yml', 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(
        thoughts_fixed,
        f,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=float('inf')
    )

print("✓ 保存完成")
print()

print("="*60)
print("✅ 修复完成！")
print("="*60)
print()
print(f"📊 统计:")
print(f"  - 原始数据: {len(thoughts)} 条")
print(f"  - 删除重复: {removed_count} 条")
print(f"  - 最终数据: {len(thoughts_fixed)} 条")
print()
