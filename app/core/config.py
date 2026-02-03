import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing")
