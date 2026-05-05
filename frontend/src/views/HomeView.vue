<template>
  <div class="home-page safe-area-top safe-area-bottom">
    <!-- Header -->
    <header class="home-header">
      <div class="header-left">
        <h1 class="header-title">AI Speak</h1>
        <p class="header-greeting">嗨，{{ auth.user?.display_name || auth.user?.username }} 👋</p>
      </div>
      <button class="btn btn-ghost btn-icon" @click="handleLogout" title="登出">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
        </svg>
      </button>
    </header>

    <!-- Mode Selection -->
    <section class="mode-section">
      <h2 class="section-title">開始練習</h2>

      <div class="mode-cards">
        <!-- Chat Mode -->
        <div class="mode-card" @click="startConversation('chat')">
          <div class="mode-icon mode-icon-chat">💬</div>
          <h3>純聊天</h3>
          <p>輕鬆自在地和 AI 聊天，練習日常英文對話</p>
          <span class="badge badge-primary">Free Talk</span>
        </div>

        <!-- Interview Mode -->
        <div class="mode-card" @click="startConversation('interview')">
          <div class="mode-icon mode-icon-interview">💼</div>
          <h3>面試練習</h3>
          <p>模擬英文面試，上傳履歷進行客製化練習</p>
          <span class="badge badge-warning">Mock Interview</span>
        </div>
      </div>
    </section>

    <!-- Quick Links -->
    <section class="quick-section">
      <div class="quick-links">
        <router-link to="/history" class="quick-link">
          <div class="quick-icon">📋</div>
          <span>歷史紀錄</span>
        </router-link>
        <router-link to="/documents" class="quick-link">
          <div class="quick-icon">📄</div>
          <span>管理文件</span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useChatStore } from '../stores/chatStore'

const router = useRouter()
const auth = useAuthStore()
const chat = useChatStore()

async function startConversation(mode) {
  try {
    const data = await chat.createConversation(mode)
    router.push(`/chat/${data.id}`)
  } catch {
    alert('無法建立對話，請確認後端服務是否運作中')
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.home-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  padding-top: 0.5rem;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-greeting {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: 0.125rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.mode-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mode-card {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  cursor: pointer;
  transition: all var(--transition-base);
}

.mode-card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.mode-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0.75rem 0 0.375rem;
}

.mode-card p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
}

.mode-icon {
  width: 3rem;
  height: 3rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.mode-icon-chat {
  background: rgba(99, 102, 241, 0.15);
}

.mode-icon-interview {
  background: rgba(245, 158, 11, 0.15);
}

.quick-section {
  margin-top: 2rem;
}

.quick-links {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.quick-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all var(--transition-base);
}

.quick-link:hover {
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.quick-icon {
  font-size: 1.25rem;
}
</style>
