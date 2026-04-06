# AI Research Assistant

一個基於 LangGraph + Tool Calling 的 AI 自動研究助手，輸入主題後自動搜尋網路資料，產生結構化研究報告。

**Live Demo API**: https://ai-research-assistant-production-9f6e.up.railway.app

**前端**：本機執行 Streamlit（`streamlit run streamlit_app.py`）

## 功能

- **自動研究**：輸入主題，Agent 自動搜尋相關資料並產生報告
- **Tool Calling**：AI 自主決定搜尋關鍵字和搜尋時機
- **LangGraph Agent**：conditional edge 讓 AI 判斷資料是否足夠，不足時自動重新搜尋
- **結構化報告**：Pydantic 驗證輸出格式，確保報告包含標題、摘要、重點、結論
- **非同步任務**：研究任務背景執行，立刻回傳任務 ID，不需等待
- **JWT 認證**：註冊、登入、token 驗證
- **歷史查詢**：查詢所有研究任務和結果
- **Streamlit UI**：直覺的前端介面，支援登入和研究任務管理
- **健康檢查**：`/health` API 確認服務狀態

## 技術架構

| 類別 | 技術 |
|------|------|
| 後端框架 | FastAPI |
| 資料庫 | PostgreSQL + SQLAlchemy ORM |
| 資料庫遷移 | Alembic |
| Agent 框架 | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| 搜尋工具 | Tavily API |
| 認證 | JWT (python-jose) |
| 密碼加密 | bcrypt (passlib) |
| 資料驗證 | Pydantic v2 |
| 前端 | Streamlit |
| 測試 | pytest + FastAPI TestClient |
| CI/CD | GitHub Actions |
| 部署 | Docker + Railway |

## 系統架構

```
用戶輸入主題
    │
    ▼
FastAPI（背景任務）
    │
    ▼
LangGraph Agent
    │
    ├── agent node → AI 決定搜尋關鍵字（Tool Calling）
    │       │
    │       ▼
    ├── tools node → Tavily 執行搜尋
    │       │
    │       ▼
    ├── agent node → 判斷資料夠不夠（conditional edge）
    │       │
    │       ▼
    └── report node → Pydantic 驗證，產生結構化 JSON 報告
    │
    ▼
PostgreSQL（儲存任務和報告）
```

## 專案結構

```
ai-research-assistant/
├── app/
│   ├── main.py          # FastAPI 入口、Lifespan、Agent 初始化
│   ├── database.py      # 資料庫連線設定
│   ├── models.py        # SQLAlchemy 資料表
│   ├── schemas.py       # Pydantic 資料格式
│   ├── dependencies.py  # JWT 驗證
│   ├── agent.py         # LangGraph Agent、Tool Calling、結構化輸出
│   └── routers/
│       ├── auth.py      # 認證 API
│       └── research.py  # 研究任務 API
├── alembic/             # 資料庫遷移檔案
├── tests/               # pytest 測試
│   ├── test_agent.py
│   ├── test_auth.py
│   ├── test_health.py
│   └── test_research.py
├── .github/workflows/   # CI/CD
│   └── ci.yml
├── streamlit_app.py     # Streamlit 前端
├── Dockerfile
├── .env.example
└── requirements.txt
```

## 安裝步驟

### 1. 建立虛擬環境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 安裝套件

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

複製 `.env.example` 為 `.env` 並填入實際的值：

```bash
cp .env.example .env
```

### 4. 建立資料庫

```sql
CREATE DATABASE ai_research;
```

### 5. 執行資料庫遷移

```bash
alembic upgrade head
```

### 6. 啟動 FastAPI

```bash
uvicorn app.main:app --reload
```

### 7. 啟動 Streamlit（另一個 terminal）

```bash
streamlit run streamlit_app.py
```

## API 路由

### 認證
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/auth/register` | 註冊 |
| POST | `/auth/login` | 登入，回傳 JWT token |
| GET | `/auth/me` | 取得目前用戶 |

### 研究任務
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/research/` | 建立研究任務（背景執行） |
| GET | `/research/` | 取得所有研究任務 |
| GET | `/research/{id}` | 取得單一研究任務和報告 |

## 報告格式

```json
{
    "title": "報告標題",
    "summary": "摘要（100字內）",
    "key_points": ["重點1", "重點2", "重點3"],
    "conclusion": "結論"
}
```

## 測試

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t ai-research-assistant .
docker run -p 8000:8000 --env-file .env ai-research-assistant
```
