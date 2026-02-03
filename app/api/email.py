from fastapi import APIRouter, HTTPException, Depends
import logging

from app.core.firebase import verify_firebase_token
from app.utils.tokens import estimate_tokens_from_text

from app.models.email import (
    WriteEmailRequest,
    ReplyEmailRequest,
    TemplateEmailRequest,
    EmailResponse,
)

from app.orchestrators.email_builder import (
    build_write_email,
    build_reply_email,
    build_template_email,
)

router = APIRouter(
    prefix="/email",
    tags=["Email"],
    dependencies=[Depends(verify_firebase_token)],
)

logger = logging.getLogger("email_generation")


# ---------------- WRITE EMAIL ----------------
@router.post("/write", response_model=EmailResponse)
def write_email(payload: WriteEmailRequest):
    try:
        email, prompt = build_write_email(payload)

        input_tokens = estimate_tokens_from_text(prompt)
        output_tokens = estimate_tokens_from_text(email)
        total_tokens = input_tokens + output_tokens

        return {
            "email": email,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }

    except RuntimeError as e:
        logger.warning(f"Write email validation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception:
        logger.exception("Write email generation crashed")
        raise HTTPException(
            status_code=500,
            detail="Internal email generation error",
        )


# ---------------- REPLY EMAIL ----------------
@router.post("/reply", response_model=EmailResponse)
def reply_email(payload: ReplyEmailRequest):
    try:
        email, prompt = build_reply_email(payload)

        input_tokens = estimate_tokens_from_text(prompt)
        output_tokens = estimate_tokens_from_text(email)
        total_tokens = input_tokens + output_tokens

        return {
            "email": email,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }

    except RuntimeError as e:
        logger.warning(f"Reply email validation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception:
        logger.exception("Reply email generation crashed")
        raise HTTPException(
            status_code=500,
            detail="Internal reply email error",
        )


# ---------------- TEMPLATE EMAIL ----------------
@router.post("/template", response_model=EmailResponse)
def template_email(payload: TemplateEmailRequest):
    try:
        email, prompt = build_template_email(payload)

        input_tokens = estimate_tokens_from_text(prompt)
        output_tokens = estimate_tokens_from_text(email)
        total_tokens = input_tokens + output_tokens

        return {
            "email": email,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }

    except RuntimeError as e:
        logger.warning(f"Template email validation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception:
        logger.exception("Template email generation crashed")
        raise HTTPException(
            status_code=500,
            detail="Internal template email error",
        )
