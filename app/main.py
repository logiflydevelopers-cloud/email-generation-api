from fastapi import FastAPI
from app.api.router import router as api_router
import logging

app = FastAPI(
    title="Email Generator API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------- Health Check ----------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# ---------------- API Router ----------------
app.include_router(api_router, prefix="/api/v1")


# ---------------- Logging Startup ----------------
@app.on_event("startup")
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # change to DEBUG for local/dev
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
