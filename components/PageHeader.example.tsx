import React from 'react';
import PageHeader from './PageHeader';

// 使用示例
const PageHeaderExample: React.FC = () => {
  // 示例数据
  const sampleData = {
    title: "深入理解 React Hooks 的设计原理与最佳实践",
    subtitle: "从函数组件的状态管理到性能优化，全面解析现代 React 开发",
    publishedAt: "2024-01-15",
    author: "张三",
    readingTime: 12,
    category: "前端开发",
    tags: ["React", "Hooks", "JavaScript", "前端", "教程"],
    metaFields: [
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
    ]
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      {/* 基础用法 */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          基础用法
        </h2>
        <PageHeader
          title="简单标题"
          publishedAt="2024-01-15"
          author="作者名"
        />
      </section>

      {/* 完整功能 */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          完整功能
        </h2>
        <PageHeader
          {...sampleData}
          enableJsonLd={true}
        />
      </section>

      {/* 加载状态 */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          加载状态
        </h2>
        <PageHeader
          title=""
          showSkeleton={true}
        />
      </section>

      {/* 长标题测试 */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          长标题测试
        </h2>
        <PageHeader
          title="这是一个非常长的标题，用来测试组件在长文本情况下的换行和布局表现，确保在不同屏幕尺寸下都能正常显示"
          subtitle="副标题也可以很长，用来测试响应式设计和文本换行效果"
          publishedAt="2024-01-15"
          author="测试作者"
          readingTime={15}
          tags={["长标题", "测试", "响应式", "换行", "布局"]}
        />
      </section>

      {/* 自定义元信息 */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
          自定义元信息
        </h2>
        <PageHeader
          title="自定义元信息示例"
          metaFields={[
            {
              label: "版本",
              value: "v2.1.0",
              icon: <span>📦</span>
            },
            {
              label: "状态",
              value: "已完成",
              icon: <span>✅</span>,
              className: "text-green-500"
            },
            {
              label: "优先级",
              value: "高",
              icon: <span>🔥</span>,
              className: "text-red-500"
            }
          ]}
        />
      </section>
    </div>
  );
};

export default PageHeaderExample;

