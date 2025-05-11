<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import ArticleToc from '../components/ArticleToc.vue'
import { Article } from '../model/article'
import MarkdownIt from 'markdown-it'
// 导入PrismJS及相关样式
import Prism from 'prismjs'
// 导入基础样式
import 'prismjs/themes/prism-tomorrow.css' // 使用tomorrow主题
// 导入行号插件
import 'prismjs/plugins/line-numbers/prism-line-numbers.js'
import 'prismjs/plugins/line-numbers/prism-line-numbers.css'
// 导入工具栏插件（提供复制按钮等）
import 'prismjs/plugins/toolbar/prism-toolbar.js'
import 'prismjs/plugins/toolbar/prism-toolbar.css'
import 'prismjs/plugins/copy-to-clipboard/prism-copy-to-clipboard.js'
// 按需导入常用语言
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-css'
import 'prismjs/components/prism-markup' // HTML
import 'prismjs/components/prism-markdown'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-java'
import 'prismjs/components/prism-c'
import 'prismjs/components/prism-cpp'
import 'prismjs/components/prism-csharp'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-yaml'
import 'prismjs/components/prism-sql'
import articleApi from '../api/articleApi'
import { getRandomCoverImage } from '../assets/imageResources'
import { debugLog, debugError } from '../utils/debug'

// 初始化markdown解析器
const md = new MarkdownIt({
  html: true,        // 允许HTML标签
  linkify: true,     // 自动将URL转换为链接
  typographer: true, // 启用一些语言中立的替换和引号美化
  breaks: true,      // 将换行符转换为<br>
  highlight: function (str, lang) {
    // 代码高亮处理
    if (lang && Prism.languages[lang]) {
      try {
        return `<pre class="line-numbers"><code class="language-${lang}">${Prism.highlight(str, Prism.languages[lang], lang)
          }</code></pre>`;
      } catch (err) {
        debugError('代码高亮错误:', err);
      }
    }
    // 如果语言不支持或出错，使用普通代码块
    return `<pre class="line-numbers"><code class="language-text">${md.utils.escapeHtml(str)}</code></pre>`;
  }
})

// 自定义处理图片引用
md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx];
  const srcIndex = token.attrIndex('src');
  const src = token.attrs[srcIndex][1];

  // 处理普通图片 - 确保图片能够完整显示
  return `<div class="image-container"><img src="${src}" alt="${token.content || ''}" class="article-image" style="max-width: 100%; width: auto; height: auto;" /></div>`;
}

import { generateSlug } from '../utils/slugUtils'

// 存储标题ID映射，用于在渲染时使用
const headingIdMap = new Map();

// 用于跟踪已经使用过的标题ID，避免重复使用
const usedHeadingIds = new Set();

// 自定义处理标题，添加ID以支持目录跳转
md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx];
  const nextToken = tokens[idx + 1];
  const level = token.tag.substr(1); // h1 -> 1, h2 -> 2, etc.

  if (nextToken && nextToken.type === 'inline' && nextToken.content) {
    // 查找是否已经为该标题生成过ID
    const text = nextToken.content;
    let slug;

    // 严格使用在extractHeadings中提取的标题ID
    // 精确匹配文本和级别，确保找到正确的标题
    // 查找未使用过的ID，处理相同文本和级别的标题
    const existingHeadingIndex = headingIds.value.findIndex(h =>
      h.text === text && h.level === parseInt(level) && !usedHeadingIds.has(h.id)
    );

    if (existingHeadingIndex !== -1) {
      const existingHeading = headingIds.value[existingHeadingIndex];
      slug = existingHeading.id;
      // 标记该ID已被使用
      usedHeadingIds.add(slug);
      debugLog(`使用已提取的标题ID: 文本="${text}", ID="${slug}"`);
    } else {
      // 如果找不到精确匹配，尝试只匹配文本
      const textMatchHeadingIndex = headingIds.value.findIndex(h =>
        h.text === text && !usedHeadingIds.has(h.id)
      );

      if (textMatchHeadingIndex !== -1) {
        const textMatchHeading = headingIds.value[textMatchHeadingIndex];
        slug = textMatchHeading.id;
        // 标记该ID已被使用
        usedHeadingIds.add(slug);
        debugLog(`使用文本匹配的标题ID: 文本="${text}", ID="${slug}"`);
      } else {
        // 这种情况不应该发生，因为我们已经在提取阶段为所有标题生成了ID
        // 但为了健壮性，仍然提供一个后备方案
        debugError(`警告：无法找到标题的ID: 文本="${text}", 级别=${level}`);
        // 使用与extractHeadings相同的逻辑生成ID
        const baseId = generateSlug(text);
        slug = `${baseId}-idx${globalHeadingIndex++}`;
        // 标记该ID已被使用
        usedHeadingIds.add(slug);
        debugLog(`为标题生成新的ID(渲染时): 文本="${text}", ID="${slug}"`);
      }
    }

    return `<${token.tag} id="${slug}">`;
  }

  return self.renderToken(tokens, idx, options);
}

