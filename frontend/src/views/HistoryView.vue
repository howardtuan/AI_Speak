<template>
  <div class="history-page safe-area-top safe-area-bottom">
    <header class="page-header">
      <button class="btn btn-ghost btn-icon" @click="router.push('/')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      </button>
      <h1>📋 歷史紀錄</h1>
      <div></div>
    </header>
    <div v-if="loading" class="loading">載入中...</div>
    <div v-else-if="conversations.length === 0" class="empty">尚無對話紀錄</div>
    <div v-else class="conv-list">
      <div v-for="c in conversations" :key="c.id" class="card conv-item" @click="goTo(c)">
        <div class="conv-top">
          <span class="badge" :class="c.mode==='chat'?'badge-primary':'badge-warning'">{{ c.mode==='chat'?'💬 聊天':'💼 面試' }}</span>
          <span class="conv-date">{{ formatDate(c.started_at) }}</span>
        </div>
        <p class="conv-title">{{ c.title || `對話 #${c.id}` }}</p>
        <div class="conv-bottom">
          <span class="text-muted">{{ c.message_count || 0 }} 則訊息</span>
          <span v-if="c.has_report" class="badge badge-success">已有報告</span>
          <span v-else-if="!c.is_active" class="text-muted">已結束</span>
          <span v-else class="badge badge-primary">進行中</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
const router = useRouter()
const chat = useChatStore()
const conversations = ref([])
const loading = ref(true)
onMounted(async () => { await chat.fetchConversations(); conversations.value = chat.conversations; loading.value = false })
function formatDate(d) { return new Date(d).toLocaleDateString('zh-TW', { month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' }) }
function goTo(c) { if(c.has_report || !c.is_active) router.push(`/report/${c.id}`); else router.push(`/chat/${c.id}`) }
</script>

<style scoped>
.history-page{min-height:100vh;padding:1rem;max-width:600px;margin:0 auto}
.page-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem}
.page-header h1{font-size:1.25rem;font-weight:700}
.conv-list{display:flex;flex-direction:column;gap:.75rem}
.conv-item{cursor:pointer}
.conv-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:.5rem}
.conv-date{font-size:.75rem;color:var(--text-muted)}
.conv-title{font-weight:500;margin-bottom:.5rem}
.conv-bottom{display:flex;align-items:center;gap:.75rem;font-size:.8125rem}
.text-muted{color:var(--text-muted)}
.loading,.empty{text-align:center;color:var(--text-secondary);padding:3rem}
</style>
