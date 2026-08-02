import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: API_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status

    if (status === 401 || status === 403) {
      const authStore = useAuthStore()
      authStore.logout()

      if (typeof window !== 'undefined') {
        window.location.assign('/')
      }
    }

    return Promise.reject(error)
  },
)

export default api
