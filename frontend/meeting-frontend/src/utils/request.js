import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

/**
 * 请求拦截器：自动携带 JWT
 */
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

/**
 * 响应拦截：统一处理后端约定格式
 */
request.interceptors.response.use(
  response => {
    const res = response.data

    if (res.code !== 0) {
      alert(res.msg || '请求失败')
      return Promise.reject(res)
    }

    // 保留你原来的设计：只把 data 给页面
    return res.data
  },
  error => {
    alert('网络错误，请检查后端是否启动')
    return Promise.reject(error)
  }
)

export default request
