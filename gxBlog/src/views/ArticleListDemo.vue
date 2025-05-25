<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import articleApi from '../api/articleApi'
import type { ArticleListItem, Pagination } from '../types/article'
import { debugLog, debugError } from '../utils/debug'
// 导入组件
import ArticleCard from '../components/ArticleCard.vue'
import CategoryButtons from '../components/CategoryButtons.vue'
// 导入Naive UI组件
import {
  NCard,
  NButton,

  NSpin,
  NEmpty,
  NPagination,
  NGrid,
  NGridItem,
  NPageHeader,
  NIcon,
  NLayout,
  NLayoutContent,
  NBackTop,
} from 'naive-ui'
// 导入图标
import { ArrowUpOutline } from '@vicons/ionicons5'

import Text3d from '../components/ui/Text3d.vue'
import LetterPullup from '../components/ui/LetterPullup.vue'
// 移除未使用的导入

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
    // 尝试从本地存储获取分类数据
    const cachedData = localStorage.getItem('blog_categories')
    const cachedTime = localStorage.getItem('blog_categories_time')
    const currentTime = new Date().getTime()

    // 检查缓存是否存在且未过期（7天有效期，因为分类很少变化）
    if (cachedData && cachedTime && (currentTime - parseInt(cachedTime)) < 7 * 24 * 60 * 60 * 1000) {
      categories.value = JSON.parse(cachedData)
      debugLog('从缓存获取文章分类成功:', categories)
      return
    }

    // 缓存不存在或已过期，从服务器获取
    const response = await articleApi.getCategories()
    if (response.status === 200) {
      categories.value = response.data || []

      // 将数据存入本地存储
      localStorage.setItem('blog_categories', JSON.stringify(response.data))
      localStorage.setItem('blog_categories_time', currentTime.toString())

      debugLog('从服务器获取文章分类成功:', categories)
    }
  } catch (error) {
    // 如果请求失败但有缓存数据，使用缓存数据
    const cachedData = localStorage.getItem('blog_categories')
    if (cachedData) {
      categories.value = JSON.parse(cachedData)
      debugLog('请求失败，使用缓存的文章分类数据')
    } else {
      debugError('获取文章分类失败:', error)
    }
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

    // 构建缓存键，包含分页和分类信息
    const cacheKey = `blog_articles_${params.currentPage}_${params.pageSize}_${params.categoryId || 'all'}_${params.sortBy}`
    const cacheTimeKey = `${cacheKey}_time`

    // 尝试从本地存储获取文章数据
    const cachedData = localStorage.getItem(cacheKey)
    const cachedTime = localStorage.getItem(cacheTimeKey)
    const currentTime = new Date().getTime()

    // 检查缓存是否存在且未过期（1天有效期，因为博客内容更新频率低）
    if (cachedData && cachedTime && (currentTime - parseInt(cachedTime)) < 24 * 60 * 60 * 1000) {
      const parsedData = JSON.parse(cachedData)
      articles.value = parsedData.list
      pagination.value = parsedData.pagination
      debugLog('从缓存获取文章列表成功')
      loading.value = false
      return
    }

    // 缓存不存在或已过期，从服务器获取
    const response = await articleApi.getArticleList(params)

    if (response.data.code === 200) {
      articles.value = response.data.data.list
      pagination.value = response.data.data.pagination

      // 将数据存入本地存储
      localStorage.setItem(cacheKey, JSON.stringify({
        list: response.data.data.list,
        pagination: response.data.data.pagination
      }))
      localStorage.setItem(cacheTimeKey, currentTime.toString())

      debugLog('从服务器获取文章列表成功')
    }
  } catch (error) {
    // 如果请求失败但有缓存数据，尝试使用缓存
    const cacheKey = `blog_articles_${page}_10_${selectedCategory.value || 'all'}_createTime_desc`
    const cachedData = localStorage.getItem(cacheKey)

    if (cachedData) {
      const parsedData = JSON.parse(cachedData)
      articles.value = parsedData.list
      pagination.value = parsedData.pagination
      debugLog('请求失败，使用缓存的文章列表数据')
    } else {
      debugError('获取文章列表失败:', error)
    }
  } finally {
    loading.value = false
  }
}

