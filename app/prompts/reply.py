from app.prompts.system import get_system_prompt


def build_reply_prompt(
    body: str,
    tone: str,
    language_code: str,
    max_words: int,
) -> str:
    return f"""
{get_system_prompt()}

TASK:
Write a professional email REPLY to the message below.

STRICT RULES:
- Write the FULL reply email (greeting + body + closing).
- Respond appropriately to the content provided.
- Be clear, polite, and relevant.
- Use full sentences only.
- No bullet points or numbered lists.
- Do NOT include explanations or commentary.

LENGTH:
- The full reply should be approximately {max_words} words.

ORIGINAL EMAIL:
\"\"\"
{body}
\"\"\"

Tone: {tone}
Language: {language_code}
""".strip()
