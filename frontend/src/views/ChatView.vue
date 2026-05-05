<template>
  <div class="chat-page safe-area-top safe-area-bottom">
    <header class="chat-header glass">
      <button class="btn btn-ghost btn-icon" @click="router.push('/')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      </button>
      <div class="hdr-center">
        <span class="badge" :class="mode === 'chat' ? 'badge-primary' : 'badge-warning'">
          {{ mode === 'chat' ? '💬 聊天' : '💼 面試' }}
        </span>
        <span class="timer" :class="{ 'timer-warn': remaining <= 180 }">{{ timerText }}</span>
      </div>
      <button class="btn btn-danger" style="font-size:.8rem;padding:.5rem 1rem" @click="handleEnd">結束</button>
    </header>
    <div class="msgs" ref="msgsEl">
      <div v-for="(m,i) in messages" :key="i" :class="['msg','msg-'+m.role]">
        <div class="bubble"><p>{{ m.content }}</p></div>
      </div>
      <div v-if="isProcessing" class="msg msg-assistant">
        <div class="bubble"><p>{{ aiText || '⋯' }}</p></div>
      </div>
    </div>
    <div class="controls glass">
      <div v-if="timeUp" class="time-up">⏰ 時間到！請結束對話查看報告</div>
      <div v-else class="rec-area">
        <p class="rec-hint">{{ isRecording ? '🔴 錄音中...' : '按住說話' }}</p>
        <button class="rec-btn" :class="{recording:isRecording,disabled:isProcessing}" @pointerdown="startRec" @pointerup="stopRec" @pointerleave="stopRec" :disabled="isProcessing||timeUp">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/><path d="M19 10v2a7 7 0 01-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
          <div v-if="isRecording" class="ripple"></div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
import { useAudioRecorder } from '../composables/useAudioRecorder'
import { useWebSocket } from '../composables/useWebSocket'

const route = useRoute()
const router = useRouter()
const chat = useChatStore()
const cid = route.params.id
const { isRecording, startRecording, stopRecording } = useAudioRecorder()
const { connect, sendAudio, aiText, userText, isProcessing, timeUp } = useWebSocket(cid)
const messages = ref([])
const msgsEl = ref(null)
const mode = ref('chat')
const elapsed = ref(0)
let timer = null
const remaining = computed(() => 20*60 - elapsed.value)
const timerText = computed(() => {
  const t = Math.max(0, remaining.value)
  return `${String(Math.floor(t/60)).padStart(2,'0')}:${String(t%60).padStart(2,'0')}`
})
onMounted(async () => {
  const c = await chat.getConversation(cid)
  mode.value = c.mode
  messages.value = (c.messages||[]).map(m=>({role:m.role,content:m.content}))
  connect()
  timer = setInterval(()=> elapsed.value++, 1000)
})
onUnmounted(() => { if(timer) clearInterval(timer) })
watch(userText, v => { if(v) { messages.value.push({role:'user',content:v}); scroll() } })
watch(() => isProcessing.value, p => { if(!p && aiText.value) { messages.value.push({role:'assistant',content:aiText.value}); scroll() } })
function scroll() { nextTick(()=>{ if(msgsEl.value) msgsEl.value.scrollTop = msgsEl.value.scrollHeight }) }
async function startRec() { if(!isProcessing.value && !timeUp.value) await startRecording() }
async function stopRec() { if(!isRecording.value) return; const b = await stopRecording(); if(b) sendAudio(b) }
async function handleEnd() { if(confirm('結束對話並生成報告？')) { await chat.endConversation(cid); router.push(`/report/${cid}`) } }
</script>

<style scoped>
.chat-page{display:flex;flex-direction:column;height:100vh;height:100dvh}
.chat-header{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;border-bottom:1px solid var(--border-default);flex-shrink:0}
.hdr-center{display:flex;flex-direction:column;align-items:center;gap:.25rem}
.timer{font-size:.8rem;color:var(--text-secondary);font-variant-numeric:tabular-nums}
.timer-warn{color:var(--accent-danger);font-weight:600}
.msgs{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.75rem}
.msg{display:flex;max-width:85%}
.msg-user{align-self:flex-end}
.msg-assistant{align-self:flex-start}
.bubble{padding:.75rem 1rem;border-radius:var(--radius-lg);font-size:.9375rem;line-height:1.5}
.msg-user .bubble{background:var(--accent-primary);color:#fff;border-bottom-right-radius:4px}
.msg-assistant .bubble{background:var(--bg-card);border:1px solid var(--border-default);border-bottom-left-radius:4px}
.controls{padding:1rem;border-top:1px solid var(--border-default);flex-shrink:0}
.rec-area{display:flex;flex-direction:column;align-items:center;gap:.75rem}
.rec-hint{font-size:.8rem;color:var(--text-secondary)}
.rec-btn{position:relative;width:72px;height:72px;border-radius:50%;border:none;background:var(--gradient-primary);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all var(--transition-base);touch-action:none}
.rec-btn:hover:not(.disabled){box-shadow:var(--shadow-glow-lg);transform:scale(1.05)}
.rec-btn.recording{background:var(--accent-danger);animation:pulse-glow 1.5s ease infinite}
.rec-btn.disabled{opacity:.5;cursor:not-allowed}
.ripple{position:absolute;inset:0;border-radius:50%;border:2px solid var(--accent-danger);animation:ripple 1.5s ease infinite}
.time-up{text-align:center;color:var(--accent-warning);font-weight:500;padding:.5rem}
</style>
