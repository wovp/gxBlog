<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { debugLog, debugError } from '../utils/debug';

// 定义组件的props
const props = defineProps<{
    headingIds: { text: string, id: string, level: number }[]; // 从文章渲染时提取的标题ID映射
    scrollContainer?: Window | HTMLElement; // 滚动容器，默认为window
}>();

// 生成文章目录
const generateToc = (headings: { text: string, id: string, level: number }[]) => {
    if (!headings || headings.length === 0) return '';

    const toc = headings.map(heading => ({
        level: heading.level,
        text: heading.text,
        slug: heading.id
    }));

    debugLog(`使用传递的标题ID映射生成目录，共${toc.length}项`);
    toc.forEach(item => {
        debugLog(`目录项: 文本="${item.text}", ID="${item.slug}", 级别=${item.level}`);
    });

    if (toc.length === 0) return '';

    let html = '<div class="toc-container">';

    toc.forEach(heading => {
        // 使用生成的slug作为href和data-slug属性
        const href = `#${heading.slug}`;
        const dataSlug = heading.slug;

        // 根据标题级别设置不同的样式
        let levelStyle = '';
        let prefixChar = '';

        if (heading.level === 1) {
            levelStyle = 'font-weight: 600; color: #6c5ce7; display: block;'; // 一级标题：紫色，加粗
            prefixChar = '•';
        } else if (heading.level === 2) {
            levelStyle = 'font-weight: 500; color: #0984e3; margin-left: 1rem; display: block;'; // 二级标题：蓝色，中等粗细，缩进
            prefixChar = '◦';
        } else if (heading.level === 3) {
            levelStyle = 'font-weight: 400; color: #00b894; margin-left: 2rem; display: block;'; // 三级标题：绿色，正常粗细，更多缩进
            prefixChar = '·';
        }

        // 生成目录项HTML，使用内联样式控制外观和缩进
        html += `<div class="toc-item toc-level-${heading.level}"><a href="${href}" data-slug="${dataSlug}" data-text="${heading.text}" style="${levelStyle}">${prefixChar} ${heading.text}</a></div>`;
    });

    html += '</div>';
    return html;
};

// 目录HTML内容
const tocHtml = ref('');

// 监听headingIds变化，重新生成目录
watch(() => props.headingIds, (newHeadings) => {
    tocHtml.value = generateToc(newHeadings);
}, { immediate: true });

// 监听滚动事件，高亮当前阅读位置的目录项
const updateTocActiveState = () => {
    try {
        // 检查文档是否已加载完成
        if (!document || !document.body) return;

        // 获取文章内容容器
        const articleContent = document.querySelector('.article-content');
        if (!articleContent) return;

        // 获取所有标题元素
        const headings = articleContent.querySelectorAll('h1, h2, h3');
        if (!headings || headings.length === 0) return;

        // 获取目录容器
        const tocContainer = document.querySelector('.article-toc');
        if (!tocContainer) return;

        // 获取所有目录项
        const tocLinks = tocContainer.querySelectorAll('.toc-item a');
        if (!tocLinks || tocLinks.length === 0) return;

        // 清除所有目录项的active状态
        tocLinks.forEach(link => {
            if (link && link.classList) {
                link.classList.remove('active');
            }
        });

        // 找到当前可见的标题
        let currentHeadingId = '';
        const scrollPosition = window.scrollY + 100; // 添加一点偏移量
        // 从后往前遍历，找到第一个在视口上方的标题
        for (let i = headings.length - 1; i >= 0; i--) {
            const heading = headings[i];
            // 确保heading是HTMLElement类型，因为Element类型没有offsetTop属性
            if (heading && heading instanceof HTMLElement && heading.offsetTop <= scrollPosition) {
                currentHeadingId = heading.id;
                break;
            }
        }

        // 如果找到了当前标题，高亮对应的目录项
        if (currentHeadingId) {
            const activeLink = tocContainer.querySelector(`.toc-item a[href="#${currentHeadingId}"]`);
            if (activeLink && activeLink.classList) {
                activeLink.classList.add('active');

                // 确保当前高亮的目录项在视口内
                if (tocContainer && tocContainer instanceof HTMLElement) {
                    // 确保activeLink是HTMLElement类型
                    if (activeLink instanceof HTMLElement) {
                        const linkTop = activeLink.offsetTop;
                        const containerTop = tocContainer.scrollTop;
                        const containerHeight = tocContainer.offsetHeight;

                        if (linkTop < containerTop || linkTop > containerTop + containerHeight) {
                            tocContainer.scrollTop = linkTop - containerHeight / 2;
                        }
                    }
                }
            }
        } else if (tocLinks.length > 0 && tocLinks[0].classList) {
            // 如果没有找到当前标题，默认高亮第一个目录项
            tocLinks[0].classList.add('active');
        }
    } catch (error) {
        debugError('目录高亮更新失败:', error);
    }
};

