import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-3-flash-preview"  # or gemini-pro

def generate_email(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
        }
    )

    if not response.candidates:
        raise RuntimeError("Gemini returned no candidates")

    candidate = response.candidates[0]

    if not candidate.content or not candidate.content.parts:
        raise RuntimeError(
            f"Gemini returned empty content (finish_reason={candidate.finish_reason})"
        )

    text_parts = [
        part.text for part in candidate.content.parts if hasattr(part, "text")
    ]

    if not text_parts:
        raise RuntimeError("Gemini returned no text output")

    return "\n".join(text_parts).strip()
