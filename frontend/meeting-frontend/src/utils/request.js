import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:8000', // Django 默认端口
  timeout: 5000
})

// 响应拦截：统一处理后端约定格式
request.interceptors.response.use(
  response => {
    const res = response.data

    if (res.code !== 0) {
      alert(res.msg || '请求失败')
      return Promise.reject(res)
    }

    // 只把 data 给页面
    return res.data
  },
  error => {
    alert('网络错误，请检查后端是否启动')
    return Promise.reject(error)
  }
)

export default request