// 点击目录项时平滑滚动到对应位置
const setupTocClickHandlers = () => {
    try {
        // 检查文档是否已加载完成
        if (!document || !document.body) return;

        // 获取目录容器
        const tocContainer = document.querySelector('.article-toc');
        if (!tocContainer) return;

        // 获取所有目录项
        const tocLinks = tocContainer.querySelectorAll('.toc-item a');
        if (!tocLinks || tocLinks.length === 0) return;

        tocLinks.forEach(link => {
            if (!link) return;

            // 移除可能已存在的事件监听器，避免重复添加
            const oldClickListener = link._clickListener;
            if (oldClickListener) {
                link.removeEventListener('click', oldClickListener);
            }

            // 创建新的事件监听器
            const clickListener = (e) => {
                e.preventDefault();
                if (!link.getAttribute) return;

                const href = link.getAttribute('href');
                if (!href) {
                    debugError('目录项链接href属性为空');
                    return;
                }

                // 检查href是否只有#
                if (href === '#') {
                    debugError('目录项链接href属性只有#，缺少ID');
                    return;
                }

                const targetId = href.substring(1);
                if (!targetId) {
                    debugError('目录项链接targetId为空');
                    return;
                }

                // 直接使用ID精确匹配，因为我们已经确保了目录项ID和标题ID完全一致
                const targetElement = document.getElementById(targetId);

                // 添加调试信息
                debugLog(`目录点击: href="${href}", targetId="${targetId}", 元素存在=${targetElement !== null}`);

                // 不再需要文本匹配作为备选方案，因为我们已经确保了ID的一致性

                if (targetElement) {
                    // 计算更合适的偏移量
                    // 考虑页面顶部的导航栏、文章标题等元素的高度
                    const headerOffset = 120; // 增加偏移量，确保标题完全可见

                    // 获取元素相对于文档的位置
                    const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;

                    // 计算滚动位置，考虑偏移量
                    const offsetPosition = elementPosition - headerOffset;

                    // 平滑滚动到目标位置
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    debugLog(`滚动到元素: id="${targetElement.id}", 位置=${offsetPosition}, 原始位置=${elementPosition}`);

                    // 高亮当前点击的目录项
                    document.querySelectorAll('.toc-item a').forEach(item => {
                        item.classList.remove('active');
                    });
                    link.classList.add('active');
                } else {
                    debugError(`无法找到目标元素: ${targetId}`);
                }
            };

            // 保存事件监听器引用，以便后续可以移除
            link._clickListener = clickListener;

            // 添加事件监听器
            link.addEventListener('click', clickListener);
        });

        debugLog('目录点击事件设置成功');
    } catch (error) {
        debugError('设置目录点击事件失败:', error);
    }
};

// 扩展Window接口，添加自定义属性
declare global {
    interface Window {
        _tocScrollHandler?: EventListener;
        __DEBUG__?: boolean;
    }
}

// 存储定时器ID，以便在组件卸载时清除
let tocInitTimer: number | null = null;

onMounted(() => {
    try {
        // 等待文章内容和DOM完全加载后设置目录相关功能
        // 增加延迟时间，确保DOM元素完全渲染
        tocInitTimer = window.setTimeout(() => {
            try {
                debugLog('初始化目录功能');

                // 设置目录点击事件
                setupTocClickHandlers();

                // 初始化目录高亮
                updateTocActiveState();

                // 监听滚动事件，使用防抖处理以提高性能
                const scrollHandler = () => {
                    window.requestAnimationFrame(() => {
                        updateTocActiveState();
                        // debugLog('滚动事件触发，更新目录高亮'); // 注释掉滚动事件调试信息
                    });
                };

                // 保存事件处理函数引用，以便在组件卸载时移除
                window._tocScrollHandler = scrollHandler;

                // 添加滚动事件监听
                window.addEventListener('scroll', scrollHandler, { passive: true });

                // 强制检查目录容器的样式
                const tocContainer = document.querySelector('.article-toc');
                if (tocContainer && tocContainer instanceof HTMLElement) {
                    // 确保目录容器有正确的样式
                    tocContainer.style.position = 'sticky';
                    tocContainer.style.top = '20px';
                    tocContainer.style.maxHeight = 'calc(100vh - 40px)';
                    tocContainer.style.overflowY = 'auto';
                    debugLog('已强制设置目录容器样式');
                }

                debugLog('目录功能初始化完成');
            } catch (error) {
                debugError('目录功能初始化失败:', error);
            }
        }, 1500); // 增加延迟时间到1.5秒
    } catch (error) {
        debugError('组件挂载过程出错:', error);
    }
});

// 组件卸载时清理资源
onUnmounted(() => {
    try {
        // 清除定时器
        if (tocInitTimer !== null) {
            clearTimeout(tocInitTimer);
            tocInitTimer = null;
        }

        // 移除滚动事件监听
        if (window._tocScrollHandler) {
            window.removeEventListener('scroll', window._tocScrollHandler);
            delete window._tocScrollHandler;
        } else {
            // 兼容性处理，确保事件监听被移除
            window.removeEventListener('scroll', updateTocActiveState);
        }

        debugLog('目录功能资源已清理');
    } catch (error) {
        debugError('清理目录功能资源失败:', error);
    }
});
</script>

<template>
    <div class="article-toc" v-if="tocHtml">
        <div class="toc-header">
            <span class="toc-icon">📚</span> 目录
        </div>
        <div class="toc-content" v-html="tocHtml"></div>
    </div>
</template>

<style scoped>
/* 引入外部CSS文件 */
@import '../assets/css/ArticleToc.css';
</style>