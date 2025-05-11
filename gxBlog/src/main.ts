import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router'
import { debugLog } from './utils/debug'

// 设置全局调试标志
const isDebugMode = import.meta.env.MODE === 'development' || import.meta.env.VITE_DEBUG === 'true'
// 设置全局调试变量，确保与debug.ts中的逻辑一致
window.__DEBUG__ = isDebugMode
debugLog('应用启动', { env: import.meta.env.MODE, debug: window.__DEBUG__, isDebugMode })

// 只在开发环境且非调试模式下导入mock数据
if (import.meta.env.MODE === 'development' && !isDebugMode) {
    debugLog('开发环境非调试模式：导入mock数据')
    import('./mock')
    import('./mock/articleMock')
} else {
    debugLog('生产环境或调试模式：使用后端API，不导入mock数据')
}

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')