// 切换分类
const changeCategory = (categoryId: string) => {
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
  <n-layout class="article-list-container min-h-screen relative">
    <n-layout-content class="relative z-10">
      <!-- 页面标题区域 -->
      <n-page-header class="page-header">
        <template #title>
          <Text3d>
            所有文章
          </Text3d>
        </template>
        <template #subtitle>
          <LetterPullup words="探索各种技术文章和个人见解" :delay="0.5" class="text-black dark:text-white" />
        </template>
      </n-page-header>

      <!-- 分类筛选区域 -->
      <CategoryButtons :categories="categories" v-model:selectedCategory="selectedCategory" @change="changeCategory" />

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <n-spin size="large" />
        <p>加载中...</p>
      </div>

      <!-- 文章列表 -->
      <div v-else>
        <!-- 空状态 -->
        <n-card v-if="articles.length === 0" class="empty-state-card">
          <n-empty description="没有找到相关文章" size="large">
            <template #extra>
              <n-button type="primary" @click="changeCategory('')" size="small" class="empty-state-button">
                查看全部文章
              </n-button>
            </template>
          </n-empty>
        </n-card>

        <!-- 文章列表 -->
        <n-grid v-else x-gap="24" y-gap="24" cols="1 s:1 m:2 l:3" responsive="screen" class="article-grid">
          <n-grid-item v-for="article in articles" :key="article.articleId" class="article-grid-item">
            <ArticleCard :article="article" />
          </n-grid-item>
        </n-grid>

        <!-- 分页 -->
        <div class="pagination-container" v-if="pagination.totalPages > 1">
          <n-pagination v-model:page="pagination.currentPage" :page-count="pagination.totalPages" :page-sizes="[10]"
            :page-size="pagination.pageSize" :item-count="pagination.total" @update:page="changePage"
            show-quick-jumper />
        </div>
      </div>
    </n-layout-content>

    <!-- 回到顶部按钮 -->
    <n-back-top :right="30" :bottom="30">
      <div class="back-top-btn">
        <n-icon size="20">
          <arrow-up-outline />
        </n-icon>
      </div>
    </n-back-top>
  </n-layout>
</template>

<style scoped>
.article-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  background: transparent;
  /* 移除背景色，让雪花背景可见 */
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.8s ease-in-out;
  backdrop-filter: blur(1px);
  /* 添加轻微模糊效果增强视觉层次感 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 装饰元素 - 已由雪花背景替代，保留动画定义供其他元素使用 */
@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }

  25% {
    transform: translate(10px, 10px) rotate(5deg);
  }

  50% {
    transform: translate(0, 15px) rotate(0deg);
  }

  75% {
    transform: translate(-10px, 5px) rotate(-5deg);
  }

  100% {
    transform: translate(0, 0) rotate(0deg);
  }
}

@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }

  25% {
    transform: translate(10px, 10px) rotate(5deg);
  }

  50% {
    transform: translate(0, 15px) rotate(0deg);
  }

  75% {
    transform: translate(-10px, 5px) rotate(-5deg);
  }

  100% {
    transform: translate(0, 0) rotate(0deg);
  }
}

/* 页面标题区域 */
.page-header {
  /* margin-bottom: 1.5rem; */
  width: 100%;
  background-color: transparent;
}

.page-title {
  font-size: 2.5rem;
  color: #4a6bdf;
  margin-bottom: 0.5rem;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  display: inline-block;
  padding-bottom: 10px;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #4a6bdf, #6b9dff);
  border-radius: 2px;
}

/* 分类筛选区域样式已移至CategoryButtons组件 */

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  animation: pulse 1.5s infinite ease-in-out alternate;
}

@keyframes pulse {
  from {
    opacity: 0.7;
  }

  to {
    opacity: 1;
  }
}

.loading-container p {
  margin-top: 16px;
  color: #4a6bdf;
  font-weight: 500;
  letter-spacing: 1px;
}

/* 文章网格样式 */
.article-grid {
  margin: 20px 0;
}

.article-grid-item {
  perspective: 1000px;
  transform-style: preserve-3d;
  min-height: 450px;
}

/* 为卡片添加延迟动画 */
.article-grid-item:nth-child(3n+1) {
  animation-delay: 0.1s;
}

.article-grid-item:nth-child(3n+2) {
  animation-delay: 0.2s;
}

.article-grid-item:nth-child(3n+3) {
  animation-delay: 0.3s;
}

/* 搜索和分类区域 */
.search-and-filter {
  margin: 1rem 0;
  padding: 0 1rem;
}

.search-and-filter .n-input-group {
  margin-bottom: 1rem;
  max-width: 600px;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(74, 107, 223, 0.12);
  backdrop-filter: blur(5px);
  animation: fadeIn 0.8s ease-in-out;
  animation-delay: 0.5s;
  animation-fill-mode: both;
}

/* 空状态卡片 */
.empty-state-card {
  padding: 40px 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 8px 20px rgba(74, 107, 223, 0.1);
  backdrop-filter: blur(5px);
  animation: fadeIn 0.8s ease-in-out;
}

.empty-state-button {
  margin-top: 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.empty-state-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(74, 107, 223, 0.3);
}

/* 回到顶部按钮 */
.back-top-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(145deg, #4a6bdf, #6b9dff);
  color: white;
  box-shadow: 0 4px 10px rgba(74, 107, 223, 0.3);
  transition: all 0.3s ease;
}

.back-top-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(74, 107, 223, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .article-grid-item {
    min-height: 400px;
  }
}

@media (max-width: 480px) {
  .article-grid-item {
    min-height: 380px;
  }

  .article-grid {
    margin: 10px 0;
  }
}
</style>