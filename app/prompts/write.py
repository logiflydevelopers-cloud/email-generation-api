def build_write_prompt(topic, tone, language, word_count):
    prompt = f"""
Role:
You are an expert Executive Assistant and Communications Specialist.

Task:
Write a professional email.

STRICT REQUIREMENTS (DO NOT IGNORE):
- The email MUST be written in {language}.
- The tone MUST be strictly {tone}.
- The total length MUST be between {int(word_count * 0.9)} and {int(word_count * 1.1)} words.
- DO NOT exceed this word limit.
- If you cannot comply, shorten the email.

Content Rules:
- Include a Subject line.
- Use '---' as a separator.
- Use the exact dates mentioned in the topic if any.
- Do NOT add unnecessary details.
- Do NOT include explanations or meta text.

Output Format (follow exactly):

Subject: <subject text>
---
<email body>
"""
    return prompt
