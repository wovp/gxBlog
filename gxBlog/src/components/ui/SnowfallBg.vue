<template>
    <div ref="canvasContainerRef" :class="$props.class" aria-hidden="true"
        style="width: 100%; height: 100%; overflow: hidden;">
        <canvas ref="canvasRef" style="display: block; width: 100%; height: 100%;"></canvas>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, reactive, computed } from "vue";
import { useDevicePixelRatio } from "@vueuse/core";

type Snowflake = {
    x: number;
    y: number;
    size: number;
    alpha: number;
    dx: number; // Horizontal drift
    dy: number; // Vertical fall speed
};

type Props = {
    color?: string;
    quantity?: number;
    speed?: number;
    maxRadius?: number;
    minRadius?: number;
    class?: string;
};

const props = withDefaults(defineProps<Props>(), {
    color: "#FFF",
    quantity: 100,
    speed: 1, // Controls how fast the snowflakes fall
    maxRadius: 3, // Default max radius
    minRadius: 1, // Default min radius
    class: "",
});

const canvasRef = ref<HTMLCanvasElement | null>(null);
const canvasContainerRef = ref<HTMLDivElement | null>(null);
const context = ref<CanvasRenderingContext2D | null>(null);
const snowflakes = ref<Snowflake[]>([]);
const canvasSize = reactive<{ w: number; h: number }>({ w: 0, h: 0 });
const { pixelRatio } = useDevicePixelRatio();

const color = computed(() => {
    const hex = props.color.replace(/^#/, "").padStart(6, "0");
    const bigint = parseInt(hex, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return `${r} ${g} ${b}`;
});

onMounted(() => {
    if (canvasRef.value) {
        context.value = canvasRef.value.getContext("2d");
    }
    // 确保在组件挂载后立即初始化canvas
    initCanvas();
    // 添加一个小延迟，确保DOM完全渲染后再次调整尺寸
    setTimeout(() => {
        resizeCanvas();
    }, 100);
    animate();
    // 监听窗口大小变化
    window.addEventListener("resize", () => {
        resizeCanvas();
    });
});

onBeforeUnmount(() => {
    window.removeEventListener("resize", initCanvas);
});

function initCanvas() {
    resizeCanvas();
    createSnowflakes();
}

function resizeCanvas() {
    if (canvasContainerRef.value && canvasRef.value && context.value) {
        snowflakes.value.length = 0;
        // 获取父容器的宽高
        canvasSize.w = canvasContainerRef.value.offsetWidth || window.innerWidth;
        canvasSize.h = canvasContainerRef.value.offsetHeight || window.innerHeight;

        // 设置canvas的实际尺寸（考虑设备像素比）
        canvasRef.value.width = canvasSize.w * pixelRatio.value;
        canvasRef.value.height = canvasSize.h * pixelRatio.value;

        // 确保canvas样式尺寸与父容器一致
        canvasRef.value.style.width = '100%';
        canvasRef.value.style.height = '100%';

        // 缩放上下文以匹配设备像素比
        context.value.scale(pixelRatio.value, pixelRatio.value);

        // 重新创建雪花
        createSnowflakes();
    }
}

function createSnowflakes() {
    for (let i = 0; i < props.quantity; i++) {
        const snowflake = createSnowflake();
        snowflakes.value.push(snowflake);
    }
}

function createSnowflake(): Snowflake {
    const x = Math.random() * canvasSize.w;
    const y = Math.random() * canvasSize.h;
    const size = Math.random() * (props.maxRadius! - props.minRadius!) + props.minRadius!; // Random size between min and max radius
    const alpha = Math.random() * 0.5 + 0.5; // Opacity between 0.5 and 1
    const dx = (Math.random() - 0.5) * 0.5; // Slight horizontal drift
    const dy = Math.random() * 0.25 + props.speed; // Falling speed

    return { x, y, size, alpha, dx, dy };
}

function drawSnowflake(snowflake: Snowflake) {
    if (context.value) {
        const { x, y, size, alpha } = snowflake;
        context.value.beginPath();
        context.value.arc(x, y, size, 0, Math.PI * 2);
        context.value.fillStyle = `rgba(${color.value.split(" ").join(", ")}, ${alpha})`;
        context.value.fill();
    }
}

function animate() {
    if (context.value) {
        context.value.clearRect(0, 0, canvasSize.w, canvasSize.h);
    }

    snowflakes.value.forEach((snowflake) => {
        snowflake.x += snowflake.dx; // Drift horizontally
        snowflake.y += snowflake.dy; // Fall down

        // Reset snowflake when it moves out of the canvas
        if (snowflake.y > canvasSize.h) {
            snowflake.y = -snowflake.size; // Reset to the top
            snowflake.x = Math.random() * canvasSize.w; // Random horizontal position
        }

        drawSnowflake(snowflake);
    });

    requestAnimationFrame(animate);
}
</script>