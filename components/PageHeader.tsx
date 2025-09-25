import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

// 类型定义
interface MetaField {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  className?: string;
}

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  metaFields?: MetaField[];
  publishedAt?: string | Date;
  author?: string;
  readingTime?: number;
  category?: string;
  tags?: string[];
  className?: string;
  showSkeleton?: boolean;
  enableJsonLd?: boolean;
  jsonLdData?: Record<string, any>;
}

// 暗色模式 Hook
const useDarkMode = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const checkDarkMode = () => {
      const isDarkMode = 
        localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      setIsDark(isDarkMode);
    };

    checkDarkMode();
    window.addEventListener('storage', checkDarkMode);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', checkDarkMode);

    return () => {
      window.removeEventListener('storage', checkDarkMode);
      window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', checkDarkMode);
    };
  }, []);

  return isDark;
};

// 阅读时长计算
const calculateReadingTime = (content: string): number => {
  const wordsPerMinute = 200; // 中文阅读速度
  const wordCount = content.length;
  return Math.ceil(wordCount / wordsPerMinute);
};

// 默认图标组件
const DefaultIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
  </svg>
);

// Skeleton 组件
const Skeleton: React.FC<{ className?: string }> = ({ className = "" }) => (
  <div className={`animate-pulse bg-gray-300 dark:bg-gray-600 rounded ${className}`} />
);

// 主组件
const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  metaFields = [],
  publishedAt,
  author,
  readingTime,
  category,
  tags = [],
  className = "",
  showSkeleton = false,
  enableJsonLd = true,
  jsonLdData = {}
}) => {
  const isDark = useDarkMode();
  const [isLoading, setIsLoading] = useState(showSkeleton);

  // 模拟加载状态
  useEffect(() => {
    if (showSkeleton) {
      const timer = setTimeout(() => setIsLoading(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [showSkeleton]);

  // 构建元信息数组
  const allMetaFields: MetaField[] = [
    ...metaFields,
    ...(publishedAt ? [{
      label: '发布时间',
      value: format(new Date(publishedAt), 'yyyy年MM月dd日', { locale: zhCN }),
      icon: <DefaultIcon />
    }] : []),
    ...(author ? [{
      label: '作者',
      value: author,
      icon: <DefaultIcon />
    }] : []),
    ...(readingTime ? [{
      label: '阅读时长',
      value: `${readingTime} 分钟`,
      icon: <DefaultIcon />
    }] : []),
    ...(category ? [{
      label: '分类',
      value: category,
      icon: <DefaultIcon />
    }] : [])
  ];

  // 生成 JSON-LD 结构化数据
  const generateJsonLd = () => {
    if (!enableJsonLd) return null;

    const baseData = {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": title,
      ...(subtitle && { "alternativeHeadline": subtitle }),
      ...(author && { "author": { "@type": "Person", "name": author } }),
      ...(publishedAt && { "datePublished": new Date(publishedAt).toISOString() }),
      ...(category && { "articleSection": category }),
      ...(tags.length > 0 && { "keywords": tags.join(", ") }),
      ...jsonLdData
    };

    return (
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(baseData) }}
      />
    );
  };

  // 样式类名
  const containerClasses = `
    max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12
    ${isDark ? 'text-white' : 'text-gray-900'}
    ${className}
  `.trim();

  const titleClasses = `
    text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight
    ${isDark ? 'text-white' : 'text-gray-900'}
    mb-4 sm:mb-6
  `.trim();

  const subtitleClasses = `
    text-lg sm:text-xl lg:text-2xl
    ${isDark ? 'text-gray-300' : 'text-gray-600'}
    mb-6 sm:mb-8
  `.trim();

  const metaContainerClasses = `
    flex flex-wrap items-center gap-4 sm:gap-6
    ${isDark ? 'text-gray-400' : 'text-gray-500'}
    text-sm sm:text-base
    mb-6 sm:mb-8
  `.trim();

  const tagContainerClasses = `
    flex flex-wrap gap-2 sm:gap-3
    mb-6 sm:mb-8
  `.trim();

  const tagClasses = `
    px-3 py-1 rounded-full text-xs sm:text-sm font-medium
    ${isDark 
      ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' 
      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
    }
    transition-colors duration-200
  `.trim();

  if (isLoading) {
    return (
      <header className={containerClasses}>
        <Skeleton className="h-12 w-3/4 mb-4" />
        <Skeleton className="h-6 w-1/2 mb-6" />
        <div className="flex flex-wrap gap-4 mb-6">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-16" />
        </div>
        <div className="flex flex-wrap gap-2">
          <Skeleton className="h-6 w-16 rounded-full" />
          <Skeleton className="h-6 w-20 rounded-full" />
        </div>
      </header>
    );
  }

  return (
    <>
      {generateJsonLd()}
      <header className={containerClasses}>
        {/* 标题 */}
        <h1 className={titleClasses}>
          {title}
        </h1>

        {/* 副标题 */}
        {subtitle && (
          <h2 className={subtitleClasses}>
            {subtitle}
          </h2>
        )}

        {/* 元信息区域 */}
        {allMetaFields.length > 0 && (
          <div className={metaContainerClasses}>
            {allMetaFields.map((field, index) => (
              <div key={index} className="flex items-center gap-2">
                {field.icon && (
                  <span className="flex-shrink-0">
                    {field.icon}
                  </span>
                )}
                <span className="font-medium">{field.label}:</span>
                <span className={field.className || ''}>{field.value}</span>
              </div>
            ))}
          </div>
        )}

        {/* 标签区域 */}
        {tags.length > 0 && (
          <div className={tagContainerClasses}>
            {tags.map((tag, index) => (
              <span key={index} className={tagClasses}>
                {tag}
              </span>
            ))}
          </div>
        )}
      </header>
    </>
  );
};

export default PageHeader;

