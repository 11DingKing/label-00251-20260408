import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    // 登录/注册接口的 401 不跳转，让页面自己处理错误
    const isAuthApi = err.config?.url?.startsWith('/auth/')
    if (err.response?.status === 401 && !isAuthApi) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
