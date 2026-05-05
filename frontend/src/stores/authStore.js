import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!accessToken.value)

  async function login(username, password) {
    const { data } = await axios.post(`${API_URL}/auth/login/`, {
      username,
      password,
    })
    setTokens(data.access, data.refresh)
    await fetchProfile()
  }

  async function register(username, email, password) {
    const { data } = await axios.post(`${API_URL}/auth/register/`, {
      username,
      email,
      password,
    })
    setTokens(data.tokens.access, data.tokens.refresh)
    user.value = data.user
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  async function fetchProfile() {
    const { data } = await axios.get(`${API_URL}/auth/profile/`, {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    })
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
  }

  async function refreshAccessToken() {
    const { data } = await axios.post(`${API_URL}/auth/refresh/`, {
      refresh: refreshToken.value,
    })
    setTokens(data.access, data.refresh || refreshToken.value)
  }

  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function logout() {
    accessToken.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    fetchProfile,
    refreshAccessToken,
    logout,
  }
})
