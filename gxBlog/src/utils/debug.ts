/**
 * 调试工具函数
 * 只在开发环境下输出调试信息
 */

// 为TypeScript声明全局调试标志
declare global {
  interface Window {
    __DEBUG__?: boolean
  }
}

// 判断是否为开发环境或启用了调试模式
// 使用 import.meta.env 替代 process.env 来判断环境
const isDev = import.meta.env.DEV
const isDebugMode = import.meta.env.MODE === 'development' || import.meta.env.VITE_DEBUG === 'true'

// 判断是否启用调试
const isDebugEnabled = () => {
  // 如果明确设置了VITE_DEBUG=true，则启用调试
  // 否则在开发环境下，除非明确设置了window.__DEBUG__=false，否则启用调试
  return isDebugMode || (isDev && (window.__DEBUG__ !== false))
}

/**
 * 调试日志输出
 * @param message 日志消息
 * @param data 相关数据
 */
export const debugLog = (message: string, data?: any) => {
  if (isDebugEnabled()) {
    console.log(`[DEBUG] ${message}`, data || '')
  }
}

/**
 * 调试警告输出
 * @param message 警告消息
 * @param data 相关数据
 */
export const debugWarn = (message: string, data?: any) => {
  if (isDebugEnabled()) {
    console.warn(`[DEBUG WARNING] ${message}`, data || '')
  }
}

/**
 * 调试错误输出
 * @param message 错误消息
 * @param error 错误对象
 */
export const debugError = (message: string, error?: any) => {
  if (isDebugEnabled()) {
    console.error(`[DEBUG ERROR] ${message}`, error || '')
  }
}

/**
 * 调试计时开始
 * @param label 计时标签
 */
export const debugTimeStart = (label: string) => {
  if (isDebugEnabled()) {
    console.time(`[DEBUG TIME] ${label}`)
  }
}

/**
 * 调试计时结束
 * @param label 计时标签
 */
export const debugTimeEnd = (label: string) => {
  if (isDebugEnabled()) {
    console.timeEnd(`[DEBUG TIME] ${label}`)
  }
}