<script setup lang="ts">
import type { NumberAnimationInst } from 'naive-ui'
import { onMounted, onUnmounted, ref } from 'vue'

// 创建 Intersection Observer 来处理淡入动画
let observer: IntersectionObserver

// 定义个人兴趣爱好
const hobbies = [
  { name: '阅读', icon: '📚' },
  { name: '旅行', icon: '✈️' },
  { name: '摄影', icon: '📷' },
  { name: '音乐', icon: '🎵' },
  { name: '编程', icon: '💻' }
]

// 计算年龄的逻辑
const birthYear = 2003 // 这里替换为你的出生年份
const currentAge = ref(0)

// 计算精确的年龄（包含小数部分）
const calculateAge = () => {
  const now = new Date()
  const birthDate = new Date(birthYear, 2, 19) // 假设1月1日为生日，可以根据实际情况调整
  const ageInMilliseconds = now.getTime() - birthDate.getTime()
  const ageInYears = ageInMilliseconds / (1000 * 60 * 60 * 24 * 365.25)
  currentAge.value = parseFloat(ageInYears.toFixed(9)) // 保留9位小数以实现平滑动画效果
}

// 定时更新年龄
let ageInterval: number | null = null

const goToGitHub = () => {
  window.open('https://github.com/wovp', '_blank');
}

onMounted(() => {
  const numberAnimationInstRef = ref<NumberAnimationInst | null>(null)
  // 设置 Intersection Observer
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
      }
    })
  }, {
    threshold: 0.1 // 当元素10%进入视口时触发
  })

  // 观察所有带有 fade-in-section 类的元素
  document.querySelectorAll('.fade-in-section').forEach(el => {
    observer.observe(el)
  })

  // 初始计算年龄
  calculateAge()
  numberAnimationInstRef.value?.play()
})

onUnmounted(() => {
  // 清除 Intersection Observer
  if (observer) {
    observer.disconnect()
  }

  // 清除年龄计时器
  if (ageInterval !== null) {
    clearInterval(ageInterval)
    ageInterval = null
  }
})
</script>

<template>
  <n-layout class="about-page">
    <n-layout-header>
      <n-page-header>
        <template #title>
          <n-gradient-text type="success" size="48">✨ 关于我 ✨</n-gradient-text>
        </template>
      </n-page-header>
    </n-layout-header>

    <n-layout-content>
      <!-- 作者信息卡片 -->
      <n-card class="author-card fade-in-section" hoverable>
        <div class="author-profile">
          <div class="avatar-container">
            <n-avatar size="64" :src="`avata.jpg`" class="author-avatar" />
            <div class="avatar-decoration">♥</div>
          </div>
          <div class="author-info">
            <n-h2 prefix="bar">技术博主</n-h2>
            <n-text depth="3">全栈开发工程师 / 技术写作者</n-text>
            <div class="social-links">
              <n-button quaternary circle class="social-button" title="github" @click="goToGitHub">
                <template #icon>
                  <n-icon>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                      <path
                        d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33c.85 0 1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"
                        fill="currentColor" />
                    </svg>
                  </n-icon>
                </template>
              </n-button>
            </div>
          </div>
        </div>
      </n-card>

      <!-- 个人简介 -->
      <n-card title="✨ 个人简介 ✨" class="about-section fade-in-section" hoverable>
        <n-text class="bio-text">
          <p>普通人</p>
        </n-text>
      </n-card>

      <!-- 年龄倒计时 -->
      <n-card title="✨ 我的年龄 ✨" class="about-section fade-in-section age-card" hoverable>
        <div class="age-container">
          <n-text class="age-label">我已经在这个世界上度过了</n-text>
          <div class="age-animation">
            <n-number-animation ref="numberAnimationInstRef" :from="0" :to="currentAge" :duration="5000" :precision="9"
              show-separator active />
            <n-text class="age-unit">岁</n-text>
          </div>
          <n-text class="age-description">时间飞逝，感谢相遇！</n-text>
        </div>
      </n-card>

      <!-- 兴趣爱好 -->
      <n-card title="✨ 兴趣爱好 ✨" class="about-section fade-in-section" hoverable>
        <n-grid :cols="5" :x-gap="12">
          <n-grid-item v-for="hobby in hobbies" :key="hobby.name">
            <n-card class="hobby-card" hoverable>
              <div class="hobby-icon">{{ hobby.icon }}</div>
              <n-text class="hobby-name">{{ hobby.name }}</n-text>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-card>
    </n-layout-content>
  </n-layout>
</template>

<style scoped>
.about-page {
  padding: 2rem 1rem;
  min-height: 100vh;
  background-color: #fff5f8;
  /* 淡粉色背景 */
}

.fade-in-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}

.fade-in-section.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.author-card {
  margin-bottom: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.author-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(255, 105, 180, 0.25);
}

.author-profile {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-container {
  position: relative;
}

.author-avatar {
  width: 80;
  height: 120px;
  border: 3px solid #ff69b4;
  box-shadow: 0 4px 8px rgba(255, 105, 180, 0.3);
  transition: transform 0.5s ease;
}

.avatar-decoration {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 24px;
  color: #ff69b4;
  animation: float 2s ease-in-out infinite;
}

.author-info {
  flex: 1;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.social-button {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.social-button:hover {
  transform: scale(1.2) rotate(5deg);
  background-color: rgba(255, 105, 180, 0.1);
}

.about-section {
  margin-bottom: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.about-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(255, 105, 180, 0.25);
}

.bio-text p {
  line-height: 1.8;
  margin-bottom: 1rem;
  font-size: 1.05rem;
}

.hobby-card {
  text-align: center;
  padding: 1rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #fff5f8 0%, #fff0f5 100%);
  box-shadow: 0 4px 8px rgba(255, 105, 180, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hobby-card:hover {
  transform: scale(1.1) rotate(3deg);
  box-shadow: 0 8px 16px rgba(255, 105, 180, 0.25);
}

.hobby-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  animation: bounce 2s ease infinite;
}

.hobby-name {
  font-weight: bold;
  color: #ff69b4;
}

.age-card {
  text-align: center;
}

.age-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
}

.age-label {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #ff69b4;
}

.age-animation {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin: 1rem 0;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: pulse 2s infinite;
}

.age-unit {
  margin-left: 0.5rem;
  font-size: 2rem;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.age-description {
  font-size: 1rem;
  color: #666;
  margin-top: 1rem;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(1);
  }
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

@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .author-profile {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .social-links {
    justify-content: center;
  }

  .hobby-card {
    padding: 0.5rem;
  }

  .hobby-icon {
    font-size: 2rem;
  }
}
</style>