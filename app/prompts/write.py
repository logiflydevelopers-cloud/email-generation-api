def build_write_prompt(topic, tone, language, word_count, extra=""):
    system_instruction = (
        "You are an expert Communications Specialist. Your task is to draft a complete, high-quality email.\n"
        f"- **Language**: {language}\n"
        f"- **Tone**: {tone}\n"
        f"- **Length**: Aim for around {word_count} words, but prioritize completeness and clarity.\n"
        "- **Structure**: Include a clear Subject line and a full email body.\n"
        "- The email MUST contain at least one complete paragraph in the body.\n"
        f"{extra}\n"
    )

    user_content = (
        f"Topic details:\n{topic}\n\n"
        "Please write the full email now."
    )

    return f"{system_instruction}\n{user_content}"


# # Example Usage:
# prompt = build_write_prompt("Requesting a 2-day extension on the Q1 report", "Professional", "English", 100)
# print(prompt)