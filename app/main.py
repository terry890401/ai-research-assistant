from fastapi import FastAPI
from app.routers import auth, research
from contextlib import asynccontextmanager
from app.agent import build_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行
    print("啟動 AI Research Assistant...")
    app.state.agent = build_agent()
    print("Agent 初始化完成")
    
    yield  # 應用程式運行中
    
    # 關閉時執行
    print("關閉 AI Research Assistant...")

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(research.router)

@app.get("/")
def root():
    return {"message":"AI Research Assistant"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}