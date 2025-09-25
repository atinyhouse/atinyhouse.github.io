import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import styles from './PageHeader.module.css';

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
  theme?: 'light' | 'dark' | 'auto';
}

// 暗色模式 Hook
const useDarkMode = (theme: 'light' | 'dark' | 'auto' = 'auto') => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (theme === 'light') {
      setIsDark(false);
      return;
    }
    if (theme === 'dark') {
      setIsDark(true);
      return;
    }

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
  }, [theme]);

  return isDark;
};

// 默认图标组件
const DefaultIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
  </svg>
);

// Skeleton 组件
const Skeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={`${styles.skeleton} ${className || ''}`} />
);

// 主组件
const PageHeaderCSSModules: React.FC<PageHeaderProps> = ({
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
  jsonLdData = {},
  theme = 'auto'
}) => {
  const isDark = useDarkMode(theme);
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
      icon: <DefaultIcon className={styles.metaIcon} />
    }] : []),
    ...(author ? [{
      label: '作者',
      value: author,
      icon: <DefaultIcon className={styles.metaIcon} />
    }] : []),
    ...(readingTime ? [{
      label: '阅读时长',
      value: `${readingTime} 分钟`,
      icon: <DefaultIcon className={styles.metaIcon} />
    }] : []),
    ...(category ? [{
      label: '分类',
      value: category,
      icon: <DefaultIcon className={styles.metaIcon} />
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

  // 动态类名
  const containerClasses = [
    styles.container,
    isDark ? 'dark' : 'light',
    className
  ].filter(Boolean).join(' ');

  const titleClasses = [
    styles.title,
    isDark ? styles.dark : styles.light
  ].filter(Boolean).join(' ');

  const subtitleClasses = [
    styles.subtitle,
    isDark ? styles.dark : styles.light
  ].filter(Boolean).join(' ');

  const metaContainerClasses = [
    styles.metaContainer,
    isDark ? styles.dark : styles.light
  ].filter(Boolean).join(' ');

  const tagContainerClasses = styles.tagContainer;

  const tagClasses = [
    styles.tag,
    isDark ? styles.dark : styles.light
  ].filter(Boolean).join(' ');

  if (isLoading) {
    return (
      <header className={containerClasses}>
        <Skeleton className={styles.skeletonTitle} />
        <Skeleton className={styles.skeletonSubtitle} />
        <div className={styles.metaContainer}>
          <Skeleton className={styles.skeletonMeta} />
          <Skeleton className={styles.skeletonMeta} />
          <Skeleton className={styles.skeletonMeta} />
        </div>
        <div className={styles.tagContainer}>
          <Skeleton className={styles.skeletonTag} />
          <Skeleton className={styles.skeletonTag} />
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
              <div key={index} className={styles.metaItem}>
                {field.icon && (
                  <span className={styles.metaIcon}>
                    {field.icon}
                  </span>
                )}
                <span className={styles.metaLabel}>{field.label}:</span>
                <span className={field.className || styles.metaValue}>{field.value}</span>
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

export default PageHeaderCSSModules;



