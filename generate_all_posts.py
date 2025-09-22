#!/usr/bin/env python3
"""
为所有_posts中的文章生成HTML页面
"""
import os
import re
import yaml
from datetime import datetime
from pathlib import Path

def parse_front_matter(content):
    """解析Front Matter"""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    try:
        front_matter = yaml.safe_load(parts[1])
        content = parts[2].strip()
        return front_matter, content
    except:
        return {}, content

def markdown_to_html(content):
    """简单的Markdown到HTML转换"""
    # 处理标题
    content = re.sub(r'^### (.*)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.*)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    
    # 处理粗体
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'_(.*?)_', r'<em>\1</em>', content)
    
    # 处理引用
    content = re.sub(r'^> (.*)$', r'<blockquote><p>\1</p></blockquote>', content, flags=re.MULTILINE)
    
    # 处理段落
    paragraphs = content.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.startswith('#'):
            # 处理换行
            p = p.replace('\n', '<br>')
            html_paragraphs.append(f'<p>{p}</p>')
        else:
            html_paragraphs.append(p)
    
    return '\n\n'.join(html_paragraphs)

def generate_post_page(post_file, front_matter, content):
    """生成文章页面HTML"""
    title = front_matter.get('title', 'Untitled')
    author = front_matter.get('author', '小草庐')
    date = front_matter.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # 解析日期
    try:
        if isinstance(date, str):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        else:
            date_obj = date
        formatted_date = date_obj.strftime('%Y年%m月%d日')
    except:
        formatted_date = date
    
    # 转换Markdown内容
    html_content = markdown_to_html(content)
    
    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 小草庐 | A Tiny House</title>
  <meta name="description" content="{title}">

  <!-- CSS -->
  <link rel="stylesheet" href="../assets/main.css">
  <link rel="stylesheet" href="../assets/custom.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap">

  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png">

  <!-- Dark Mode Script -->
  <script>
    function toggleTheme() {{
      const body = document.body;
      const themeToggle = document.getElementById('themeToggle');
      
      if (body.getAttribute('data-theme') === 'dark') {{
        body.removeAttribute('data-theme');
        themeToggle.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      }} else {{
        body.setAttribute('data-theme', 'dark');
        themeToggle.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      }}
    }}

    document.addEventListener('DOMContentLoaded', function() {{
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark') {{
        document.body.setAttribute('data-theme', 'dark');
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {{
          themeToggle.setAttribute('data-theme', 'dark');
        }}
      }}
    }});
  </script>
</head>

