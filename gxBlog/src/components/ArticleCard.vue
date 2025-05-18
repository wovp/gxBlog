<script setup lang="ts">
import { computed } from 'vue'
import type { ArticleListItem } from '../types/article'
// 导入Naive UI组件
import {
  NCard,
  NButton,
  NSpace,
  NTag,
  NText,
  NImage,
  NIcon
} from 'naive-ui'
// 导入图标
import { EyeOutline, ChatbubbleOutline } from '@vicons/ionicons5'

// 定义组件属性
const props = defineProps<{
  article: ArticleListItem
}>()

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}
</script>

<template>
  <n-card class="article-card" hoverable content-style="padding: 0;" :segmented="{ content: true }">
    <!-- 文章封面图 -->
    <template v-if="article.coverImage" #cover>
      <n-image :src="article.coverImage" :alt="article.title" object-fit="cover" class="article-image" />
    </template>

    <!-- 文章内容 -->
    <div class="article-content">
      <div class="article-meta">
        <div class="article-author">胖胖藏</div>
        <div class="article-date">{{ formatDate(article.createTime) }}</div>
      </div>

      <h3 class="article-title">{{ article.title }}</h3>

      <n-text depth="3" class="article-preview">{{ article.preview }}</n-text>

      <div class="article-footer">
        <!-- 文章标签 -->
        <div class="article-tags" v-if="article.tags && article.tags.length">
          <n-tag v-for="(tag, index) in article.tags" :key="index" type="primary" size="small" class="article-tag"
            :bordered="false">
            {{ tag }}
          </n-tag>
        </div>
        <!-- 文章统计 -->
        <div class="article-stats">
          <n-space size="small">
            <n-text v-if="article.viewCount" class="view-count">
              <n-icon size="16">
                <eye-outline />
              </n-icon>
              {{ article.viewCount }}
            </n-text>
            <n-text v-if="article.commentCount" class="comment-count">
              <n-icon size="16">
                <chatbubble-outline />
              </n-icon>
              {{ article.commentCount }}
            </n-text>
          </n-space>
        </div>
      </div>

      <div class="read-more-container">
        <router-link :to="`/article/${article.articleId}`" custom v-slot="{ navigate }">
          <n-button type="primary" ghost class="read-more-btn" @click="navigate">
            阅读全文
          </n-button>
        </router-link>
      </div>
    </div>
  </n-card>
</template>

<style scoped>
/* 文章卡片 */
.article-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  border: none;
  background: linear-gradient(145deg, #ffffff, #f7f9ff);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.8s ease-out;
  animation-fill-mode: both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(74, 107, 223, 0.15);
}

.article-card:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #4a6bdf, #6b9dff);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.article-card:hover:before {
  opacity: 1;
}

.article-image {
  height: 200px;
  width: 100%;
  object-fit: cover;
  transition: all 0.5s ease;
  filter: brightness(0.95);
}

.article-card:hover .article-image {
  transform: scale(1.05);
  filter: brightness(1.05);
}

.article-content {
  padding: 24px;
  border-radius: 0 0 16px 16px;
  background-color: #ffffff;
  position: relative;
  z-index: 1;
}

.article-content::before {
  content: '';
  position: absolute;
  top: -15px;
  left: 0;
  right: 0;
  height: 15px;
  background-color: #ffffff;
  border-radius: 16px 16px 0 0;
  z-index: -1;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.article-author {
  font-size: 0.9rem;
  color: #4a6bdf;
  font-weight: 500;
}

.article-date {
  font-size: 0.8rem;
  color: #888;
}

.article-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #333;
  line-height: 1.4;
  transition: all 0.3s ease;
  position: relative;
  padding-bottom: 12px;
  letter-spacing: 0.5px;
  text-overflow: ellipsis;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.article-title:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #4a6bdf, #6b9dff);
  transition: width 0.3s ease;
}

.article-card:hover .article-title {
  color: #4a6bdf;
}

.article-card:hover .article-title:after {
  width: 60px;
}

.article-preview {
  margin: 1rem 0;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  color: #666;
  font-size: 0.95rem;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.article-tag {
  transition: all 0.3s;
  background-color: rgba(74, 107, 223, 0.1) !important;
  color: #4a6bdf !important;
}

.article-tag:hover {
  background-color: rgba(74, 107, 223, 0.2) !important;
  transform: translateY(-2px);
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
  gap: 4px;
  transition: color 0.3s ease;
}

.article-card:hover .view-count,
.article-card:hover .comment-count {
  color: #4a6bdf;
}

.read-more-container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.read-more-btn {
  width: 100%;
  border-radius: 20px;
  transition: all 0.3s ease;
  border-color: #4a6bdf;
  color: #4a6bdf;
  font-weight: 500;
  letter-spacing: 1px;
}

.read-more-btn:hover {
  background-color: #4a6bdf;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(74, 107, 223, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .article-image {
    height: 180px;
  }

  .article-content {
    padding: 20px;
  }

  .article-title {
    font-size: 1.2rem;
  }

  .article-preview {
    -webkit-line-clamp: 2;
  }
}
</style>