import axios from 'axios'

const api = {
  // 获取文章列表
  getArticles() {
    return axios.get('/api/articles')
  },
  // 获取文章详情
  getArticleDetail(id: number) {
    return axios.get(`/api/article/${id}`)
  }
}

export default api