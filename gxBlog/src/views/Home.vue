<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import ArticleCard from '../components/ArticleCard.vue'
import type { Article } from '../model/article'
import articleApi from '../api/articleApi'
import { getRandomCoverImage, getRandomAvatarImage } from '../assets/imageResources'
import { debugLog, debugTimeStart, debugTimeEnd, debugError } from '../utils/debug'

// 最新文章数据
const latestArticles = ref<Article[]>([])
const loading = ref(true)

// 环境变量相关的计算属性
// const isDev = computed(() => import.meta.env.DEV)
const envMode = computed(() => import.meta.env.MODE)
const isDebugMode = computed(() => import.meta.env.MODE === 'development' || import.meta.env.VITE_DEBUG === 'true')

// 获取最新文章
const fetchLatestArticles = async () => {
  debugLog('开始获取最新文章')
  debugTimeStart('fetchLatestArticles')
  loading.value = true
  try {
    // 调用API获取最新文章数据，按创建时间降序排序
    debugLog('准备调用API', {
      pageSize: 3,
      currentPage: 1,
      sortBy: 'createTime_desc'
    })

    const response = await articleApi.getArticleList({
      pageSize: 3, // 显示3篇最新文章
      currentPage: 1,
      sortBy: 'createTime_desc' // 按创建时间降序，获取最新文章
    })

    debugLog('API响应状态', {
      code: response.data.code,
      message: response.data.message,
      hasData: !!response.data.data,
      listLength: response.data.data?.list?.length || 0
    })

    if (response.data.code === 200) {
      // 将API返回的文章数据转换为Article类型
      latestArticles.value = response.data.data.list.map((item: any) => {
        debugLog('处理文章数据', item)
        return {
          id: Number(item.articleId),
          title: item.title,
          content: item.preview,
          author: item.author,
          createTime: item.createTime,
          tags: [], // API可能没有返回标签，使用空数组
          viewCount: 0, // 这些信息在列表接口可能没有
          commentCount: 0,
          coverImage: getRandomCoverImage(), // 使用本地随机图片
          comments: []
        }
      })
      debugLog('文章数据处理完成', { count: latestArticles.value.length })
    } else {
      debugError('API返回错误码', { code: response.data.code, message: response.data.message })
    }
  } catch (error) {
    debugError('获取最新文章失败', error)
    console.error('获取最新文章失败:', error)
  } finally {
    loading.value = false
    debugTimeEnd('fetchLatestArticles')
    debugLog('最新文章获取流程结束', { success: latestArticles.value.length > 0 })
  }
}

onMounted(() => {
  debugLog('Home组件挂载')

  // 只在开发环境且非调试模式下引入mock数据
  if (import.meta.env.MODE === 'development' && !isDebugMode.value) {
    debugLog('开发环境非调试模式：准备引入mock数据')
    import('../mock/articleMock')
      .then(() => debugLog('mock数据引入成功'))
      .catch(err => debugError('mock数据引入失败', err))
  } else {
    debugLog('生产环境或调试模式：不引入mock数据，直接使用后端API')
  }

  // 获取最新文章
  debugLog('准备获取最新文章')
  fetchLatestArticles()
})

</script>

