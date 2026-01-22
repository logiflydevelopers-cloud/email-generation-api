from fastapi import APIRouter, HTTPException

from app.models.email import (
    WriteEmailRequest,
    ReplyEmailRequest,
    EmailResponse,
)

from app.prompts.write import build_write_prompt
from app.prompts.reply import build_reply_prompt
from app.prompts.template import build_template_prompt

from app.services.llm_service import generate_email
from app.utils.dates import extract_dates
from app.utils.text import normalize_closing


router = APIRouter(prefix="/email", tags=["Email"])


# ---------------- WRITE EMAIL ----------------
@router.post("/write", response_model=EmailResponse)
def write_email(payload: WriteEmailRequest):
    prompt = build_write_prompt(
        topic=payload.topic,
        tone=payload.tone,
        language=payload.language_code,
        word_count=payload.length_words
    )

    try:
        result = generate_email(prompt)

        # ✅ Guard: empty or whitespace-only output
        if not result or not result.strip():
            raise HTTPException(
                status_code=502,
                detail="LLM returned empty response"
            )

        # ✅ Normalize sign-off
        result = normalize_closing(result)

        # ✅ HARD word-count enforcement (critical)
        words = result.split()
        max_words = int(payload.length_words * 1.1)

        if len(words) > max_words:
            result = " ".join(words[:payload.length_words])

    except HTTPException:
        raise  # rethrow intentional HTTP errors

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {str(e)}"
        )

    return {"email": result}



# ---------------- REPLY EMAIL ----------------
@router.post("/reply", response_model=EmailResponse)
def reply_email(payload: ReplyEmailRequest):
    prompt = build_reply_prompt(
        body=payload.body,
        tone=payload.tone,
        language=payload.language_code
    )

    try:
        result = generate_email(prompt)   # 🔥 no token limit
        result = normalize_closing(result)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {str(e)}"
        )

    return {"email": result}


# ---------------- EMAIL FROM TEMPLATE ----------------
@router.post("/template", response_model=EmailResponse)
def template_email(payload: ReplyEmailRequest):
    prompt = build_template_prompt(
        body=payload.body,
        tone=payload.tone,
        language=payload.language_code
    )

    try:
        result = generate_email(prompt)   # 🔥 no token limit
        result = normalize_closing(result)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {str(e)}"
        )

    return {"email": result}
