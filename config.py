"""
EduGenie Configuration
Loads environment variables and exposes typed settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-3.5-flash-lite"

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set. "
        "Please add it to your .env file. See .env.example for reference."
    )
