# AI Speak — 英文口說練習 App

本地化 AI 英文口說練習應用。所有 AI 推論皆在本地執行，不使用任何雲端 API。

## 功能
- 💬 **純聊天模式** — 自由英文對話練習
- 💼 **面試模式** — 上傳履歷，AI 扮演面試官 (RAG)
- 🎙️ **語音對話** — 按住說話，AI 語音回覆
- 📊 **課後報告** — 評分、錯誤標註、複習總表
- ⏱️ **20 分鐘限時** — 每次對話 20 分鐘

## 技術棧
| 層級 | 技術 |
|------|------|
| 前端 | Vue.js 3 + Vite + Pinia |
| 後端 | Django 5 + DRF + Channels |
| 資料庫 | PostgreSQL 16 + pgvector |
| LLM | Ollama (Llama 3.2) |
| STT | faster-whisper (large-v3) |
| TTS | Kokoro TTS |
| 行動端 | Capacitor.js (iOS) |

## 快速開始

### 1. 啟動基礎服務
```bash
docker compose up -d
```

### 2. 後端
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver  # 或 daphne config.asgi:application
```

### 3. 前端
```bash
cd frontend
npm install
npm run dev
```

### 4. Ollama
```bash
ollama pull llama3.2
ollama serve
```

## 硬體需求
- RTX 4070S 12GB VRAM (或同等級)
- 16GB+ RAM
