<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

interface Props {
  article: {
    id: number
    title: string
    content: string
    author: string
    createTime: string
    tags: string[]
    viewCount: number
    commentCount: number
    coverImage: string
  }
}

const props = defineProps<Props>()
const router = useRouter()

const summary = computed(() => {
  // 生成文章摘要，截取前100个字符
  return props.article.content.length > 100
    ? props.article.content.substring(0, 100) + '...'
    : props.article.content
})

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const goToDetail = () => {
  router.push(`/article/${props.article.id}`)
}
</script>

<template>
  <div class="article-card" @click="goToDetail">
    <div class="article-image">
      <img :src="article.coverImage" :alt="article.title" />
    </div>
    <div class="article-content">
      <h2 class="article-title">{{ article.title }}</h2>
      <div class="article-meta">
        <span class="article-author">{{ article.author }}</span>
        <span class="article-date">{{ formatDate(article.createTime) }}</span>
      </div>
      <p class="article-summary">{{ summary }}</p>
      <div class="article-footer">
        <div class="article-tags">
          <span v-for="(tag, index) in article.tags" :key="index" class="tag">{{ tag }}</span>
        </div>
        <div class="article-stats">
          <span class="views"><i class="icon-eye"></i> {{ article.viewCount }}</span>
          <span class="comments"><i class="icon-comment"></i> {{ article.commentCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 引入外部CSS文件 */
@import '../assets/css/ArticleCard.css';
</style>