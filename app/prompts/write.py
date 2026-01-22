def build_write_prompt(topic, tone, language, word_count, extra=""):
    """
    Constructs the prompt logic for the AI model.
    """
    system_instruction = (
        "You are an expert Communications Specialist. Your task is to draft a high-quality email.\n"
        f"Strictly follow these rules:\n"
        f"- **Language**: {language}\n"
        f"- **Tone**: {tone}\n"
        f"- **Length**: Approximately {word_count} words.\n"
        "- **Structure**: Provide a Subject line and the Email Body.\n"
        f"{extra}\n" # This injects the date logic if present
    )
    
    user_content = (
        f"Topic details: {topic}\n\n"
        "Please write the email now."
    )
    
    return f"{system_instruction}\n{user_content}"

# # Example Usage:
# prompt = build_write_prompt("Requesting a 2-day extension on the Q1 report", "Professional", "English", 100)
# print(prompt)