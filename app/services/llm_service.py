import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-3-flash-preview"

def generate_email(prompt: str, length_words: int) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    max_output_tokens = max(200,int(length_words * 1.6) )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,          # lower = more instruction-following
            "max_output_tokens": 200,    # 🔥 REQUIRED (prevents empty output)
            "top_p": 0.9,
            "top_k": 40
        }
    )

    # 🔒 Guard: no candidates at all
    if not response or not response.candidates:
        raise RuntimeError("Gemini returned no candidates")

    candidate = response.candidates[0]

    # 🔒 Guard: empty content
    if not candidate.content or not candidate.content.parts:
        raise RuntimeError(
            f"Gemini returned empty content (finish_reason={candidate.finish_reason})"
        )

    # 🔒 Extract text safely
    text_parts = [
        part.text.strip()
        for part in candidate.content.parts
        if hasattr(part, "text") and part.text and part.text.strip()
    ]

    if not text_parts:
        raise RuntimeError(
            f"Gemini returned no usable text (finish_reason={candidate.finish_reason})"
        )

    return "\n".join(text_parts)
