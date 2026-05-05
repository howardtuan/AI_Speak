<template>
  <div class="login-page safe-area-top safe-area-bottom">
    <div class="login-bg">
      <div class="login-orb login-orb-1"></div>
      <div class="login-orb login-orb-2"></div>
    </div>

    <div class="login-container animate-slide-up">
      <!-- Logo -->
      <div class="login-logo">
        <div class="logo-icon">🎙️</div>
        <h1 class="logo-title">AI Speak</h1>
        <p class="logo-subtitle">練習英文口說，隨時隨地</p>
      </div>

      <!-- Form -->
      <div class="login-card glass">
        <div class="tab-switcher">
          <button
            :class="['tab-btn', { active: tab === 'login' }]"
            @click="tab = 'login'"
          >登入</button>
          <button
            :class="['tab-btn', { active: tab === 'register' }]"
            @click="tab = 'register'"
          >註冊</button>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="username">使用者名稱</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="input"
              placeholder="輸入使用者名稱"
              required
            />
          </div>

          <div v-if="tab === 'register'" class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="input"
              placeholder="your@email.com"
            />
          </div>

          <div class="form-group">
            <label for="password">密碼</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="input"
              placeholder="輸入密碼"
              required
            />
          </div>

          <p v-if="error" class="error-text">{{ error }}</p>

          <button
            type="submit"
            class="btn btn-primary btn-lg"
            :disabled="loading"
            style="width: 100%"
          >
            <span v-if="loading" class="spinner"></span>
            {{ tab === 'login' ? '登入' : '註冊' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const auth = useAuthStore()

const tab = ref('login')
const loading = ref(false)
const error = ref('')
const form = reactive({ username: '', email: '', password: '' })

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    if (tab.value === 'login') {
      await auth.login(form.username, form.password)
    } else {
      await auth.register(form.username, form.email, form.password)
    }
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '操作失敗，請再試一次'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
}

.login-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.login-orb-1 {
  width: 400px;
  height: 400px;
  background: var(--accent-primary);
  top: -100px;
  right: -100px;
}

.login-orb-2 {
  width: 300px;
  height: 300px;
  background: var(--accent-secondary);
  bottom: -50px;
  left: -50px;
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 1.5rem;
}

.login-logo {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
}

.logo-title {
  font-size: 2rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-subtitle {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  margin-top: 0.25rem;
}

.login-card {
  border-radius: var(--radius-xl);
  padding: 2rem;
}

.tab-switcher {
  display: flex;
  background: var(--bg-input);
  border-radius: var(--radius-md);
  padding: 4px;
  margin-bottom: 1.5rem;
}

.tab-btn {
  flex: 1;
  padding: 0.625rem;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font-family);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn.active {
  background: var(--accent-primary);
  color: white;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-group label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.error-text {
  color: var(--accent-danger);
  font-size: 0.875rem;
  text-align: center;
}

.spinner {
  display: inline-block;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
</style>
