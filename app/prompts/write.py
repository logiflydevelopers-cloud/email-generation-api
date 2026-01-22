def build_write_prompt(topic, tone, language, word_count):
    """
    Constructs a strict, production-safe prompt for email generation.
    """

    min_words = int(word_count * 0.9)
    max_words = int(word_count * 1.1)

    system_instruction = (
        "SYSTEM INSTRUCTION (STRICT):\n"
        "You are an email-writing engine.\n\n"
        "You MUST follow ALL rules below. Failure to comply makes the output INVALID.\n\n"
        "RULES:\n"
        f"- Language: {language}\n"
        f"- Tone: {tone}\n"
        f"- Length: BETWEEN {min_words} AND {max_words} WORDS TOTAL (HARD LIMIT)\n"
        "- Do NOT exceed the word limit.\n"
        "- The email body MUST contain at least 3 complete sentences.\n"
        "- The email body MUST NOT be empty.\n"
        "- Do NOT omit the email body.\n"
        "- Do NOT add unrelated information.\n"
        "- Do NOT change the topic.\n\n"
        "STRUCTURE (FOLLOW EXACTLY):\n"
        "Subject: <one-line subject>\n"
        "---\n"
        "<email body>\n"
    )

    user_content = (
        f"TOPIC:\n{topic}\n\n"
        "Write the email now."
    )

    return f"{system_instruction}\n{user_content}"
