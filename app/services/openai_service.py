import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4o-mini"

def generate_email(prompt: str, max_tokens: int) -> str:
    """
    Sends a prompt to OpenAI and returns generated email text.
    """
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        max_output_tokens=max_tokens
    )

    return response.output_text