<body>
  <nav class="nav">
    <div class="nav-container">
      <a href="../" class="nav-title">A Tiny House</a>
      <ul>
        <li><a href="../">Posts</a></li>
        <li><a href="../about">About</a></li>
        <li><a href="../tags">Tags</a></li>
      </ul>
      <button class="theme-toggle" onclick="toggleTheme()" id="themeToggle">
        <div class="theme-toggle-slider"></div>
      </button>
    </div>
  </nav>

  <main>
    <article class="post">
      <div class="post-info">
        <span>Written by</span>
        {author}
        <br>
        <span>on&nbsp;</span><time datetime="{date}">{formatted_date}</time>
      </div>

      <h1 class="post-title">{title}</h1>
      <div class="post-line"></div>

      <div class="post-content">
        {html_content}
      </div>
    </article>
  </main>

  <!-- 桌面端目录 -->
  <div class="table-of-contents" id="toc">
    <div class="table-of-contents-title">目录</div>
    <ul class="table-of-contents-list" id="toc-list">
      <!-- 目录内容将通过JavaScript生成 -->
    </ul>
  </div>

  <!-- 移动端目录按钮 -->
  <button class="toc-toggle" id="toc-toggle">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="3" y1="6" x2="21" y2="6"></line>
      <line x1="3" y1="12" x2="21" y2="12"></line>
      <line x1="3" y1="18" x2="21" y2="18"></line>
    </svg>
  </button>

  <!-- 移动端目录覆盖层 -->
  <div class="toc-overlay" id="toc-overlay"></div>

  <!-- 移动端目录 -->
  <div class="toc-mobile" id="toc-mobile">
    <button class="toc-close" id="toc-close">&times;</button>
    <div class="table-of-contents-title">目录</div>
    <ul class="table-of-contents-list" id="toc-mobile-list">
      <!-- 目录内容将通过JavaScript生成 -->
    </ul>
  </div>

  <div class="pagination">
    <a href="#" class="top">Top</a>
  </div>

  <footer>
    <span>
      &copy; <time datetime="2024">2024</time> 小草庐. Made with Jekyll using the <a href="https://github.com/chesterhow/tale/">Tale</a> theme.
    </span>
  </footer>

  <!-- 目录功能JavaScript -->
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      function generateTOC() {{
        const headings = document.querySelectorAll('.post-content h1, .post-content h2, .post-content h3, .post-content h4, .post-content h5, .post-content h6');
        const tocList = document.getElementById('toc-list');
        const tocMobileList = document.getElementById('toc-mobile-list');
        
        if (headings.length === 0) {{
          document.getElementById('toc').style.display = 'none';
          document.getElementById('toc-toggle').style.display = 'none';
          return;
        }}

        let tocHTML = '';
        let currentLevel = 0;
        
        headings.forEach((heading, index) => {{
          const level = parseInt(heading.tagName.charAt(1));
          const id = `heading-${{index}}`;
          heading.id = id;
          
          const text = heading.textContent.trim();
          const link = `<a href="#${{id}}" data-target="${{id}}">${{text}}</a>`;
          
          if (level > currentLevel) {{
            tocHTML += '<ul>';
            currentLevel = level;
          }} else if (level < currentLevel) {{
            for (let i = level; i < currentLevel; i++) {{
              tocHTML += '</ul>';
            }}
            currentLevel = level;
          }}
          
          tocHTML += `<li>${{link}}</li>`;
        }});
        
        for (let i = 0; i < currentLevel; i++) {{
          tocHTML += '</ul>';
        }}
        
        tocList.innerHTML = tocHTML;
        tocMobileList.innerHTML = tocHTML;
      }}

      function updateActiveState(targetId) {{
        document.querySelectorAll('.table-of-contents-list a').forEach(link => {{
          link.classList.remove('active');
          if (link.getAttribute('data-target') === targetId) {{
            link.classList.add('active');
          }}
        }});
      }}

      function highlightCurrentSection() {{
        const headings = document.querySelectorAll('.post-content h1, .post-content h2, .post-content h3, .post-content h4, .post-content h5, .post-content h6');
        
        function updateActiveLink() {{
          let current = '';
          
          headings.forEach(heading => {{
            const rect = heading.getBoundingClientRect();
            if (rect.top <= 100) {{
              current = heading.id;
            }}
          }});
          
          if (current) {{
            updateActiveState(current);
          }}
        }}
        
        window.addEventListener('scroll', updateActiveLink);
        updateActiveLink();
      }}

      function initMobileTOC() {{
        const toggle = document.getElementById('toc-toggle');
        const overlay = document.getElementById('toc-overlay');
        const mobile = document.getElementById('toc-mobile');
        const close = document.getElementById('toc-close');
        
        function openTOC() {{
          overlay.classList.add('active');
          mobile.classList.add('active');
          document.body.style.overflow = 'hidden';
        }}
        
        function closeTOC() {{
          overlay.classList.remove('active');
          mobile.classList.remove('active');
          document.body.style.overflow = '';
        }}
        
        toggle.addEventListener('click', openTOC);
        overlay.addEventListener('click', closeTOC);
        close.addEventListener('click', closeTOC);
        
        mobile.addEventListener('click', function(e) {{
          if (e.target.tagName === 'A') {{
            closeTOC();
          }}
        }});
      }}

      function initSmoothScroll() {{
        document.addEventListener('click', function(e) {{
          if (e.target.matches('.table-of-contents-list a')) {{
            e.preventDefault();
            const targetId = e.target.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {{
              updateActiveState(targetId);
              
              const offsetTop = targetElement.offsetTop - 80;
              window.scrollTo({{
                top: offsetTop,
                behavior: 'smooth'
              }});
            }}
          }}
        }});
      }}

      generateTOC();
      highlightCurrentSection();
      initMobileTOC();
      initSmoothScroll();
    }});
  </script>
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    posts_dir = Path('_posts')
    
    # 处理所有文章
    for post_file in posts_dir.glob('*.md'):
        print(f"处理文章: {post_file}")
        
        # 读取文件内容
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析Front Matter
        front_matter, content = parse_front_matter(content)
        
        # 生成HTML
        html = generate_post_page(post_file, front_matter, content)
        
        # 确定输出路径
        date_part = post_file.name[:10]  # YYYY-MM-DD
        title_part = post_file.name[11:-3]  # 去掉日期和.md
        safe_title = re.sub(r'[^\w\-]', '-', title_part.lower())
        
        # 创建目录结构
        year, month, day = date_part.split('-')
        output_dir = Path(year) / month / day
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f'{safe_title}.html'
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"生成页面: {output_path}")
    
    print("所有文章构建完成！")

if __name__ == '__main__':
    main()
