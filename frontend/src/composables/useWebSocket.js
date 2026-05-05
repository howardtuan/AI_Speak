import { ref, onUnmounted } from 'vue'

export function useWebSocket(conversationId) {
  const ws = ref(null)
  const aiText = ref('')
  const userText = ref('')
  const isConnected = ref(false)
  const isProcessing = ref(false)
  const timeUp = ref(false)

  const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

  function connect() {
    ws.value = new WebSocket(`${WS_URL}/ws/chat/${conversationId}/`)

    ws.value.onopen = () => {
      isConnected.value = true
    }

    ws.value.onclose = () => {
      isConnected.value = false
    }

    ws.value.onmessage = (event) => {
      if (typeof event.data === 'string') {
        const data = JSON.parse(event.data)

        switch (data.type) {
          case 'connected':
            break
          case 'user_text':
            userText.value = data.text
            isProcessing.value = true
            break
          case 'ai_token':
            aiText.value += data.token
            break
          case 'ai_complete':
            isProcessing.value = false
            break
          case 'time_up':
            timeUp.value = true
            break
        }
      } else {
        // Binary data = TTS audio
        const blob = new Blob([event.data], { type: 'audio/wav' })
        const url = URL.createObjectURL(blob)
        const audio = new Audio(url)
        audio.play().catch(() => {})
        audio.onended = () => URL.revokeObjectURL(url)
      }
    }
  }

  function sendAudio(blob) {
    if (ws.value?.readyState === WebSocket.OPEN) {
      aiText.value = ''
      userText.value = ''
      ws.value.send(blob)
    }
  }

  function sendConfig(mode) {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify({ type: 'config', mode }))
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    connect,
    sendAudio,
    sendConfig,
    disconnect,
    aiText,
    userText,
    isConnected,
    isProcessing,
    timeUp,
  }
}
