def build_template_prompt(body: str, tone: str, language: str) -> str:
    return f"""
You are an expert email template designer.

TASK:
You are given an existing email or draft.
You MUST rewrite it to create an improved version.

STRICT RULES:
- DO NOT copy sentences verbatim.
- DO NOT return the same wording.
- Rewrite and improve clarity, tone, and flow.
- Preserve the original intent and structure.
- If real values (names, dates, places, companies) are present, use them EXACTLY.
- If information is missing, keep placeholders.
- Do NOT invent facts or details.
- Do NOT include labels such as "Body:", "Greeting:", or "Closing:".

ORIGINAL CONTENT:
\"\"\"{body}\"\"\" 

TONE:
{tone}

LANGUAGE:
{language}

FORMAT (STRICT):
Greeting
Body paragraphs
Closing
Name

MANDATORY ENDING:
The email MUST end with EXACTLY:

Best regards,
{{NAME}}
"""
