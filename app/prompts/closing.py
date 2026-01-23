from app.prompts.system import get_system_prompt

def build_closing_prompt(
    tone: str,
    language_code: str,
) -> str:
    return f"""
{get_system_prompt()}

TASK:
Write a professional email closing line.

Rules:
- One short line only
- Polite and professional
- Do NOT include a name
- Do NOT include punctuation beyond a comma

Tone: {tone}
Language: {language_code}
""".strip()
