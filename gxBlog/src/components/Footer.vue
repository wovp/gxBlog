<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于博客</h3>
          <p>欢迎来到高兴的博客，用于分享技术文章和个人见解。</p>
        </div>
        <div class="footer-section">
          <h3>联系方式</h3>
          <ul class="contact-list">
            <li><i class="icon-email"></i> zhiqqwwgg@gmail.com</li>
            <li><i class="icon-github"></i> github.com/wovp</li>
            <li><i class="icon-weixin"></i> none</li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>快速链接</h3>
          <ul class="quick-links">
            <li><a href="/">首页</a></li>
            <li><a href="/articles">文章</a></li>
            <li><a href="/about">关于</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} 个人博客 | 版权所有</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
/* 引入外部CSS文件 */
@import '../assets/css/Footer.css';
</style>