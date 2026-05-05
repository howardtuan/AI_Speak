<template>
  <div class="report-page safe-area-top safe-area-bottom">
    <header class="rpt-header">
      <button class="btn btn-ghost btn-icon" @click="router.push('/history')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      </button>
      <h1>📊 課後報告</h1>
      <div></div>
    </header>
    <div v-if="loading" class="loading">載入中...</div>
    <div v-else-if="report" class="rpt-content">
      <!-- Scores -->
      <div class="scores-grid">
        <div class="score-card" v-for="s in scores" :key="s.label">
          <div class="score-num" :style="{color: scoreColor(s.value)}">{{ s.value }}</div>
          <div class="score-label">{{ s.label }}</div>
        </div>
      </div>
      <!-- Summary -->
      <div class="card summary-card">
        <h3>💡 總結回饋</h3>
        <p>{{ report.summary }}</p>
      </div>
      <!-- Corrections -->
      <div v-if="report.corrections?.length" class="card">
        <h3>❌ 錯誤標註</h3>
        <div class="correction" v-for="(c,i) in report.corrections" :key="i">
          <div class="corr-row"><span class="corr-label">原文：</span><span class="corr-original">{{ c.original_text }}</span></div>
          <div class="corr-row"><span class="corr-label">修正：</span><span class="corr-corrected">{{ c.corrected_text }}</span></div>
          <div class="corr-row"><span class="badge badge-primary">{{ c.error_type }}</span></div>
          <p class="corr-explain">{{ c.explanation }}</p>
        </div>
      </div>
      <!-- Review Items -->
      <div v-if="report.review_items?.length" class="card">
        <h3>🔄 複習項目</h3>
        <div class="review-item" v-for="(r,i) in report.review_items" :key="i">
          <div class="ri-header"><span class="badge badge-success">{{ r.item_type }}</span><strong>{{ r.content }}</strong></div>
          <p class="ri-example">📝 {{ r.example_sentence }}</p>
          <p v-if="r.translation" class="ri-trans">🇹🇼 {{ r.translation }}</p>
        </div>
      </div>
    </div>
    <div v-else class="loading">報告尚未生成</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
const route = useRoute()
const router = useRouter()
const chat = useChatStore()
const report = ref(null)
const loading = ref(true)
const scores = computed(() => report.value ? [
  { label: '流暢度', value: report.value.fluency_score },
  { label: '文法', value: report.value.grammar_score },
  { label: '詞彙', value: report.value.vocabulary_score },
  { label: '總分', value: report.value.overall_score },
] : [])
function scoreColor(v) { if(v>=8) return 'var(--accent-success)'; if(v>=5) return 'var(--accent-warning)'; return 'var(--accent-danger)' }
onMounted(async () => {
  try { report.value = await chat.getReport(route.params.id) } catch {}
  loading.value = false
})
</script>

<style scoped>
.report-page{min-height:100vh;padding:1rem;max-width:600px;margin:0 auto}
.rpt-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem}
.rpt-header h1{font-size:1.25rem;font-weight:700}
.rpt-content{display:flex;flex-direction:column;gap:1rem}
.scores-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem}
.score-card{background:var(--bg-card);border:1px solid var(--border-default);border-radius:var(--radius-md);padding:1rem;text-align:center}
.score-num{font-size:2rem;font-weight:700}
.score-label{font-size:.75rem;color:var(--text-secondary);margin-top:.25rem}
.summary-card p{color:var(--text-secondary);margin-top:.5rem;line-height:1.6}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.75rem}
.correction{padding:.75rem 0;border-bottom:1px solid var(--border-default)}
.correction:last-child{border-bottom:none}
.corr-row{display:flex;align-items:center;gap:.5rem;margin-bottom:.25rem}
.corr-label{font-size:.75rem;color:var(--text-muted);min-width:2.5rem}
.corr-original{text-decoration:line-through;color:var(--accent-danger)}
.corr-corrected{color:var(--accent-success);font-weight:500}
.corr-explain{font-size:.8125rem;color:var(--text-secondary);margin-top:.25rem}
.review-item{padding:.75rem 0;border-bottom:1px solid var(--border-default)}
.review-item:last-child{border-bottom:none}
.ri-header{display:flex;align-items:center;gap:.5rem}
.ri-example{font-size:.875rem;color:var(--text-secondary);margin-top:.375rem}
.ri-trans{font-size:.8125rem;color:var(--text-muted);margin-top:.25rem}
.loading{text-align:center;color:var(--text-secondary);padding:3rem}
</style>
