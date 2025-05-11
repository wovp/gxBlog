/**
 * Axios请求配置
 * 添加请求和响应拦截器，用于调试
 */

import axios from 'axios'
import { debugLog, debugError } from './debug'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const { method, url, data, params } = config
    debugLog('发起请求', { method, url, data, params })
    return config
  },
  error => {
    debugError('请求错误', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { status, statusText, data, config } = response
    debugLog('请求响应', {
      url: config.url,
      status,
      statusText,
      data: data.code === 200 ? '数据正常' : data
    })
    return response
  },
  error => {
    debugError('响应错误', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message
    })
    return Promise.reject(error)
  }
)

export default request