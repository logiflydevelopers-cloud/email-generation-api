import logging
import math

logger = logging.getLogger("email_generation")

# 1 token ≈ 4 characters (rounded UP)
def estimate_tokens_from_text(text: str) -> int:
    if not text or not text.strip():
        return 0
    return math.ceil(len(text) / 4)


def calculate_token_usage(prompt: str, output: str) -> dict[str, int]:
    input_tokens = estimate_tokens_from_text(prompt)
    output_tokens = estimate_tokens_from_text(output)

    total_tokens = input_tokens + output_tokens

    logger.debug(
        f"[LLM TOKENS] "
        f"Input: {input_tokens} | "
        f"Output: {output_tokens} | "
        f"Total: {total_tokens}"
    )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }
