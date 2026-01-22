def build_write_prompt(topic, tone, language, word_count, extra=""):
    if word_count <= 80:
        system_instruction = (
            "You are an email writing assistant.\n"
            f"Language: {language}\n"
            f"Tone: {tone}\n"
            "This is a SIMPLE, SHORT email.\n"
            f"The email MUST be between {max(30, word_count - 10)} and {word_count + 5} words.\n"
            f"DO NOT exceed {word_count + 5} words.\n"
            "DO NOT include:\n"
            "- Headings\n"
            "- Bullet points\n"
            "- Sections\n"
            "- Lists\n"
            "- Explanations\n"
            "- Strategies\n"
            "- Plans\n"
            "- Justifications\n"
            "Structure:\n"
            "- Subject line\n"
            "- One short greeting\n"
            "- One short body paragraph\n"
            "- Closing\n"
            f"{extra}\n"
        )

    elif word_count <= 180:
        system_instruction = (
            "You are a professional email writer.\n"
            f"Language: {language}\n"
            f"Tone: {tone}\n"
            f"Target length: {word_count} words.\n"
            "This is a NORMAL professional email.\n"
            "Avoid unnecessary sections or excessive detail.\n"
            f"{extra}\n"
        )

    else:
        system_instruction = (
            "You are an expert Communications Specialist.\n"
            f"Language: {language}\n"
            f"Tone: {tone}\n"
            f"Target length: {word_count} words.\n"
            "This is a DETAILED or MEETING-style email.\n"
            "You MAY use headings, bullet points, or sections if helpful.\n"
            f"{extra}\n"
        )

    user_content = (
        f"Topic:\n{topic}\n\n"
        "Write the email now."
    )

    return f"{system_instruction}\n{user_content}"
