<script setup lang="ts">
import { ref } from 'vue'
// 导入Naive UI组件
import {
    NSpace,
    NButton,
    NCard
} from 'naive-ui'

// 定义组件属性
const props = defineProps<{
    categories: any[]
    selectedCategory: string
}>()

// 定义事件
const emit = defineEmits<{
    (e: 'update:selectedCategory', categoryId: string): void
    (e: 'change', categoryId: string): void
}>()

// 切换分类
const changeCategory = (categoryId: string) => {
    const newCategoryId = categoryId === props.selectedCategory ? '' : categoryId
    emit('update:selectedCategory', newCategoryId)
    emit('change', newCategoryId)
}
</script>

<template>
    <n-card class="category-section" :bordered="false" :segmented="{ content: true }">
        <n-space justify="center" wrap>
            <n-button :type="selectedCategory === '' ? 'primary' : 'default'" @click="changeCategory('')" size="small"
                round class="category-button">
                全部
            </n-button>
            <n-button v-for="category in categories" :key="category.categoryId"
                :type="selectedCategory === category.categoryId ? 'primary' : 'default'"
                @click="changeCategory(category.categoryId)" size="small" round class="category-button">
                {{ category.name }}
            </n-button>
        </n-space>
    </n-card>
</template>

<style scoped>
/* 分类筛选区域 */
.category-section {
    margin-bottom: 2rem;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 16px;
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 15px rgba(74, 107, 223, 0.08);
    animation: slideDown 0.6s ease-out;
    padding: 16px;
    position: relative;
    overflow: hidden;
}

.category-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #4a6bdf, #6b9dff);
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.category-button {
    transition: all 0.3s ease;
    margin: 4px;
    font-weight: 500;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.category-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(74, 107, 223, 0.2), rgba(107, 157, 255, 0.2));
    transition: all 0.4s ease;
    z-index: -1;
    border-radius: 16px;
}

.category-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(74, 107, 223, 0.15);
}

.category-button:hover::before {
    left: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .category-section {
        padding: 12px 8px;
    }

    .category-button {
        font-size: 0.85rem;
        padding: 0 12px;
    }
}
</style>