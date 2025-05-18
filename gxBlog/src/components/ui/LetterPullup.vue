<template>
    <!-- 使用内联 flex 容器 -->
    <div class="inline-flex flex-wrap justify-center">
        <Motion v-for="(letter, index) in letters" :key="letter" as="span" :initial="pullupVariant.initial"
            :animate="pullupVariant.animate" :transition="{ delay: index * (props.delay || 0.05) }" :class="cn(
                'font-display text-center text-4xl font-bold tracking-[-0.02em] text-black drop-shadow-sm md:text-4xl md:leading-[5rem]',
                'inline-block', // 确保每个字母是行内块元素
                props.class
            )">
            <span v-if="letter === ' '">&nbsp;</span>
            <span v-else>{{ letter }}</span>
        </Motion>
    </div>
</template>

<script setup lang="ts">
import { Motion } from "motion-v";
import { cn } from "../../lib/utils";

interface LetterPullupProps {
    class?: string;
    words: string;
    delay?: number;
}

const props = defineProps<LetterPullupProps>();
const letters = props.words.split("");

const pullupVariant = {
    initial: { y: 100, opacity: 0 },
    animate: { y: 0, opacity: 1 },
};
</script>

<style scoped>
/* 确保没有意外的块级样式 */
.motion-component {
    display: inline-block !important;
}
</style>