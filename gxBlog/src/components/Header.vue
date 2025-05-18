<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BlurReveal from './ui/BlurReveal.vue'

const router = useRouter()
const activeIndex = ref('4')

const handleSelect = (key: string) => {
  // 更新activeIndex值
  activeIndex.value = key

  // 根据key进行路由跳转
  switch (key) {
    case '1':
      router.push('/')
      break
    case '2':
      router.push('/articles')
      break
    case '3':
      router.push('/about')
      break
    case '4':
      router.push('/blog')
      break
  }
}
</script>

<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <div class="logo-icon">✿</div>
        <div class="logo-text">
          <BlurReveal :duration="0.75" :delay="0.2" :blur="'15px'" :yOffset="10" class="blur-reveal-container">
            <h1 class="site-title">胖胖藏</h1>
            <p class="site-desc">✨ 分享技术与生活 ✨</p>
          </BlurReveal>
        </div>
      </div>
      <nav class="nav-menu">
        <ul>
          <li>
            <a href="#" @click.prevent="handleSelect('1')" :class="{ active: activeIndex === '1' }">
              <span class="nav-icon">🏠</span> <span class="nav-text">首页</span>
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="handleSelect('2')" :class="{ active: activeIndex === '2' }">
              <span class="nav-icon">📚</span> <span class="nav-text">文章</span>
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="handleSelect('3')" :class="{ active: activeIndex === '3' }">
              <span class="nav-icon">👋</span> <span class="nav-text">关于</span>
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="handleSelect('4')" :class="{ active: activeIndex === '4' }">
              <span class="nav-icon">📝</span> <span class="nav-text">博客</span>
            </a>
          </li>
        </ul>
      </nav>
    </div>
    <div class="floating-bubbles">
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
    </div>
  </header>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&display=swap');

.header {
  background-image: url('/header-backgroundPic.png');
  background-size: cover;
  background-position: center;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 3px solid #ffcce0;
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 248, 250, 0.85);
  z-index: -1;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 2.2rem;
  color: #ff69b4;
  animation: bounce 2s infinite;
  text-shadow: 0 0 10px rgba(255, 105, 180, 0.7);
  transition: transform 0.3s;
}

.logo:hover .logo-icon {
  transform: rotate(15deg) scale(1.2);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.blur-reveal-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.site-title {
  font-family: 'Mochiy Pop One', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #ff69b4;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(255, 105, 180, 0.3);
  position: relative;
  display: inline-block;
}

.site-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #ff69b4;
  transition: width 0.5s ease;
}

.logo:hover .site-title::after {
  width: 100%;
}

.site-desc {
  font-size: 0.9rem;
  color: #ff9dbb;
  margin: 0;
  letter-spacing: 1px;
  text-shadow: 0 0 5px rgba(255, 157, 187, 0.3);
  opacity: 0.9;
  transition: opacity 0.3s ease;
}

.logo:hover .site-desc {
  opacity: 1;
}

.nav-menu ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-menu li {
  margin-left: 1.5rem;
  margin-bottom: 0.5rem;
}

.nav-menu a {
  text-decoration: none;
  color: #ff69b4;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 0.5rem 0.8rem;
  transition: all 0.3s;
  position: relative;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
  overflow: hidden;
}

.nav-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.nav-text {
  position: relative;
  transition: transform 0.3s ease;
}

.nav-menu a:hover .nav-icon {
  transform: translateY(-3px) scale(1.2);
}

.nav-menu a:hover .nav-text {
  transform: translateY(3px);
}

.nav-menu a::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #ff69b4, #ffb6c1);
  opacity: 0;
  z-index: -1;
  transform: translateY(100%);
  transition: all 0.3s;
  border-radius: 20px;
}

.nav-menu a:hover::before,
.nav-menu a.active::before {
  opacity: 1;
  transform: translateY(0);
}

.nav-menu a:hover,
.nav-menu a.active {
  color: #fff;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);
}

/* 浮动气泡动画 */
.floating-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
  overflow: hidden;
}

.bubble {
  position: absolute;
  bottom: -50px;
  width: 30px;
  height: 30px;
  background: rgba(255, 182, 193, 0.3);
  border-radius: 50%;
  opacity: 0.5;
  animation: rise 15s infinite ease-in;
}

.bubble:nth-child(1) {
  width: 20px;
  height: 20px;
  left: 10%;
  animation-duration: 12s;
}

.bubble:nth-child(2) {
  width: 15px;
  height: 15px;
  left: 30%;
  animation-duration: 18s;
  animation-delay: 1s;
}

.bubble:nth-child(3) {
  width: 25px;
  height: 25px;
  left: 50%;
  animation-duration: 15s;
  animation-delay: 2s;
}

.bubble:nth-child(4) {
  width: 18px;
  height: 18px;
  left: 70%;
  animation-duration: 20s;
  animation-delay: 3s;
}

.bubble:nth-child(5) {
  width: 22px;
  height: 22px;
  left: 85%;
  animation-duration: 16s;
  animation-delay: 4s;
}

@keyframes rise {
  0% {
    bottom: -50px;
    transform: translateX(0);
  }

  50% {
    transform: translateX(40px);
  }

  100% {
    bottom: 120%;
    transform: translateX(-40px);
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

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

/* 响应式设计优化 */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    padding: 1rem;
  }

  .nav-menu ul {
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1rem;
  }

  .nav-menu li {
    margin: 0.5rem;
  }

  .logo {
    margin-bottom: 0.5rem;
  }
}
</style>