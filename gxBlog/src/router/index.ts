import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/articles',
    name: 'ArticleList',
    component: () => import('../views/ArticleListDemo.vue') // 使用功能更完整的组件
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: () => import('../views/ArticleDetail.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  }
  // 移除重复的ArticleListDemo路由
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router