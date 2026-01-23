from app.prompts.system import get_system_prompt

def build_subject_prompt(
    topic: str,
    tone: str,
    language_code: str,
) -> str:
    return f"""
{get_system_prompt()}

TASK:
Write a concise and clear email subject line.

Rules:
- One line only
- Maximum 10 words
- No punctuation at the end
- Must reflect the topic accurately

Topic:
{topic}

Tone: {tone}
Language: {language_code}
""".strip()