const route = useRoute()
const articleId = route.params.id

// 使用从imageResources导入的getRandomCoverImage函数

// 文章数据
const article = ref<Article>()
const markdownContent = ref('')
const loading = ref(true)

// 存储标题ID映射，用于传递给目录组件
const headingIds = ref<{ text: string, id: string, level: number }[]>([])

// 全局索引，确保每个标题都有唯一的ID
let globalHeadingIndex = 0;

// 在渲染Markdown前提取标题和ID
const extractHeadings = (content: string) => {
  const headingRegex = /^(#{1,3})\s+(.+)$/gm;
  const headings = [];
  let match;

  // 重置全局索引
  globalHeadingIndex = 0;

  // 用于跟踪相同文本和级别的标题出现次数
  const headingCounter = new Map<string, number>();

  while ((match = headingRegex.exec(content)) !== null) {
    const level = match[1].length;
    const text = match[2].trim();

    // 创建标题的唯一键（文本+级别）
    const headingKey = `${text}-${level}`;

    // 获取该标题的出现次数
    const count = headingCounter.get(headingKey) || 0;
    // 更新计数器
    headingCounter.set(headingKey, count + 1);

    // 生成基础ID
    let baseId = generateSlug(text);

    // 添加全局索引作为后缀，确保唯一性
    // 如果是相同文本和级别的标题的第二次或更多次出现，添加出现次数作为额外标识
    const id = count > 0
      ? `${baseId}-idx${globalHeadingIndex}-dup${count}`
      : `${baseId}-idx${globalHeadingIndex}`;

    // 递增全局索引
    globalHeadingIndex++;

    headings.push({ text, id, level });
    debugLog(`提取标题: 文本="${text}", ID="${id}", 级别=${level}, 索引=${globalHeadingIndex - 1}, 重复次数=${count}`);
  }

  return headings;
}

// 监听markdownContent变化，提取标题ID
watch(() => markdownContent.value, (newContent) => {
  if (newContent) {
    // 先提取标题和ID
    headingIds.value = extractHeadings(newContent);
    debugLog(`提取了${headingIds.value.length}个标题ID`);
  }
}, { immediate: true });

// 将Markdown内容转换为HTML
const htmlContent = computed(() => {
  // 使用已提取的标题ID渲染Markdown
  return md.render(markdownContent.value);
})

// 目录功能已移至ArticleToc组件

// 获取文章详情
const fetchArticleDetail = async () => {
  loading.value = true
  try {
    // 调用API获取文章详情
    debugLog('获取文章详情，ID:', articleId)
    const response = await articleApi.getArticleDetail(String(articleId))

    if (response.data.code === 200) {
      const articleData = response.data.data
      debugLog('文章详情数据:', articleData)

      // 处理Markdown内容中的Obsidian图片引用
      let processedMarkdown = articleData.markdownContent || ''
      // 替换Obsidian风格的图片引用 ![[image.png]] 为标准Markdown图片语法 ![alt](src)
      processedMarkdown = processedMarkdown.replace(/!\[\[(.*?)\]\]/g, '![$1](/images/$1)')

      // 保存处理后的Markdown原始内容
      markdownContent.value = processedMarkdown

      // 设置文章数据
      article.value = {
        id: Number(articleData.articleId),
        title: articleData.title,
        content: '', // 这里不再直接使用content字段，而是使用computed的htmlContent
        author: articleData.author,
        createTime: articleData.createTime,
        tags: articleData.category ? [articleData.category.name] : [],
        viewCount: articleData.viewCount || 0,
        commentCount: articleData.commentCount || 0,
        coverImage: articleData.coverImage || getRandomCoverImage(),
        comments: articleData.comments || []
      }

      // 如果API没有返回评论数据，则使用模拟评论
      if (!article.value.comments || article.value.comments.length === 0) {
        article.value.comments = Array.from({ length: 5 + Number(articleId) % 5 }, (_, index) => ({
          id: index + 1,
          content: `这是对文章 ${articleId} 的评论 ${index + 1}。非常喜欢这篇文章，内容详实，观点独到，给我带来了很多启发。`,
          author: ['读者A', '技术爱好者', '前端开发者', '学习者', '路人甲'][index % 5],
          createTime: new Date(Date.now() - Math.floor(Math.random() * 10000000000)).toISOString()
        }))
      }
    } else {
      console.warn('API返回错误，使用模拟数据')
      // 使用模拟数据，但不在这里硬编码，而是再次调用API以使用mock数据
      setTimeout(async () => {
        try {
          const mockResponse = await articleApi.getArticleDetail(String(articleId))
          if (mockResponse.data.code === 200) {
            const mockArticleData = mockResponse.data.data
            markdownContent.value = mockArticleData.markdownContent || ''

            article.value = {
              id: Number(mockArticleData.articleId),
              title: mockArticleData.title,
              content: '',
              author: mockArticleData.author,
              createTime: mockArticleData.createTime,
              tags: mockArticleData.category ? [mockArticleData.category.name] : [],
              viewCount: mockArticleData.viewCount || 0,
              commentCount: mockArticleData.commentCount || 0,
              coverImage: mockArticleData.coverImage || getRandomCoverImage(),
              comments: mockArticleData.comments || []
            }
          } else {
            throw new Error('Mock API also failed')
          }
        } catch (mockError) {
          console.error('Mock数据获取失败:', mockError)
          // 如果mock数据也失败，则使用完全硬编码的数据
          markdownContent.value = `# 详细文章标题 ${articleId}

这是文章 ${articleId} 的详细内容。

Vue.js是一个用于构建用户界面的渐进式JavaScript框架。与其它大型框架不同的是，Vue被设计为可以自底向上逐层应用。Vue的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。

## Vue的特点

Vue.js的设计受到了Angular和React等框架的启发，但它提供了更简单的API和更小的体积。Vue.js的主要特点包括：

* 响应式数据绑定：当数据变化时，视图会自动更新
* 组件化开发：可以构建可复用的组件
* 虚拟DOM：提高渲染性能
* 轻量级：压缩后只有约20KB
* 易学易用：学习曲线平缓

## Vue 3的新特性

Vue 3带来了许多重要的改进和新特性：

1. Composition API：提供了更灵活的代码组织方式
2. 更好的TypeScript支持：改进了类型推断
3. 性能提升：渲染速度更快，内存占用更少
4. Tree-shaking友好：更小的打包体积

Vue.js的生态系统也非常丰富，包括Vue Router用于路由管理，Vuex用于状态管理，以及许多其他官方和社区维护的库。

## 结论

Vue.js是一个灵活、高效且易于使用的前端框架，适合各种规模的项目。无论是小型应用还是大型企业级应用，Vue都能提供出色的开发体验和性能。`

          article.value = {
            id: Number(articleId),
            title: `详细文章标题 ${articleId}`,
            content: '',
            author: '技术专家',
            createTime: '2023-04-15T08:30:00',
            tags: ['Vue', 'JavaScript', '前端开发'],
            viewCount: 1200 + Number(articleId) * 100,
            commentCount: 25 + Number(articleId) * 5,
            coverImage: getRandomCoverImage(),
            comments: Array.from({ length: 5 + Number(articleId) % 5 }, (_, index) => ({
              id: index + 1,
              content: `这是对文章 ${articleId} 的评论 ${index + 1}。非常喜欢这篇文章，内容详实，观点独到，给我带来了很多启发。`,
              author: ['读者A', '技术爱好者', '前端开发者', '学习者', '路人甲'][index % 5],
              createTime: new Date(Date.now() - Math.floor(Math.random() * 10000000000)).toISOString()
            }))
          }
        }
        loading.value = false
      }, 500) // 短暂延迟以模拟网络请求
      return
    }

    // 设置loading为false
    loading.value = false
  } catch (error) {
    console.error('获取文章详情失败:', error)
    // 设置错误状态，不再使用硬编码的内容
    article.value = undefined
    loading.value = false
  }
}

// 目录相关功能已移至ArticleToc组件

// 不再需要目录相关的定时器

onMounted(async () => {
  try {
    // 引入mock数据
    import('../mock/articleMock')

    // 获取文章详情
    await fetchArticleDetail()

    // 确保Prism重新高亮页面上的代码块
    setTimeout(() => {
      Prism.highlightAll();
    }, 100);

    // 确保目录始终保持在左侧
    setTimeout(() => {
      const tocElement = document.querySelector('.toc-outside');
      if (tocElement) {
        tocElement.style.position = 'fixed';
        tocElement.style.left = '20px';
        tocElement.style.top = '80px';
        tocElement.style.zIndex = '100';
        debugLog('已强制设置目录位置为左侧固定');
      }
    }, 200);

    debugLog('文章详情页面初始化完成');
  } catch (error) {
    debugError('组件挂载过程出错:', error);
  }
})

// 组件卸载时清理资源
onUnmounted(() => {
  debugLog('文章详情页面资源已清理');
})

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}
</script>

