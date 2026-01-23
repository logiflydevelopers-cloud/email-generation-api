import logging

logger = logging.getLogger("email_generation")

# Safe token estimation
def estimate_tokens_from_chars(char_count: int) -> int:
    return max(1, int(char_count / 4))


def log_llm_usage(prompt: str, output: str, model: str = "flash") -> None:
    prompt_chars = len(prompt)
    output_chars = len(output)

    prompt_tokens = estimate_tokens_from_chars(prompt_chars)
    output_tokens = estimate_tokens_from_chars(output_chars)

    logger.debug(
        f"[LLM USAGE] "
        f"Prompt: {prompt_chars} chars (~{prompt_tokens} tokens) | "
        f"Output: {output_chars} chars (~{output_tokens} tokens) | "
        f"Total: ~{prompt_tokens + output_tokens} tokens"
    )
