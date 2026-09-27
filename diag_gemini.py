"""
Safe Gemini diagnostic — never prints the API key.
Run: python diag_gemini.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY", "")
print(f"[1] API key present : {bool(key)}")
print(f"[2] API key length  : {len(key)}")
print(f"[3] Key prefix (4)  : {key[:4]!r}")

from google import genai  # noqa: E402

try:
    client = genai.Client(api_key=key)
    print("[4] Client init     : OK")
except Exception as exc:
    safe = str(exc).replace(key, "[REDACTED]") if key else str(exc)
    print(f"[4] Client init     : FAILED -- {type(exc).__name__}: {safe}")
    raise SystemExit(1)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with exactly: diagnostic OK",
    )
    text = response.text or ""
    print(f"[5] API call        : OK -- response length {len(text)} chars")
    print(f"[6] Preview         : {text[:80]!r}")
except Exception as exc:
    safe = str(exc).replace(key, "[REDACTED]") if key else str(exc)
    print(f"[5] API call        : FAILED -- {type(exc).__name__}: {safe}")
    raise SystemExit(1)
