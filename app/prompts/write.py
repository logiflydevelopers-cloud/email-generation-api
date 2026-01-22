def build_write_prompt(topic, tone, language, word_count, extra=""):
    # Decide role & structure based on length
    if word_count <= 80:
        role = "You are an email writing assistant."
        structure_rules = (
            "- Keep the email short, simple, and human.\n"
            "- Do NOT include bullet points, headings, sections, or lists.\n"
        )
    elif word_count <= 180:
        role = "You are a professional email writer."
        structure_rules = (
            "- Write a clear professional email.\n"
            "- Avoid unnecessary sections or lists unless clearly helpful.\n"
        )
    else:
        role = "You are an expert Communications Specialist."
        structure_rules = (
            "- This is a detailed or meeting-style email.\n"
            "- You MAY use headings, bullet points, or sections where appropriate.\n"
        )

    system_instruction = (
        f"{role}\n"
        f"- Language: {language}\n"
        f"- Tone: {tone}\n"
        f"- The email MUST be between {max(30, word_count - 10)} and {word_count + 10} words.\n"
        f"- DO NOT exceed {word_count + 10} words.\n"
        "- Always include a subject line.\n"
        f"{structure_rules}"
        f"{extra}\n"
    )

    user_content = (
        f"Topic:\n{topic}\n\n"
        "Write the email now."
    )

    return f"{system_instruction}\n{user_content}"
