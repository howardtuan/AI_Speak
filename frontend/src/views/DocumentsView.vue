<template>
  <div class="docs-page safe-area-top safe-area-bottom">
    <header class="page-header">
      <button class="btn btn-ghost btn-icon" @click="router.push('/')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      </button>
      <h1>📄 管理文件</h1>
      <div></div>
    </header>
    <!-- Upload -->
    <div class="card upload-area" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
      <input ref="fileInput" type="file" accept=".pdf,.docx" hidden @change="handleFile" />
      <p class="upload-icon">📤</p>
      <p>點擊或拖曳上傳履歷 (PDF / DOCX)</p>
      <p class="text-sm text-muted">面試練習模式會根據你的文件進行客製化提問</p>
    </div>
    <div v-if="uploading" class="uploading">上傳處理中...</div>
    <!-- Document List -->
    <div class="doc-list">
      <div v-for="d in docs" :key="d.id" class="card doc-item">
        <div class="doc-info">
          <span class="doc-icon">{{ d.file_type === 'pdf' ? '📕' : '📘' }}</span>
          <div>
            <p class="doc-name">{{ d.filename }}</p>
            <p class="text-sm text-muted">{{ d.chunk_count }} 段落 · {{ formatDate(d.uploaded_at) }}</p>
          </div>
        </div>
        <button class="btn btn-ghost" @click="deleteDoc(d.id)">🗑️</button>
      </div>
    </div>
    <div v-if="!docs.length && !uploading" class="empty">尚未上傳任何文件</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
const router = useRouter()
const docs = ref([])
const uploading = ref(false)
onMounted(fetchDocs)
async function fetchDocs() { const { data } = await api.get('/documents/'); docs.value = data }
async function handleFile(e) { const f = e.target.files[0]; if(f) await upload(f) }
async function handleDrop(e) { const f = e.dataTransfer.files[0]; if(f) await upload(f) }
async function upload(file) {
  uploading.value = true
  const fd = new FormData(); fd.append('file', file)
  try { await api.post('/documents/upload/', fd); await fetchDocs() } catch(e) { alert('上傳失敗: ' + (e.response?.data?.detail || e.message)) }
  uploading.value = false
}
async function deleteDoc(id) { if(confirm('確定刪除？')) { await api.delete(`/documents/${id}/`); await fetchDocs() } }
function formatDate(d) { return new Date(d).toLocaleDateString('zh-TW') }
</script>

<style scoped>
.docs-page{min-height:100vh;padding:1rem;max-width:600px;margin:0 auto}
.page-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem}
.page-header h1{font-size:1.25rem;font-weight:700}
.upload-area{text-align:center;padding:2rem;cursor:pointer;border:2px dashed var(--border-default);transition:all var(--transition-base)}
.upload-area:hover{border-color:var(--accent-primary);background:rgba(99,102,241,.05)}
.upload-icon{font-size:2rem;margin-bottom:.5rem}
.uploading{text-align:center;color:var(--accent-primary);padding:1rem;font-weight:500}
.doc-list{display:flex;flex-direction:column;gap:.75rem;margin-top:1rem}
.doc-item{display:flex;align-items:center;justify-content:space-between}
.doc-info{display:flex;align-items:center;gap:.75rem}
.doc-icon{font-size:1.5rem}
.doc-name{font-weight:500}
.text-sm{font-size:.8125rem}
.text-muted{color:var(--text-muted)}
.empty{text-align:center;color:var(--text-secondary);padding:3rem}
</style>
