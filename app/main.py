from fastapi import FastAPI
from app.routers import auth, research

app = FastAPI()

app.include_router(auth.router)
app.include_router(research.router)

@app.get("/")
def root():
    return {"message":"AI Research Assistant"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}