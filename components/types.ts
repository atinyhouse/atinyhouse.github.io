// PageHeader 组件类型定义

export interface MetaField {
  /** 字段标签 */
  label: string;
  /** 字段值 */
  value: string | number;
  /** 可选图标 */
  icon?: React.ReactNode;
  /** 自定义样式类名 */
  className?: string;
}

export interface PageHeaderProps {
  /** 页面标题（必需） */
  title: string;
  /** 副标题 */
  subtitle?: string;
  /** 自定义元信息字段 */
  metaFields?: MetaField[];
  /** 发布日期 */
  publishedAt?: string | Date;
  /** 作者 */
  author?: string;
  /** 阅读时长（分钟） */
  readingTime?: number;
  /** 分类 */
  category?: string;
  /** 标签数组 */
  tags?: string[];
  /** 自定义样式类名 */
  className?: string;
  /** 是否显示加载状态 */
  showSkeleton?: boolean;
  /** 是否启用 JSON-LD */
  enableJsonLd?: boolean;
  /** 自定义 JSON-LD 数据 */
  jsonLdData?: Record<string, any>;
  /** 主题模式（仅 CSS Modules 版本） */
  theme?: 'light' | 'dark' | 'auto';
}

export interface JsonLdData {
  '@context': string;
  '@type': string;
  headline: string;
  alternativeHeadline?: string;
  author?: {
    '@type': string;
    name: string;
  };
  datePublished?: string;
  articleSection?: string;
  keywords?: string;
  [key: string]: any;
}

// 工具类型
export type ThemeMode = 'light' | 'dark' | 'auto';

export type SkeletonVariant = 'title' | 'subtitle' | 'meta' | 'tag';

// 响应式断点
export interface Breakpoints {
  sm: number;
  md: number;
  lg: number;
  xl: number;
}

export const defaultBreakpoints: Breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
};

// 样式配置
export interface StyleConfig {
  /** 是否启用动画 */
  enableAnimations?: boolean;
  /** 动画持续时间（毫秒） */
  animationDuration?: number;
  /** 是否启用悬停效果 */
  enableHover?: boolean;
  /** 自定义颜色主题 */
  colors?: {
    primary?: string;
    secondary?: string;
    accent?: string;
    text?: string;
    background?: string;
  };
}

export const defaultStyleConfig: StyleConfig = {
  enableAnimations: true,
  animationDuration: 200,
  enableHover: true,
  colors: {
    primary: '#3b82f6',
    secondary: '#6b7280',
    accent: '#f59e0b',
    text: '#111827',
    background: '#ffffff',
  },
};

// 事件处理器类型
export interface PageHeaderEvents {
  onTitleClick?: (title: string) => void;
  onTagClick?: (tag: string, index: number) => void;
  onMetaFieldClick?: (field: MetaField, index: number) => void;
}

// 扩展的 PageHeader Props（包含事件处理器）
export interface PageHeaderPropsWithEvents extends PageHeaderProps, PageHeaderEvents {}

// 工具函数类型
export type CalculateReadingTime = (content: string, wordsPerMinute?: number) => number;

export type FormatDate = (date: string | Date, format?: string) => string;

export type GenerateJsonLd = (props: PageHeaderProps) => JsonLdData | null;

// 默认配置
export const defaultProps: Partial<PageHeaderProps> = {
  metaFields: [],
  tags: [],
  className: '',
  showSkeleton: false,
  enableJsonLd: true,
  jsonLdData: {},
  theme: 'auto',
};

// 验证函数类型
export type ValidateProps = (props: PageHeaderProps) => string[];

// 错误类型
export interface PageHeaderError {
  field: keyof PageHeaderProps;
  message: string;
  code: string;
}

// 组件状态
export interface PageHeaderState {
  isLoading: boolean;
  isDark: boolean;
  errors: PageHeaderError[];
}

// 钩子返回类型
export interface UsePageHeaderReturn {
  state: PageHeaderState;
  actions: {
    setLoading: (loading: boolean) => void;
    setTheme: (theme: ThemeMode) => void;
    addError: (error: PageHeaderError) => void;
    clearErrors: () => void;
  };
}

// 样式类名生成器类型
export type ClassNameGenerator = (
  baseClass: string,
  modifiers?: Record<string, boolean>,
  customClass?: string
) => string;

// 主题切换器类型
export interface ThemeToggle {
  current: ThemeMode;
  toggle: () => void;
  setTheme: (theme: ThemeMode) => void;
}

// 响应式配置
export interface ResponsiveConfig {
  breakpoints: Breakpoints;
  containerMaxWidth: Record<keyof Breakpoints, string>;
  fontSize: Record<keyof Breakpoints, Record<string, string>>;
  spacing: Record<keyof Breakpoints, Record<string, string>>;
}

export const defaultResponsiveConfig: ResponsiveConfig = {
  breakpoints: defaultBreakpoints,
  containerMaxWidth: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
  fontSize: {
    sm: {
      title: '1.875rem',
      subtitle: '1.125rem',
      meta: '0.875rem',
      tag: '0.75rem',
    },
    md: {
      title: '2.25rem',
      subtitle: '1.25rem',
      meta: '1rem',
      tag: '0.875rem',
    },
    lg: {
      title: '3rem',
      subtitle: '1.5rem',
      meta: '1rem',
      tag: '0.875rem',
    },
    xl: {
      title: '3rem',
      subtitle: '1.5rem',
      meta: '1rem',
      tag: '0.875rem',
    },
  },
  spacing: {
    sm: {
      container: '2rem 1rem',
      title: '1rem',
      subtitle: '1.5rem',
      meta: '1.5rem',
      tag: '1.5rem',
    },
    md: {
      container: '3rem 1.5rem',
      title: '1.5rem',
      subtitle: '2rem',
      meta: '2rem',
      tag: '2rem',
    },
    lg: {
      container: '3rem 2rem',
      title: '1.5rem',
      subtitle: '2rem',
      meta: '2rem',
      tag: '2rem',
    },
    xl: {
      container: '3rem 2rem',
      title: '1.5rem',
      subtitle: '2rem',
      meta: '2rem',
      tag: '2rem',
    },
  },
};

