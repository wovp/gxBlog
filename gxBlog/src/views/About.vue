<script setup lang="ts">
import { getRandomAvatarImage, getRandomBackgroundImage } from '../assets/imageResources'
</script>

<template>
  <div class="about-page">
    <div class="about-header">
      <h1 class="page-title">关于我</h1>
      <div class="author-profile">
        <div class="author-avatar">
          <img :src="getRandomAvatarImage()" alt="博主头像" />
        </div>
        <div class="author-info">
          <h2 class="author-name">技术博主</h2>
          <p class="author-title">全栈开发工程师 / 技术写作者</p>
          <div class="social-links">
            <a href="#" class="social-link">GitHub</a>
            <a href="#" class="social-link">微博</a>
            <a href="#" class="social-link">知乎</a>
            <a href="#" class="social-link">掘金</a>
          </div>
        </div>
      </div>
    </div>
    
    <div class="about-content">
      <section class="about-section">
        <h2 class="section-title">个人简介</h2>
        <div class="section-content">
          <p>你好，我是一名热爱技术的全栈开发工程师，拥有5年的Web开发经验。我专注于前端和后端技术，包括Vue、React、Node.js、Python等。</p>
          <p>我创建这个博客的目的是分享我在技术学习和工作中的经验、见解和心得。希望通过我的文章，能够帮助到更多的开发者，特别是那些正在学习编程的新手。</p>
          <p>除了编程，我还喜欢阅读、旅行和摄影。我相信技术应该服务于生活，而不仅仅是工作。</p>
        </div>
      </section>
      
      <section class="about-section">
        <h2 class="section-title">技能专长</h2>
        <div class="section-content">
          <div class="skills-container">
            <div class="skill-category">
              <h3 class="category-title">前端开发</h3>
              <ul class="skill-list">
                <li class="skill-item">
                  <span class="skill-name">HTML/CSS</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 95%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">JavaScript</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 90%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">Vue.js</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 92%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">React</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 85%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">TypeScript</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 80%"></div>
                  </div>
                </li>
              </ul>
            </div>
            
            <div class="skill-category">
              <h3 class="category-title">后端开发</h3>
              <ul class="skill-list">
                <li class="skill-item">
                  <span class="skill-name">Node.js</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 88%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">Python</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 75%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">Express/Koa</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 85%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">MongoDB</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 80%"></div>
                  </div>
                </li>
                <li class="skill-item">
                  <span class="skill-name">MySQL</span>
                  <div class="skill-bar">
                    <div class="skill-level" style="width: 78%"></div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
      
      <section class="about-section">
        <h2 class="section-title">工作经历</h2>
        <div class="section-content">
          <div class="timeline">
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3 class="timeline-title">高级前端开发工程师</h3>
                <p class="timeline-company">某科技有限公司</p>
                <p class="timeline-period">2021年至今</p>
                <p class="timeline-description">负责公司核心产品的前端架构设计和开发，优化用户体验，提升应用性能。主导了多个重要项目，包括产品重构和新功能开发。</p>
              </div>
            </div>
            
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3 class="timeline-title">全栈开发工程师</h3>
                <p class="timeline-company">某网络科技公司</p>
                <p class="timeline-period">2019年 - 2021年</p>
                <p class="timeline-description">参与公司多个项目的前后端开发，使用Vue.js和Node.js构建Web应用，负责数据库设计和API开发。</p>
              </div>
            </div>
            
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3 class="timeline-title">前端开发实习生</h3>
                <p class="timeline-company">某互联网公司</p>
                <p class="timeline-period">2018年 - 2019年</p>
                <p class="timeline-description">参与公司官网和内部系统的前端开发，学习和实践前端技术，包括HTML/CSS、JavaScript和Vue.js。</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="about-section">
        <h2 class="section-title">联系我</h2>
        <div class="section-content">
          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-label">邮箱：</span>
              <span class="contact-value">example@email.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">微信：</span>
              <span class="contact-value">wechat_id</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">GitHub：</span>
              <span class="contact-value">github.com/username</span>
            </div>
          </div>
          
          <div class="contact-form">
            <h3 class="form-title">给我留言</h3>
            <div class="form-group">
              <label for="name">您的姓名</label>
              <input type="text" id="name" placeholder="请输入您的姓名" />
            </div>
            <div class="form-group">
              <label for="email">您的邮箱</label>
              <input type="email" id="email" placeholder="请输入您的邮箱" />
            </div>
            <div class="form-group">
              <label for="message">留言内容</label>
              <textarea id="message" rows="5" placeholder="请输入留言内容"></textarea>
            </div>
            <button class="submit-btn">发送留言</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  padding-bottom: 3rem;
}

/* 页面头部 */
.about-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.author-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.author-avatar {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1.5rem;
  border: 5px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.author-name {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.author-title {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  color: #3498db;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #f0f7ff;
  transition: all 0.3s;
}

.social-link:hover {
  background-color: #3498db;
  color: white;
}

/* 内容区域 */
.about-content {
  max-width: 800px;
  margin: 0 auto;
}

.about-section {
  margin-bottom: 3rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-title {
  font-size: 1.5rem;
  padding: 1.5rem;
  margin: 0;
  background-color: #f8f9fa;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
}

.section-content {
  padding: 1.5rem;
}

.section-content p {
  line-height: 1.6;
  color: #34495e;
  margin-bottom: 1rem;
}

/* 技能部分 */
.skills-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.category-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.skill-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.skill-item {
  margin-bottom: 1rem;
}

.skill-name {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
}

.skill-bar {
  height: 8px;
  background-color: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
}

.skill-level {
  height: 100%;
  background-color: #3498db;
  border-radius: 4px;
}

/* 时间线 */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 0;
  left: 7px;
  height: 100%;
  width: 2px;
  background-color: #e0e0e0;
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-dot {
  position: absolute;
  left: -2rem;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #3498db;
  border: 2px solid white;
  z-index: 1;
}

.timeline-title {
  font-size: 1.2rem;
  margin: 0 0 0.5rem;
  color: #2c3e50;
}

.timeline-company {
  font-weight: 500;
  margin: 0 0 0.3rem;
  color: #34495e;
}

.timeline-period {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0 0 0.5rem;
}

.timeline-description {
  line-height: 1.5;
  color: #34495e;
}

/* 联系表单 */
.contact-info {
  margin-bottom: 2rem;
}

.contact-item {
  margin-bottom: 0.8rem;
}

.contact-label {
  font-weight: 600;
  color: #34495e;
}

.form-title {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #34495e;
}

input, textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, textarea:focus {
  border-color: #3498db;
  outline: none;
}

.submit-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #2980b9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .skills-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .author-profile {
    padding: 0 1rem;
  }
  
  .section-title {
    padding: 1rem;
  }
  
  .section-content {
    padding: 1rem;
  }
}
</style>