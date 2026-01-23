import os
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI

# ------------------ Setup ------------------
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1",  # can be overridden to gpt-4.1-mini / gpt-4o-mini
)

logger = logging.getLogger("email_generation")

# ------------------ Token Math ------------------
# Conservative estimates (safe across languages)
TOKENS_PER_WORD = 1.3
MAX_BODY_TOKENS = 2200

# Hard timeout to prevent hanging requests
OPENAI_TIMEOUT_SECONDS = 20


# ------------------ Core Generator ------------------
def generate_text(
    prompt: str,
    target_words: int,
    mode: str,
) -> str:
    """
    Generates text using OpenAI.

    mode:
    - "subject"
    - "body"
    - "closing"

    target_words applies mainly to BODY.
    """

    # ---------------- Token Budget ----------------
    if mode == "subject":
        max_tokens = 40
        temperature = 0.4

    elif mode == "closing":
        max_tokens = 30
        temperature = 0.4

    else:  # body
        estimated_tokens = int(target_words * TOKENS_PER_WORD)

        # Floor + cap to avoid starvation or runaway generation
        max_tokens = min(
            MAX_BODY_TOKENS,
            max(200, estimated_tokens),
        )
        temperature = 0.7

    # ---------------- Pre-call Logging ----------------
    logger.info(
        f"Calling OpenAI | mode={mode} | target_words={target_words} | "
        f"max_tokens={max_tokens} | model={MODEL_NAME}"
    )

    start_time = time.time()

    # ---------------- API Call ----------------
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_output_tokens=max_tokens,
            temperature=temperature,
            timeout=OPENAI_TIMEOUT_SECONDS,  # ⬅️ CRITICAL FIX
        )

    except Exception as e:
        logger.exception(
            f"OpenAI call failed | mode={mode} | timeout={OPENAI_TIMEOUT_SECONDS}s"
        )
        raise RuntimeError("OpenAI request failed or timed out") from e

    elapsed = round(time.time() - start_time, 2)

    # ---------------- Safety Guards ----------------
    if not response or not response.output_text:
        raise RuntimeError("OpenAI returned empty output")

    text = response.output_text.strip()

    if not text:
        raise RuntimeError("OpenAI returned blank text")

    word_count = len(text.split())

    # ---------------- Post-call Logging ----------------
    logger.info(
        f"OpenAI success | mode={mode} | words={word_count} | "
        f"tokens≈{max_tokens} | time={elapsed}s"
    )

    return text
