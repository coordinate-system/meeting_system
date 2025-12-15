import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

/**
 * 请求拦截：自动携带 access token
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
 * 是否正在刷新 token（防止并发刷新）
 */
let isRefreshing = false
let retryQueue = []

const processQueue = (error, token = null) => {
  retryQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  retryQueue = []
}

/**
 * 响应拦截
 */
request.interceptors.response.use(
  response => {
    const res = response.data

    if (res.code !== 0) {
      alert(res.msg || '请求失败')
      return Promise.reject(res)
    }

    return res.data
  },
  async error => {
    const originalRequest = error.config

    // 后端返回 401，说明 access 过期
    if (error.response && error.response.status === 401) {
      // 已经尝试过刷新，还是失败 → 真正退出登录
      if (originalRequest._retry) {
        localStorage.clear()
        alert('登录已过期，请重新登录')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      // 标记：这个请求已经 retry 过
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        alert('未登录')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      // 正在刷新中：排队等待
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          retryQueue.push({
            resolve: token => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              resolve(request(originalRequest))
            },
            reject
          })
        })
      }

      isRefreshing = true

      try {
        // 🔥 调用后端 refresh 接口
        const res = await axios.post(
          'http://localhost:8000/api/token/refresh/',
          { refresh: refreshToken }
        )

        const newAccess = res.data.access
        localStorage.setItem('access_token', newAccess)

        processQueue(null, newAccess)

        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        return request(originalRequest)
      } catch (err) {
        processQueue(err, null)
        localStorage.clear()
        alert('登录已过期，请重新登录')
        window.location.href = '/login'
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    alert('网络错误')
    return Promise.reject(error)
  }
)

export default request
