from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"AI Research Assistant"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}