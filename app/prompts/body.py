from app.prompts.system import get_system_prompt

SHORT_EMAIL_MAX_WORDS = 120  # short email threshold


def build_body_prompt(
    topic: str,
    tone: str,
    language_code: str,
    min_words: int,
    max_words: int,
) -> str:
    is_short_email = max_words <= SHORT_EMAIL_MAX_WORDS

    length_instruction = (
        f"Write approximately {max_words} words. "
        "Do not be overly brief; expand naturally to match the requested length."
        if is_short_email
        else
        f"Length must be between {min_words} and {max_words} words."
    )

    return f"""
{get_system_prompt()}

TASK:
Write ONLY the BODY of a professional email.

STRICT RULES:
- Do NOT include subject
- Do NOT include greeting
- Do NOT include closing
- Body text ONLY

BODY REQUIREMENTS:
- Minimum 2 paragraphs
- Each paragraph must add new information
- Explain context, purpose, and details clearly
- Use full sentences only
- No bullet points or numbered lists
- {length_instruction}

Topic:
{topic}

Tone: {tone}
Language: {language_code}
""".strip()
