from fastapi import APIRouter
from app.api.email import router as email_router

router = APIRouter()

# Email-related routes
router.include_router(email_router)
