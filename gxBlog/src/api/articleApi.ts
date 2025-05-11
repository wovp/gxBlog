import { debugLog, debugError, debugTimeStart, debugTimeEnd } from '../utils/debug'
import request from '../utils/request'

// 文章API服务
const articleApi = {
  /**
   * 获取文章分类
   * @returns 分类列表
   */
  getCategories() {
    debugLog('调用API: 获取文章分类列表')
    debugTimeStart('API-getCategories')

    return request.get('/api/category')
      .then(response => {
        debugLog('API响应: 获取文章分类列表', response.data)
        debugTimeEnd('API-getCategories')
        return response
      })
      .catch(error => {
        debugError('API错误: 获取文章分类列表', error)
        debugTimeEnd('API-getCategories')
        throw error
      })
  },

  /**
   * 获取文章列表
   * @param params 查询参数
   * @returns 文章列表及分页信息
   */
  getArticleList(params: {
    categoryId?: string
    pageSize?: number
    currentPage?: number
    sortBy?: string
  }) {
    debugLog('调用API: 获取文章列表', params)
    debugTimeStart('API-getArticleList')

    return request.post('/api/article/list', params)
      .then(response => {
        debugLog('API响应: 获取文章列表', {
          code: response.data.code,
          message: response.data.message,
          listLength: response.data.data?.list?.length || 0,
          pagination: response.data.data?.pagination
        })
        debugTimeEnd('API-getArticleList')
        return response
      })
      .catch(error => {
        debugError('API错误: 获取文章列表', error)
        debugTimeEnd('API-getArticleList')
        throw error
      })
  },

  /**
   * 获取文章详情
   * @param articleId 文章ID
   * @returns 文章详情
   */
  getArticleDetail(articleId: string) {
    debugLog('调用API: 获取文章详情', { articleId })
    debugTimeStart('API-getArticleDetail')

    return request.get(`/api/article/${articleId}`)
      .then(response => {
        debugLog('API响应: 获取文章详情', {
          code: response.data.code,
          message: response.data.message,
          articleId: response.data.data?.articleId,
          title: response.data.data?.title
        })
        debugTimeEnd('API-getArticleDetail')
        return response
      })
      .catch(error => {
        debugError('API错误: 获取文章详情', error)
        debugTimeEnd('API-getArticleDetail')
        throw error
      })
  },

  /**
   * 搜索文章
   * @param params 搜索参数
   * @returns 搜索结果及分页信息
   */
  searchArticles(params: {
    keyword: string
    pageSize?: number
    currentPage?: number
  }) {
    debugLog('调用API: 搜索文章', params)
    debugTimeStart('API-searchArticles')

    return request.get('/api/article/search', { params })
      .then(response => {
        debugLog('API响应: 搜索文章', {
          code: response.data.code,
          message: response.data.message,
          listLength: response.data.data?.list?.length || 0,
          pagination: response.data.data?.pagination
        })
        debugTimeEnd('API-searchArticles')
        return response
      })
      .catch(error => {
        debugError('API错误: 搜索文章', error)
        debugTimeEnd('API-searchArticles')
        throw error
      })
  },

  /**
   * 获取同步状态
   * @returns 同步状态信息
   */
  getSyncStatus() {
    debugLog('调用API: 获取同步状态')
    debugTimeStart('API-getSyncStatus')

    return request.get('/api/sync/status')
      .then(response => {
        debugLog('API响应: 获取同步状态', response.data)
        debugTimeEnd('API-getSyncStatus')
        return response
      })
      .catch(error => {
        debugError('API错误: 获取同步状态', error)
        debugTimeEnd('API-getSyncStatus')
        throw error
      })
  },

  /**
   * 触发同步操作
   * @param params 同步参数
   * @returns 同步结果
   */
  triggerSync(params: {
    repo_url: string,
    target_dir: string
  }) {
    debugLog('调用API: 触发同步操作', params)
    debugTimeStart('API-triggerSync')

    return request.post('/api/sync', params)
      .then(response => {
        debugLog('API响应: 触发同步操作', response.data)
        debugTimeEnd('API-triggerSync')
        return response
      })
      .catch(error => {
        debugError('API错误: 触发同步操作', error)
        debugTimeEnd('API-triggerSync')
        throw error
      })
  }
}

export default articleApi