<template>
  <div class="home">
    <!-- 调试信息面板，仅在开发环境或调试模式下显示 -->
    <div v-if="isDebugMode" class="debug-panel">
      <div class="debug-info">
        <h3>调试信息</h3>
        <p><strong>加载状态:</strong> {{ loading ? '加载中' : '加载完成' }}</p>
        <p><strong>文章数量:</strong> {{ latestArticles.length }}</p>
        <p><strong>环境:</strong> {{ envMode }}</p>
        <button @click="fetchLatestArticles" class="debug-reload">重新加载数据</button>
      </div>
    </div>
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">欢迎来到我的博客</h1>
        <p class="hero-subtitle">分享技术、知识和个人见解</p>
        <button class="hero-button" @click="$router.push('/articles')">浏览文章</button>
      </div>
    </section>

    <!-- 文章列表入口 -->
    <section class="demo-entry">
      <div class="demo-card" @click="$router.push('/articles')">
        <div class="demo-icon">🔍</div>
        <div class="demo-content">
          <h2 class="demo-title">文章列表</h2>
          <p class="demo-desc">浏览所有文章，支持分类、搜索功能</p>
          <button class="demo-btn">立即浏览</button>
        </div>
      </div>
    </section>

    <!-- 最新文章 -->
    <section class="featured-articles">
      <h2 class="section-title">最新文章</h2>
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      <div v-else class="article-grid">
        <div v-for="article in latestArticles" :key="article.id" class="article-item">
          <ArticleCard :article="article" />
        </div>
      </div>
    </section>

    <!-- 关于博主 -->
    <section class="about-section">
      <h2 class="section-title">关于博主</h2>
      <div class="about-content">
        <div class="about-image">
          <img :src="getRandomAvatarImage()" alt="博主头像" />
        </div>
        <div class="about-text">
          <p>你好，我是一名热爱技术的开发者，专注于前端和全栈开发。这个博客是我分享技术见解、学习心得和个人项目的地方。</p>
          <p>我擅长Vue、React、Node.js等技术栈，喜欢探索新技术和最佳实践。希望通过这个博客，能与更多志同道合的朋友交流学习。</p>
          <button class="about-button" @click="$router.push('/about')">了解更多</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 调试面板 */
.debug-panel {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 9999;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  font-size: 12px;
}

/* 移除了调试控制按钮相关样式 */

.debug-info {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #ddd;
}

.debug-info h3 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}

.debug-info p {
  margin: 5px 0;
  color: #666;
}

.debug-reload {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  margin-top: 8px;
  cursor: pointer;
  font-size: 11px;
}

.debug-reload:hover {
  background-color: #0069d9;
}

.home {
  padding-bottom: 3rem;
}

/* 英雄区域样式 */
.hero {
  background: linear-gradient(135deg, #3498db, #8e44ad);
  color: white;
  padding: 5rem 2rem;
  text-align: center;
  border-radius: 8px;
  margin-bottom: 3rem;
}

.hero-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-button {
  background-color: white;
  color: #3498db;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.3s, box-shadow 0.3s;
}

.hero-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 文章示例入口样式 */
.demo-entry {
  margin-bottom: 3rem;
}

.demo-card {
  background: linear-gradient(135deg, #ff69b4, #ffb6c1);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  color: white;
  box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.demo-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(255, 105, 180, 0.4);
}

.demo-icon {
  font-size: 4rem;
  background-color: rgba(255, 255, 255, 0.2);
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.demo-content {
  flex: 1;
}

.demo-title {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.demo-desc {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.demo-btn {
  background-color: white;
  color: #ff69b4;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.demo-btn:hover {
  background-color: #f8f8f8;
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .demo-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.5rem;
  }

  .demo-icon {
    width: 80px;
    height: 80px;
    font-size: 3rem;
  }

  .demo-title {
    font-size: 1.5rem;
  }
}

/* 精选文章样式 */
.section-title {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #2c3e50;
  position: relative;
  padding-bottom: 0.5rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 3px;
  background-color: #3498db;
}

.featured-articles {
  margin-bottom: 3rem;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.article-item {
  height: 100%;
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 关于博主样式 */
.about-section {
  background-color: #f8f9fa;
  padding: 3rem 2rem;
  border-radius: 8px;
}

.about-content {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.about-image {
  flex-shrink: 0;
}

.about-image img {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  border: 5px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.about-text {
  flex-grow: 1;
}

.about-text p {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #34495e;
}

.about-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.about-button:hover {
  background-color: #2980b9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero {
    padding: 3rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .about-content {
    flex-direction: column;
    text-align: center;
  }

  .about-image {
    margin-bottom: 1.5rem;
  }
}
</style>