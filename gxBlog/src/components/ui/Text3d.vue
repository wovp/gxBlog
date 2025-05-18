<template>
    <div :class="cn('text-3d-wrapper flex items-center justify-center', props.class)">
        <div :class="cn('text-3d', animate ? 'animate-text-3d' : '', size)">
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, type HTMLAttributes } from "vue";
import { cn } from "../../lib/utils";

interface Props {
    textColor?: string;
    letterSpacing?: number;
    strokeColor?: string;
    shadowColor?: string;
    strokeSize?: number;
    shadow1Size?: number;
    shadow2Size?: number;
    class?: HTMLAttributes["class"];
    animate?: boolean;
    animationDuration?: number;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    glowColor?: string;
    glowIntensity?: number;
    fontWeight?: number;
}

const props = withDefaults(defineProps<Props>(), {
    textColor: "white",
    letterSpacing: -0.1,
    strokeColor: "#000",
    shadowColor: "#4a6bdf",
    strokeSize: 12,
    shadow1Size: 5,
    shadow2Size: 8,
    animate: true,
    animationDuration: 3000,
    size: 'md',
    glowColor: "rgba(74, 107, 223, 0.6)",
    glowIntensity: 15,
    fontWeight: 800,
});

const letterSpacingInCh = computed(() => {
    return `${props.letterSpacing}ch`;
});

const strokeSizeInPx = computed(() => {
    return `${props.strokeSize}px`;
});

const shadow1SizeInPx = computed(() => {
    return `${props.shadow1Size}px`;
});

const shadow2SizeInPx = computed(() => {
    return `${props.shadow2Size}px`;
});

const animationDurationInMs = computed(() => {
    return `${props.animationDuration}ms`;
});

const glowSizeInPx = computed(() => {
    return `${props.glowIntensity}px`;
});

const fontWeightValue = computed(() => {
    return props.fontWeight;
});
</script>

<style scoped>
.text-3d-wrapper {
    position: relative;
    padding: 0.5rem 1rem;
    overflow: visible;
}

.text-3d {
    position: relative;
    display: inline-block;
    font-weight: v-bind(fontWeightValue);
    paint-order: stroke fill;
    letter-spacing: v-bind(letterSpacingInCh);
    -webkit-text-stroke: v-bind(strokeSizeInPx) v-bind(strokeColor);
    text-shadow:
        v-bind(shadow1SizeInPx) v-bind(shadow1SizeInPx) 0px v-bind(strokeColor),
        v-bind(shadow2SizeInPx) v-bind(shadow2SizeInPx) 0px v-bind(shadowColor);
    color: v-bind(textColor);
    filter: drop-shadow(0 0 v-bind(glowSizeInPx) v-bind(glowColor));
    transition: all 0.3s ease;
}

.text-3d::before {
    content: '';
    position: absolute;
    top: -10%;
    left: -5%;
    width: 110%;
    height: 120%;
    background: linear-gradient(45deg, transparent 40%, rgba(255, 255, 255, 0.1) 45%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 55%, transparent 60%);
    background-size: 200% 200%;
    animation: shine 4s linear infinite;
    pointer-events: none;
    z-index: 1;
}

.text-3d:hover {
    transform: translateY(-2px);
    filter: drop-shadow(0 0 calc(v-bind(glowSizeInPx) * 1.5) v-bind(glowColor));
}

.animate-text-3d {
    animation: float v-bind(animationDurationInMs) ease-in-out infinite;
    animation-timing-function: ease-in-out;
    transform-origin: center;
}

/* 尺寸变体 */
.sm {
    font-size: 1.25rem;
}

.md {
    font-size: 2rem;
}

.lg {
    font-size: 3rem;
}

.xl {
    font-size: 4rem;
}

@keyframes float {
    0% {
        transform: translateY(0) rotate(0deg);
    }

    25% {
        transform: translateY(-5px) rotate(1deg);
    }

    50% {
        transform: translateY(0) rotate(0deg);
    }

    75% {
        transform: translateY(5px) rotate(-1deg);
    }

    100% {
        transform: translateY(0) rotate(0deg);
    }
}

@keyframes shine {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .lg {
        font-size: 2.5rem;
    }

    .xl {
        font-size: 3rem;
    }
}

@media (max-width: 480px) {
    .md {
        font-size: 1.5rem;
    }

    .lg {
        font-size: 2rem;
    }

    .xl {
        font-size: 2.5rem;
    }
}
</style>