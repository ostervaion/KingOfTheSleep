import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') ?? null)
  const username = ref(localStorage.getItem('username') ?? null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(user, password) {
    const formData = new URLSearchParams()
    formData.append('username', user)
    formData.append('password', password)

    const response = await api.post('/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const accessToken = response.data.access_token
    if (!accessToken) throw new Error('No token received')

    token.value = accessToken
    username.value = user
    localStorage.setItem('token', accessToken)
    localStorage.setItem('username', user)
  }

  function logout() {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  const authMode = ref('default')

  function setAuthMode(newMode) {
    authMode.value = newMode
  }

  return { authMode, setAuthMode, token, username, isAuthenticated, login, logout }
})
