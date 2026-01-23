from app.prompts.system import get_system_prompt


def build_template_prompt(
    body: str,
    tone: str,
    language_code: str,
    max_words: int,
) -> str:
    return f"""
{get_system_prompt()}

TASK:
Modify the EXISTING email template below according to the requested tone and length.

STRICT RULES:
- Preserve the ORIGINAL STRUCTURE of the template.
- Do NOT add a subject line if one does not already exist.
- Do NOT remove or rename placeholders.
- Do NOT change the greeting style unless necessary.
- Do NOT invent new sections.
- Improve wording, tone, and flow ONLY.
- Use full sentences only.
- No bullet points or numbered lists.
- Do NOT explain what you changed.

LENGTH:
- The modified template should be approximately {max_words} words.

EXISTING TEMPLATE:
\"\"\"
{body}
\"\"\"

Tone: {tone}
Language: {language_code}
""".strip()
