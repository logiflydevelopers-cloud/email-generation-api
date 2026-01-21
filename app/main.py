from fastapi import FastAPI
from app.api.router import router as api_router

app = FastAPI(title="Email Generator API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")
