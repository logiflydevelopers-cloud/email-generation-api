def build_reply_prompt(body: str, tone: str, language: str) -> str:
    return f"""
You are an expert professional email reply writer.

TASK:
Write a clear and appropriate reply to the email below.

ORIGINAL EMAIL:
\"\"\"{body}\"\"\" 

TONE:
{tone}

LANGUAGE:
{language}

STRICT RULES:
- Reply ONLY to the given email.
- Do NOT repeat the original email.
- Use any real information EXACTLY as provided.
- If information is missing, use placeholders:
  {{NAME}}, {{DATE}}, {{TIME}}, {{LOCATION}}, {{COMPANY}}
- Do NOT invent names, dates, or facts.
- Do NOT include labels such as "Body:", "Greeting:", or "Closing:".

FORMAT (STRICT):
Greeting
Reply body
Closing
Name

MANDATORY ENDING:
The reply MUST end with EXACTLY:

Best regards,
{{NAME}}
"""
