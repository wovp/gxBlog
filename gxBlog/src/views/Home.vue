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
    <!-- 英雄区域 - 重新设计为更简约高级的风格 -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-icon">✨</div>
        <h1 class="hero-title">欢迎来到我的博客</h1>
        <p class="hero-subtitle">分享技术、知识和个人见解</p>
        <button class="hero-button" @click="$router.push('/articles')">
          <span>浏览文章</span>
          <span class="button-icon">→</span>
        </button>
      </div>
      <div class="hero-decoration">
        <div class="hero-circle hero-circle-1"></div>
        <div class="hero-circle hero-circle-2"></div>
        <div class="hero-circle hero-circle-3"></div>
      </div>
    </section>

    <!-- 特色功能区 - 替换原来的文章列表入口 -->
    <section class="features-section">
      <div class="feature-card" @click="$router.push('/articles')">
        <div class="feature-icon">📚</div>
        <div class="feature-content">
          <h2 class="feature-title">文章列表</h2>
          <p class="feature-desc">浏览所有文章，按分类查找</p>
        </div>
      </div>

      <div class="feature-card" @click="$router.push('/about')">
        <div class="feature-icon">👋</div>
        <div class="feature-content">
          <h2 class="feature-title">关于我</h2>
          <p class="feature-desc">了解博主的技术栈和经历</p>
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
          <p>你好，我是一名热爱技术的开发者。这个博客是我分享技术见解、学习心得和个人项目的地方。</p>
          <p>喜欢探索新技术和最佳实践。希望通过这个博客，能与更多志同道合的朋友交流学习。</p>
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

/* 英雄区域样式 - 更简约高级的设计 */
.hero {
  background: linear-gradient(135deg, #a6c0fe, #f68084);
  color: white;
  padding: 6rem 2rem;
  text-align: center;
  border-radius: 16px;
  margin-bottom: 3rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(166, 192, 254, 0.3);
  transition: all 0.5s ease;
}

.hero:hover {
  box-shadow: 0 15px 40px rgba(166, 192, 254, 0.4);
  transform: translateY(-5px);
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-icon {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
  display: inline-block;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(to right, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.3rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  font-weight: 300;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-button {
  background-color: white;
  color: #f68084;
  border: none;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.hero-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  background-color: #fafafa;
}

.button-icon {
  transition: transform 0.3s ease;
}

.hero-button:hover .button-icon {
  transform: translateX(5px);
}

.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.hero-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.hero-circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -50px;
}

.hero-circle-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  left: -50px;
}

.hero-circle-3 {
  width: 100px;
  height: 100px;
  top: 50%;
  left: 30%;
  background: rgba(255, 255, 255, 0.15);
}

/* 特色功能区样式 */
.features-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-color: #e0e0e0;
}

.feature-icon {
  font-size: 2.5rem;
  background-color: #fef5f5;
  color: #f68084;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-card:nth-child(2) .feature-icon {
  background-color: #f0f7ff;
  color: #a6c0fe;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.feature-desc {
  font-size: 1rem;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .features-section {
    grid-template-columns: 1fr;
  }

  .feature-card {
    padding: 1.5rem;
  }

  .feature-icon {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }
}

/* 最新文章样式 - 更简约高级的设计 */
.section-title {
  font-size: 2rem;
  margin-bottom: 2.5rem;
  text-align: center;
  color: #333;
  position: relative;
  padding-bottom: 0.8rem;
  font-weight: 700;
}

.section-title::before {
  content: '✨';
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.2rem;
  opacity: 0.7;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #a6c0fe, #f68084);
  border-radius: 3px;
}

.featured-articles {
  margin-bottom: 4rem;
  padding: 0 1rem;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2.5rem;
}

.article-item {
  height: 100%;
  transition: all 0.3s ease;
}

.article-item:hover {
  transform: translateY(-5px);
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
  border: 3px solid rgba(166, 192, 254, 0.2);
  border-radius: 50%;
  border-top-color: #f68084;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.loading p {
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .article-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .section-title {
    font-size: 1.8rem;
  }
}

/* 关于博主样式 - 更简约高级的设计 */
.about-section {
  background-color: #fff;
  padding: 4rem 2rem;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.03);
  border: 1px solid #f0f0f0;
  margin-top: 2rem;
  position: relative;
  overflow: hidden;
}

.about-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(to right, #a6c0fe, #f68084);
}

.about-content {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.about-image {
  flex-shrink: 0;
  position: relative;
}

.about-image::after {
  content: '👋';
  position: absolute;
  bottom: 10px;
  right: 10px;
  font-size: 2rem;
  animation: wave 2.5s ease-in-out infinite;
  transform-origin: 70% 70%;
}

@keyframes wave {

  0%,
  100% {
    transform: rotate(0deg);
  }

  20%,
  60% {
    transform: rotate(15deg);
  }

  40%,
  80% {
    transform: rotate(0deg);
  }
}

.about-image img {
  width: 180px;
  height: 180px;
  border-radius: 24px;
  object-fit: cover;
  border: 5px solid white;
  box-shadow: 0 10px 25px rgba(166, 192, 254, 0.2);
  transition: all 0.3s ease;
}

.about-image:hover img {
  transform: scale(1.05);
  box-shadow: 0 15px 35px rgba(166, 192, 254, 0.3);
}

.about-text {
  flex-grow: 1;
}

.about-text p {
  margin-bottom: 1.2rem;
  line-height: 1.8;
  color: #555;
  font-size: 1.05rem;
}

.about-button {
  background: linear-gradient(to right, #a6c0fe, #f68084);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1.5rem;
  box-shadow: 0 5px 15px rgba(166, 192, 254, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.about-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(166, 192, 254, 0.4);
}

.about-button::after {
  content: '→';
  transition: transform 0.3s ease;
}

.about-button:hover::after {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .about-content {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
  }

  .about-image img {
    width: 150px;
    height: 150px;
  }
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