import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username'))
  const tutorial = ref(localStorage.getItem('tutorial') === 'true')

  const isAuthenticated = computed(() => Boolean(token.value))

  async function login(user, password) {
    const formData = new URLSearchParams()
    formData.append('username', user)
    formData.append('password', password)

    const response = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    const accessToken = response.data.access_token

    if (!accessToken) {
      throw new Error('No token received')
    }

    token.value = accessToken
    username.value = user

    localStorage.setItem('token', accessToken)
    localStorage.setItem('username', user)
  }

  function logout() {
    token.value = null
    username.value = null
    tutorial.value = false

    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('tutorial')
  }

  function setTutorial() {
    tutorial.value = true
    localStorage.setItem('tutorial', 'true')
  }

  function removeTutorial() {
    tutorial.value = false
    localStorage.removeItem('tutorial')
  }

  const authMode = ref('default')

  function setAuthMode(newMode) {
    authMode.value = newMode
  }

  return {
    authMode,
    token,
    username,
    tutorial,
    isAuthenticated,
    setAuthMode,
    setTutorial,
    removeTutorial,
    login,
    logout,
  }
})
