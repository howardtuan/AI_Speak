import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversation = ref(null)
  const loading = ref(false)

  async function fetchConversations() {
    loading.value = true
    try {
      const { data } = await api.get('/conversations/')
      conversations.value = data
    } finally {
      loading.value = false
    }
  }

  async function createConversation(mode, title = '') {
    const { data } = await api.post('/conversations/', { mode, title })
    return data
  }

  async function getConversation(id) {
    const { data } = await api.get(`/conversations/${id}/`)
    currentConversation.value = data
    return data
  }

  async function endConversation(id) {
    await api.post(`/conversations/${id}/end/`)
  }

  async function getReport(id) {
    const { data } = await api.get(`/conversations/${id}/report/`)
    return data
  }

  return {
    conversations,
    currentConversation,
    loading,
    fetchConversations,
    createConversation,
    getConversation,
    endConversation,
    getReport,
  }
})
