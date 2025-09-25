# PageHeader 组件

一个功能完整的页面标题组件，支持元信息显示、暗色模式、响应式设计和 SEO 优化。

## 功能特性

- ✅ **标题显示**：支持长标题自动换行
- ✅ **元信息区域**：日期、作者、阅读时长等，支持扩展字段
- ✅ **响应式设计**：移动端和桌面端完美适配
- ✅ **暗色模式**：自动检测系统主题或手动设置
- ✅ **加载状态**：Skeleton 加载动画
- ✅ **SEO 优化**：JSON-LD 结构化数据支持
- ✅ **类型安全**：完整的 TypeScript 类型定义

## 安装依赖

```bash
npm install date-fns
npm install @types/react @types/react-dom
```

## 使用方法

### 基础用法

```tsx
import PageHeader from './components/PageHeader';

function App() {
  return (
    <PageHeader
      title="文章标题"
      publishedAt="2024-01-15"
      author="作者名"
    />
  );
}
```

### 完整功能

```tsx
import PageHeader from './components/PageHeader';

function App() {
  return (
    <PageHeader
      title="深入理解 React Hooks"
      subtitle="从基础到高级的完整指南"
      publishedAt="2024-01-15"
      author="张三"
      readingTime={12}
      category="前端开发"
      tags={["React", "Hooks", "JavaScript"]}
      metaFields={[
        {
          label: "更新时间",
          value: "2024-01-20",
          icon: <span>🔄</span>
        },
        {
          label: "难度",
          value: "中级",
          icon: <span>⭐</span>,
          className: "text-orange-500"
        }
      ]}
      enableJsonLd={true}
    />
  );
}
```

### 加载状态

```tsx
<PageHeader
  title=""
  showSkeleton={true}
/>
```

## API 参考

### Props

| 属性 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `title` | `string` | - | 页面标题（必需） |
| `subtitle` | `string` | - | 副标题 |
| `metaFields` | `MetaField[]` | `[]` | 自定义元信息字段 |
| `publishedAt` | `string \| Date` | - | 发布日期 |
| `author` | `string` | - | 作者 |
| `readingTime` | `number` | - | 阅读时长（分钟） |
| `category` | `string` | - | 分类 |
| `tags` | `string[]` | `[]` | 标签数组 |
| `className` | `string` | `""` | 自定义样式类名 |
| `showSkeleton` | `boolean` | `false` | 是否显示加载状态 |
| `enableJsonLd` | `boolean` | `true` | 是否启用 JSON-LD |
| `jsonLdData` | `Record<string, any>` | `{}` | 自定义 JSON-LD 数据 |

### MetaField 类型

```tsx
interface MetaField {
  label: string;        // 字段标签
  value: string | number; // 字段值
  icon?: React.ReactNode; // 可选图标
  className?: string;    // 自定义样式类名
}
```

## 样式定制

### 使用 Tailwind CSS

组件使用 Tailwind CSS 类名，可以通过 `className` 属性进行定制：

```tsx
<PageHeader
  title="自定义样式标题"
  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white"
/>
```

### 使用 CSS Modules

如果项目不支持 Tailwind CSS，可以使用 CSS Modules 版本：

```tsx
import PageHeaderCSSModules from './components/PageHeaderCSSModules';

<PageHeaderCSSModules
  title="使用 CSS Modules 的标题"
  theme="dark" // 强制暗色模式
/>
```

## 暗色模式

组件会自动检测系统主题偏好，也可以通过 `theme` 属性手动设置：

```tsx
// 自动检测（默认）
<PageHeader title="自动主题" />

// 强制亮色模式
<PageHeaderCSSModules title="亮色模式" theme="light" />

// 强制暗色模式
<PageHeaderCSSModules title="暗色模式" theme="dark" />
```

## SEO 优化

组件支持 JSON-LD 结构化数据，有助于搜索引擎理解页面内容：

```tsx
<PageHeader
  title="SEO 优化文章"
  publishedAt="2024-01-15"
  author="作者名"
  enableJsonLd={true}
  jsonLdData={{
    "publisher": {
      "@type": "Organization",
      "name": "我的网站"
    }
  }}
/>
```

## 响应式设计

组件在不同屏幕尺寸下会自动调整：

- **移动端**：紧凑布局，较小的字体
- **平板端**：中等间距和字体大小
- **桌面端**：宽松布局，较大的字体

## 自定义图标

可以为元信息字段添加自定义图标：

```tsx
const CustomIcon = () => (
  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

<PageHeader
  title="自定义图标示例"
  metaFields={[
    {
      label: "状态",
      value: "已完成",
      icon: <CustomIcon />
    }
  ]}
/>
```

## 注意事项

1. **长标题**：组件会自动处理长标题的换行，建议标题长度控制在合理范围内
2. **性能**：大量标签可能影响渲染性能，建议控制标签数量
3. **无障碍**：组件已考虑无障碍访问，但建议在使用时添加适当的 ARIA 标签
4. **浏览器兼容**：需要支持 ES6+ 的现代浏览器

## 示例项目

查看 `PageHeader.example.tsx` 文件获取更多使用示例。