<template>
  <div class="article-detail-page">
    <!-- 文章目录 - 完全移到article-detail-layout容器外部 -->
    <ArticleToc v-if="article && article.title.length > 0" :headingIds="headingIds" class="toc-outside" />

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="article" class="article-detail-layout">
      <div class="article-container" style="overflow: visible;">
        <!-- 文章头部 -->
        <header class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>
          <div class="article-meta">
            <span><i class="fas fa-user"></i> {{ article.author }}</span>
            <span><i class="fas fa-calendar"></i> {{ formatDate(article.createTime) }}</span>
            <span><i class="fas fa-eye"></i> {{ article.viewCount }} 阅读</span>
          </div>
          <div class="article-tags">
            <span v-for="(tag, index) in article.tags" :key="index" class="tag">
              {{ tag }}
            </span>
          </div>
        </header>

        <!-- 文章封面图 -->
        <div v-if="article.coverImage" class="article-cover">
          <img :src="article.coverImage" :alt="article.title" />
        </div>

        <!-- 文章内容 -->
        <div class="article-content-wrapper">
          <div class="article-content" v-html="htmlContent"></div>
        </div>

        <!-- 文章内容结束 -->
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-message">
      <div class="error-icon">⚠️</div>
      <h2>文章加载失败</h2>
      <p>很抱歉，我们无法加载您请求的文章。请稍后再试或返回首页。</p>
      <div>
        <button class="back-btn" @click="$router.push('/')">返回首页</button>
        <button class="retry-btn" @click="fetchArticleDetail">重试</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 引入外部CSS文件 */
@import '../assets/css/ArticleDetail.css';
</style>