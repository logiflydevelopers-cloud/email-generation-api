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
from app.utils.tokens import words_to_tokens
from app.utils.dates import extract_dates
from app.utils.text import normalize_closing


router = APIRouter(prefix="/email", tags=["Email"])

MIN_OUTPUT_TOKENS = 120
MAX_OUTPUT_TOKENS = 450


# ---------------- WRITE EMAIL ----------------
@router.post("/write", response_model=EmailResponse)
def write_email(payload: WriteEmailRequest):
    start_date, end_date = extract_dates(payload.topic)

    extra = ""
    if start_date and end_date:
        extra = (
            "IMPORTANT:\n"
            f"START_DATE = {start_date}\n"
            f"END_DATE = {end_date}\n"
            "You MUST use these exact dates in subject and body.\n"
        )

    prompt = build_write_prompt(
        topic=payload.topic,
        tone=payload.tone,
        language=payload.language_code,
        word_count=payload.length_words,
        extra=extra
    )

    token_limit = max(
        MIN_OUTPUT_TOKENS,
        min(words_to_tokens(payload.length_words), MAX_OUTPUT_TOKENS)
    )

    try:
        result = generate_email(prompt, token_limit)
        result = normalize_closing(result)
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

    token_limit = max(
        MIN_OUTPUT_TOKENS,
        min(words_to_tokens(payload.length_words), MAX_OUTPUT_TOKENS)
    )

    try:
        result = generate_email(prompt, token_limit)
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

    token_limit = max(
        MIN_OUTPUT_TOKENS,
        min(words_to_tokens(payload.length_words), MAX_OUTPUT_TOKENS)
    )

    try:
        result = generate_email(prompt, token_limit)
        result = normalize_closing(result)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"LLM generation failed: {str(e)}"
        )

    return {"email": result}
