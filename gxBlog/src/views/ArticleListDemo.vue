<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import articleApi from '../api/articleApi'
import type { ArticleListItem, Pagination } from '../types/article'
import { debugLog, debugError } from '../utils/debug'

// 状态变量
const articles = ref<ArticleListItem[]>([])
const pagination = ref<Pagination>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  totalPages: 0
})
const loading = ref<boolean>(false)
const categories = ref<any[]>([])
const selectedCategory = ref<string>('')

// 获取文章分类
const fetchCategories = async () => {
  try {
    const response = await articleApi.getCategories()
    if (response.status === 200) {
      categories.value = response.data || []
      debugLog('获取文章分类成功:', categories)
    }
  } catch (error) {
    debugError('获取文章分类失败:', error)
  }
}

// 获取文章列表
const fetchArticles = async (page = 1) => {
  loading.value = true
  try {
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' })

    const params: any = {
      pageSize: 10,
      currentPage: page,
      sortBy: 'createTime_desc'
    }

    // 如果选择了分类，添加分类ID到请求参数
    if (selectedCategory.value) {
      params.categoryId = selectedCategory.value
    }

    const response = await articleApi.getArticleList(params)

    if (response.data.code === 200) {
      articles.value = response.data.data.list
      pagination.value = response.data.data.pagination
    }
  } catch (error) {
    debugError('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 切换分类
const changeCategory = (categoryId: string) => {
  selectedCategory.value = categoryId === selectedCategory.value ? '' : categoryId
  fetchArticles(1)
}

// 切换页码
const changePage = (page: number) => {
  if (page < 1 || page > pagination.value.totalPages) return
  fetchArticles(page)
}

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 环境变量相关的计算属性
const isDebugMode = computed(() => import.meta.env.MODE === 'development' || import.meta.env.VITE_DEBUG === 'true')

onMounted(() => {
  // 只在开发环境且非调试模式下引入mock数据
  if (import.meta.env.MODE === 'development' && !isDebugMode.value) {
    import('../mock/articleMock')
  }

  // 获取分类列表
  fetchCategories()

  // 获取文章列表
  fetchArticles()
})
</script>

<template>
  <div class="article-list-demo">
    <div class="page-header">
      <h1 class="page-title">所有文章</h1>
      <p class="page-description">探索各种技术文章和个人见解</p>
    </div>

    <!-- 分类筛选区域 -->
    <div class="category-section">
      <div class="category-tags">
        <button class="category-tag" :class="{ active: selectedCategory === '' }" @click="changeCategory('')">
          全部
        </button>
        <button v-for="category in categories" :key="category.categoryId" class="category-tag"
          :class="{ active: selectedCategory === category.categoryId }" @click="changeCategory(category.categoryId)">
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 文章列表 -->
    <div v-else>
      <div v-if="articles.length === 0" class="empty-state">
        <p>没有找到相关文章</p>
      </div>

      <div v-else class="article-list">
        <div v-for="article in articles" :key="article.articleId" class="article-item">
          <div class="article-image" v-if="article.coverImage">
            <img :src="article.coverImage" :alt="article.title" />
          </div>
          <h2 class="article-title">{{ article.title }}</h2>
          <div class="article-meta">
            <span class="article-author">{{ article.author }}</span>
            <span class="article-date">{{ formatDate(article.createTime) }}</span>
          </div>
          <p class="article-preview">{{ article.preview }}</p>
          <div class="article-footer">
            <div class="article-tags" v-if="article.tags && article.tags.length">
              <span v-for="(tag, index) in article.tags" :key="index" class="article-tag">{{ tag }}</span>
            </div>
            <div class="article-stats">
              <span class="view-count" v-if="article.viewCount">👁️ {{ article.viewCount }}</span>
              <span class="comment-count" v-if="article.commentCount">💬 {{ article.commentCount }}</span>
            </div>
          </div>
          <router-link :to="`/article/${article.articleId}`" class="read-more">
            阅读全文
          </router-link>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="pagination.totalPages > 1">
        <button class="page-btn prev" :disabled="pagination.currentPage === 1"
          @click="changePage(pagination.currentPage - 1)">
          上一页
        </button>

        <button v-for="page in pagination.totalPages" :key="page" class="page-btn"
          :class="{ active: page === pagination.currentPage }" @click="changePage(page)">
          {{ page }}
        </button>

        <button class="page-btn next" :disabled="pagination.currentPage === pagination.totalPages"
          @click="changePage(pagination.currentPage + 1)">
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-list-demo {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  background: linear-gradient(to bottom, #f9f4ff, #fff8fa);
  position: relative;
  overflow: hidden;
}

/* 装饰元素 */
.article-list-demo::before,
.article-list-demo::after {
  content: '';
  position: absolute;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  z-index: -1;
  opacity: 0.1;
  animation: float 15s infinite ease-in-out alternate;
}

.article-list-demo::before {
  background: linear-gradient(45deg, #ff9a9e, #fad0c4);
  top: -50px;
  left: -50px;
}

.article-list-demo::after {
  background: linear-gradient(45deg, #a18cd1, #fbc2eb);
  bottom: -50px;
  right: -50px;
  animation-delay: 2s;
}

@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }

  100% {
    transform: translate(20px, 20px) rotate(10deg);
  }
}

/* 页面标题区域 */
.page-header {
  text-align: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.page-title {
  font-size: 2.5rem;
  color: #6a3093;
  margin-bottom: 0.5rem;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  display: inline-block;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  border-radius: 2px;
}

.page-description {
  font-size: 1.1rem;
  color: #8e8e8e;
  max-width: 600px;
  margin: 1rem auto 0;
  line-height: 1.6;
}

/* 分类筛选区域 */
.category-section {
  margin-bottom: 2rem;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 1rem;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(161, 140, 209, 0.2);
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
}

.category-tag {
  background: white;
  color: #6a3093;
  border: 1px solid rgba(161, 140, 209, 0.3);
  padding: 0.5rem 1.2rem;
  border-radius: 30px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.category-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(161, 140, 209, 0.2);
  border-color: rgba(161, 140, 209, 0.5);
}

.category-tag.active {
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 10px rgba(161, 140, 209, 0.3);
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(161, 140, 209, 0.2);
  border-radius: 50%;
  border-top-color: #a18cd1;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
  box-shadow: 0 0 10px rgba(161, 140, 209, 0.3);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  color: #777;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  border: 1px dashed #d9c6f7;
}

/* 文章列表 */
.article-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.article-item {
  background-color: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.4s ease;
  border: 1px solid rgba(161, 140, 209, 0.1);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.article-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.article-item:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 15px 30px rgba(161, 140, 209, 0.2);
  border-color: rgba(161, 140, 209, 0.3);
}

.article-item:hover::before {
  transform: scaleX(1);
}

.article-image {
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  height: 180px;
  overflow: hidden;
  position: relative;
  border-radius: 16px 16px 0 0;
}

.article-image::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.9), transparent);
  z-index: 1;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.article-item:hover .article-image img {
  transform: scale(1.05) rotate(1deg);
}

.article-title {
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  font-weight: 700;
  background: linear-gradient(to right, #6a3093, #a044ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.3;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 1rem;
  align-items: center;
}

.article-author::before {
  content: '👤 ';
}

.article-date::before {
  content: '📅 ';
}

.article-preview {
  color: #666;
  line-height: 1.7;
  margin-bottom: 1.2rem;
  position: relative;
  padding-left: 1rem;
  border-left: 2px solid #f0e6ff;
  flex-grow: 1;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.article-tag {
  background: linear-gradient(to right, #e0c3fc, #8ec5fc);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(142, 197, 252, 0.3);
  transition: all 0.3s;
}

.article-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(142, 197, 252, 0.4);
}

.article-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #888;
}

.view-count,
.comment-count {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.3s;
}

.view-count:hover,
.comment-count:hover {
  color: #6a3093;
  transform: scale(1.1);
}

.read-more {
  display: inline-block;
  color: #a044ff;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  position: relative;
  padding: 0.3rem 0;
}

.read-more::after {
  content: ' →';
  opacity: 0;
  transform: translateX(-5px);
  display: inline-block;
  transition: all 0.3s;
}

.read-more:hover {
  color: #6a3093;
}

.read-more:hover::after {
  opacity: 1;
  transform: translateX(3px);
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
  gap: 0.5rem;
}

.page-btn {
  background: linear-gradient(to bottom, #f9f4ff, #fff8fa);
  border: 1px solid rgba(161, 140, 209, 0.3);
  padding: 0.6rem 1.2rem;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s;
  color: #6a3093;
  font-weight: 600;
  min-width: 40px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.page-btn:hover:not(:disabled) {
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(161, 140, 209, 0.3);
}

.page-btn.active {
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  color: white;
  box-shadow: 0 5px 10px rgba(161, 140, 209, 0.3);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .article-list {
    grid-template-columns: 1fr;
  }

  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }

  .page-title {
    font-size: 2rem;
  }
}
</style>