import { ref } from 'vue'

export function useAudioRecorder() {
  const isRecording = ref(false)
  let mediaRecorder = null
  let chunks = []

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        sampleRate: 16000,
        echoCancellation: true,
        noiseSuppression: true,
      },
    })

    mediaRecorder = new MediaRecorder(stream, {
      mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm',
    })

    chunks = []
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data)
    }
    mediaRecorder.start()
    isRecording.value = true
  }

  function stopRecording() {
    return new Promise((resolve) => {
      if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        resolve(null)
        return
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        // Stop all tracks to release microphone
        mediaRecorder.stream.getTracks().forEach((t) => t.stop())
        isRecording.value = false
        resolve(blob)
      }
      mediaRecorder.stop()
    })
  }

  return { isRecording, startRecording, stopRecording }
}
