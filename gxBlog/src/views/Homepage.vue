<template>
    <div class="homepage-container">
        <!-- 这里将通过iframe嵌入homepage项目的dist页面 -->
        <iframe src="/public/homepage/dist/index.html" style="width:100vw;height:100vh;border:none;min-height:600px;"
            title="个人主页" allowfullscreen></iframe>
    </div>
</template>

<script setup lang="ts">
// 这里可以根据需要添加交互逻辑
</script>

<style scoped>
.homepage-container {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #111;
    padding: 0;
    margin: 0;
}

iframe {
    width: 100vw;
    height: 100vh;
    border: none;
    display: block;
}
</style>