import logging

from app.models.email import (
    WriteEmailRequest,
    ReplyEmailRequest,
    TemplateEmailRequest,
)

from app.prompts.subject import build_subject_prompt
from app.prompts.body import build_body_prompt
from app.prompts.closing import build_closing_prompt
from app.prompts.reply import build_reply_prompt
from app.prompts.template import build_template_prompt

from app.services.openai_service import generate_text
from app.utils.text import wrap_email

logger = logging.getLogger("email_generation")

MIN_ACCEPT_RATIO = 0.6
SHORT_EMAIL_MAX_WORDS = 120


# -------------------------------------------------
# INTERNAL: regenerate body once if too short
# -------------------------------------------------
def regenerate_body(
    payload: WriteEmailRequest,
    min_words: int,
    longer: bool = False,
) -> tuple[str, str]:
    extra_instruction = ""

    if longer:
        extra_instruction = (
            "\nIMPORTANT: The email body MUST be significantly longer. "
            "Add more explanation, details, and context. "
            "Do not stop early."
        )

    body_prompt = build_body_prompt(
        topic=payload.topic,
        tone=payload.tone,
        language_code=payload.language_code,
        min_words=min_words,
        max_words=payload.length_words,
    ) + extra_instruction

    body = generate_text(
        prompt=body_prompt,
        target_words=payload.length_words,
        mode="body",
    )

    return body, body_prompt


# -------------------------------------------------
# WRITE EMAIL (Subject + Body + Closing)
# -------------------------------------------------
def build_write_email(payload: WriteEmailRequest) -> tuple[str, str]:
    target_words = payload.length_words
    min_words = int(target_words * 0.65)
    is_short_email = target_words <= SHORT_EMAIL_MAX_WORDS

    prompts_used: list[str] = []

    # ---------- SUBJECT ----------
    subject_prompt = build_subject_prompt(
        topic=payload.topic,
        tone=payload.tone,
        language_code=payload.language_code,
    )
    prompts_used.append(subject_prompt)

    subject = generate_text(
        prompt=subject_prompt,
        target_words=12,
        mode="subject",
    )

    # ---------- BODY PROMPT ----------
    body_prompt = build_body_prompt(
        topic=payload.topic,
        tone=payload.tone,
        language_code=payload.language_code,
        min_words=min_words,
        max_words=target_words,
    )

    if is_short_email:
        body_prompt += (
            "\nIMPORTANT: This is a short email. "
            f"Write approximately {target_words} words. "
            "Do not be overly brief."
        )

    prompts_used.append(body_prompt)

    body = generate_text(
        prompt=body_prompt,
        target_words=target_words,
        mode="body",
    )

    body_words = len(body.split()) if body else 0

    # ---------- VALIDATION + RETRY ----------
    if not is_short_email and body_words < min_words * MIN_ACCEPT_RATIO:
        logger.warning(
            f"Body too short ({body_words}/{min_words}), retrying once"
        )

        body, retry_prompt = regenerate_body(payload, min_words, longer=True)
        prompts_used.append(retry_prompt)

        body_words = len(body.split()) if body else 0
        if body_words < min_words * MIN_ACCEPT_RATIO:
            raise RuntimeError(
                f"Generated body too short after retry ({body_words}/{min_words})"
            )

    # ---------- CLOSING ----------
    closing_prompt = build_closing_prompt(
        tone=payload.tone,
        language_code=payload.language_code,
    )
    prompts_used.append(closing_prompt)

    closing = generate_text(
        prompt=closing_prompt,
        target_words=15,
        mode="closing",
    )

    # ---------- WRAP ----------
    email = wrap_email(
        subject=subject,
        body=body,
        closing=closing,
    )

    # 🔑 THIS is what the model actually saw
    full_prompt = "\n\n".join(prompts_used)

    return email, full_prompt


# -------------------------------------------------
# REPLY EMAIL
# -------------------------------------------------
def build_reply_email(payload: ReplyEmailRequest) -> tuple[str, str]:
    prompt = build_reply_prompt(
        body=payload.body,
        tone=payload.tone,
        language_code=payload.language_code,
        max_words=payload.length_words,
    )

    email = generate_text(
        prompt=prompt,
        target_words=payload.length_words,
        mode="body",
    )

    if not email or not email.strip():
        raise RuntimeError("Empty reply email generated")

    return email, prompt


# -------------------------------------------------
# TEMPLATE EMAIL
# -------------------------------------------------
def build_template_email(payload: TemplateEmailRequest) -> tuple[str, str]:
    prompt = build_template_prompt(
        body=payload.body,
        tone=payload.tone,
        language_code=payload.language_code,
        max_words=payload.length_words,
    )

    email = generate_text(
        prompt=prompt,
        target_words=payload.length_words,
        mode="body",
    )

    if not email or not email.strip():
        raise RuntimeError("Empty template email generated")

    return email, prompt
