<script setup lang="ts">
import { ref } from 'vue'

interface CommentItem {
  id: number
  content: string
  author: string
  createTime: string
}

interface Props {
  comments: CommentItem[]
}

const props = defineProps<Props>()

// 新评论表单
const commentForm = ref({
  author: '',
  content: ''
})

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 提交评论
const submitComment = () => {
  if (!commentForm.value.author.trim() || !commentForm.value.content.trim()) {
    alert('请填写昵称和评论内容')
    return
  }
  
  // 这里应该调用API提交评论，现在只是模拟
  alert('评论提交成功！')
  
  // 清空表单
  commentForm.value.author = ''
  commentForm.value.content = ''
}
</script>

<template>
  <div class="comment-section">
    <h3 class="comment-title">评论 ({{ comments.length }})</h3>
    
    <!-- 评论列表 -->
    <div class="comment-list" v-if="comments.length > 0">
      <div class="comment-item" v-for="comment in comments" :key="comment.id">
        <div class="comment-avatar">
          <!-- 使用评论者名字首字母作为头像 -->
          <div class="avatar-text">{{ comment.author.charAt(0).toUpperCase() }}</div>
        </div>
        <div class="comment-body">
          <div class="comment-header">
            <span class="comment-author">{{ comment.author }}</span>
            <span class="comment-time">{{ formatDate(comment.createTime) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>
    </div>
    
    <div class="no-comments" v-else>
      暂无评论，快来发表第一条评论吧！
    </div>
    
    <!-- 评论表单 -->
    <div class="comment-form">
      <h4>发表评论</h4>
      <div class="form-group">
        <label for="author">昵称</label>
        <input 
          type="text" 
          id="author" 
          v-model="commentForm.author" 
          placeholder="请输入您的昵称"
        >
      </div>
      <div class="form-group">
        <label for="content">评论内容</label>
        <textarea 
          id="content" 
          v-model="commentForm.content" 
          placeholder="请输入评论内容"
          rows="4"
        ></textarea>
      </div>
      <button class="submit-btn" @click="submitComment">提交评论</button>
    </div>
  </div>
</template>

<style scoped>
.comment-section {
  margin-top: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.8rem;
}

.comment-list {
  margin-bottom: 2rem;
}

.comment-item {
  display: flex;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.comment-avatar {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  margin-right: 1rem;
}

.avatar-text {
  width: 100%;
  height: 100%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 50%;
}

.comment-body {
  flex-grow: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
}

.comment-time {
  font-size: 0.85rem;
  color: #95a5a6;
}

.comment-content {
  line-height: 1.6;
  color: #34495e;
}

.no-comments {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
  font-style: italic;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.comment-form {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
}

.comment-form h4 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
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

@media (max-width: 768px) {
  .comment-section {
    padding: 1.5rem;
  }
  
  .comment-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .comment-time {
    margin-top: 0.3rem;
  }
}
</style>