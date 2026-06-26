import axios from 'axios'
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

// Eloy: En el futuro la el .env tendra este formato.
// VITE_API_URL=http://localhost:8000/
// VITE_API_WS_URL=ws://localhost:8000/ws

export default api
