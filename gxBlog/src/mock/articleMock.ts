import Mock from 'mockjs'
import { getRandomCoverImage } from '../assets/imageResources'
import { debugLog, debugWarn } from '../utils/debug'

// 模拟文章分类数据
Mock.mock('/api/category', 'get', () => {
  debugLog('Mock响应: 获取文章分类列表')
  return {
    code: 200,
    message: '成功',
    data: [
      {
        categoryId: '1',
        name: '技术分享',
        slug: 'tech-share',
        description: '编程经验、技术实践',
        createTime: '2023-05-01 12:00:00'
      },
      {
        categoryId: '2',
        name: '前端开发',
        slug: 'frontend',
        description: '前端技术、框架使用',
        createTime: '2023-05-02 14:30:00'
      },
      {
        categoryId: '3',
        name: '后端开发',
        slug: 'backend',
        description: '服务器端开发技术',
        createTime: '2023-05-03 09:15:00'
      },
      {
        categoryId: '4',
        name: '生活随笔',
        slug: 'life',
        description: '日常思考与感悟',
        createTime: '2023-05-04 16:45:00'
      }
    ]
  }
})


// 模拟文章列表数据
Mock.mock('/api/article/list', 'post', (options) => {
  debugLog('Mock响应: 获取文章列表', { requestBody: options.body })
  const body = JSON.parse(options.body)
  const categoryId = body.categoryId
  const pageSize = body.pageSize || 10
  const currentPage = body.currentPage || 1

  // 生成模拟数据
  const total = 100
  const totalPages = Math.ceil(total / pageSize)

  // 生成文章列表
  const list = []
  for (let i = 0; i < pageSize; i++) {
    const index = (currentPage - 1) * pageSize + i
    if (index < total) {
      list.push({
        articleId: String(index + 1),
        title: `${categoryId ? `[${categoryId}类]` : ''}文章标题${index + 1}`,
        author: Mock.Random.cname(),
        createTime: Mock.Random.datetime('yyyy-MM-dd HH:mm:ss'),
        preview: Mock.Random.paragraph(2)
      })
    }
  }

  return {
    code: 200,
    message: '成功',
    data: {
      list,
      pagination: {
        total,
        pageSize,
        currentPage,
        totalPages
      }
    }
  }
})

// 模拟文章详情数据
Mock.mock(new RegExp('/api/article/\d+'), 'get', (options) => {
  debugLog('Mock响应: 获取文章详情', { url: options.url })
  const url = options.url
  const match = url.match(/\/api\/article\/(\d+)/)
  if (!match) {
    throw new Error('无效的文章ID')
  }
  const articleId = match[1]

  // 生成Markdown格式的内容
  const markdownContent = `# 文章详情标题 ${articleId}

这是文章 ${articleId} 的详细内容。这里是一些技术描述和内容介绍。

## 技术背景

这是一个很长的段落，包含了很多技术细节和实现方法。Vue.js是一个用于构建用户界面的渐进式JavaScript框架。与其它大型框架不同的是，Vue被设计为可以自底向上逐层应用。Vue的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。

## 主要特点

Vue.js的设计受到了Angular和React等框架的启发，但它提供了更简单的API和更小的体积。Vue.js的主要特点包括：

* 响应式数据绑定：当数据变化时，视图会自动更新
* 组件化开发：可以构建可复用的组件
* 虚拟DOM：提高渲染性能
* 轻量级：压缩后只有约20KB
* 易学易用：学习曲线平缓

## 代码示例

\`\`\`
// 创建一个Vue应用
const app = Vue.createApp({
  data() {
    return {
      message: "Hello Vue!"
    }
  }
})

// 挂载应用
app.mount('#app')
\`\`\`

## 总结

这是总结和展望部分。Vue.js是一个灵活、高效且易于使用的前端框架，适合各种规模的项目。无论是小型应用还是大型企业级应用，Vue都能提供出色的开发体验和性能。`

  // 使用markdown-it转换为HTML（实际应用中通常在前端进行转换，这里只是模拟）
  const htmlContent = markdownContent
    .replace(/^# (.*)$/m, '<h1>$1</h1>')
    .replace(/^## (.*)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.*)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*)\*/g, '<em>$1</em>')
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\* (.*)/g, '<li>$1</li>')
    .split('</p><p>').join('</p>\n<p>')

  return {
    code: 200,
    message: '成功',
    data: {
      articleId,
      title: `文章详情标题 ${articleId}`,
      author: Mock.Random.cname(),
      createTime: Mock.Random.datetime('yyyy-MM-dd HH:mm:ss'),
      updateTime: Mock.Random.datetime('yyyy-MM-dd HH:mm:ss'),
      category: {
        categoryId: '1',
        name: '技术分享'
      },
      markdownContent: markdownContent,
      htmlContent: htmlContent
    }
  }
})

// 模拟搜索文章数据
Mock.mock(/\/api\/article\/search/, 'get', (options) => {
  debugLog('Mock响应: 搜索文章', { url: options.url })
  const url = new URL(options.url, 'http://localhost')
  const keyword = url.searchParams.get('keyword') || ''
  const pageSize = Number(url.searchParams.get('pageSize')) || 10
  const currentPage = Number(url.searchParams.get('currentPage')) || 1

  // 生成模拟数据
  const total = keyword ? 20 : 0 // 如果有关键词才返回结果
  const totalPages = Math.ceil(total / pageSize)

  // 生成文章列表
  const list = []
  for (let i = 0; i < pageSize; i++) {
    const index = (currentPage - 1) * pageSize + i
    if (index < total) {
      list.push({
        articleId: String(index + 1),
        title: `包含"${keyword}"的文章${index + 1}`,
        author: Mock.Random.cname(),
        createTime: Mock.Random.datetime('yyyy-MM-dd HH:mm:ss'),
        preview: `这是一篇包含"${keyword}"关键词的文章摘要...${Mock.Random.paragraph(1)}`
      })
    }
  }

  return {
    code: 200,
    message: '成功',
    data: {
      list,
      pagination: {
        total,
        pageSize,
        currentPage,
        totalPages
      }
    }
  }
})