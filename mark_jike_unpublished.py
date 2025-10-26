#!/usr/bin/env python3
import os
import re

posts_dir = '_posts'

for filename in os.listdir(posts_dir):
    if not filename.endswith('.md'):
        continue

    filepath = os.path.join(posts_dir, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有 source: jike
    if 'source: jike' in content:
        # 检查是否已经有 published 字段
        if not re.search(r'^published:', content, re.MULTILINE):
            # 在 source: jike 后面添加 published: false
            content = re.sub(
                r'(source: jike\n)',
                r'\1published: false\n',
                content
            )

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f'Updated: {filename}')

print('Done!')
