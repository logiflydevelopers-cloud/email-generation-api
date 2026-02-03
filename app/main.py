import logging
from fastapi import FastAPI

from app.api.router import router as api_router

# ---------------- Logging (Global) ----------------
logging.basicConfig(
    level=logging.INFO,  # INFO for prod, DEBUG for local
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("email_generation")

# ---------------- FastAPI App ----------------
app = FastAPI(
    title="Email Generator API",
    version="1.0.0",
    docs_url="/docs",      # keep enabled for now
    redoc_url="/redoc",
)

# ---------------- Health Check ----------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# ---------------- API Router ----------------
app.include_router(api_router, prefix="/api/v1")


# ---------------- Startup Hook ----------------
@app.on_event("startup")
def on_startup():
    logger.info("Email Generator API started successfully")
