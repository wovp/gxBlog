// 文章分类对象
export interface Category {
  id?: number // 添加id字段，与后端保持一致
  categoryId: string
  name: string
  slug: string
  description?: string
  createTime: string
}

// 文章列表项对象
export interface ArticleListItem {
  articleId: string
  title: string
  author: string
  createTime: string
  preview: string
}

// 文章详情对象
export interface ArticleDetail {
  articleId: string
  title: string
  author: string
  createTime: string
  updateTime?: string
  category: {
    categoryId: string
    name: string
  }
  markdownContent: string
  htmlContent: string
  content?: string // 添加content字段，与后端保持一致
}

// 分页信息
export interface Pagination {
  total: number
  pageSize: number
  currentPage: number
  totalPages: number
}

// API响应格式
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 文章列表响应
export interface ArticleListResponse {
  list: ArticleListItem[]
  pagination: Pagination
}