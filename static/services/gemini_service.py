"""
Centralised Gemini API service.

All modules call this service — there is NO direct Gemini client
instantiation anywhere else in the codebase.

Retry policy
------------
Transient availability / rate-limit errors (HTTP 503 UNAVAILABLE or any
error message containing "unavailable", "503", or "resource_exhausted")
are retried up to _MAX_RETRIES times with exponential back-off:
    attempt 1 → wait 1 s
    attempt 2 → wait 2 s
    attempt 3 → wait 4 s
All other errors (auth, validation, bad-request …) are raised immediately.
"""
from __future__ import annotations

import time
import logging

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

# Create a single client instance at import time
_client = genai.Client(api_key=GEMINI_API_KEY)

# ── Retry configuration ───────────────────────────────────────────────────────
_MAX_RETRIES: int = 3
_BASE_BACKOFF: float = 1.0  # seconds; doubles each attempt

# Keywords that identify a *transient* error worth retrying
_TRANSIENT_MARKERS = ("503", "unavailable", "resource_exhausted", "rate", "overloaded")


def _is_transient(exc: Exception) -> bool:
    """Return True if *exc* looks like a temporary Gemini availability error."""
    msg = str(exc).lower()
    return any(marker in msg for marker in _TRANSIENT_MARKERS)


def generate_text(prompt: str) -> str:
    """
    Send *prompt* to Gemini and return the text response.

    Retries up to _MAX_RETRIES times on transient 503/UNAVAILABLE errors
    using exponential back-off.  Permanent errors are raised immediately.

    Raises:
        RuntimeError: if the Gemini API call fails or returns an empty response
                      after all retries are exhausted.
    """
    last_exc: Exception | None = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = _client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            text = response.text
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text.strip()

        except Exception as exc:
            if not _is_transient(exc):
                # Permanent error — fail fast, no point retrying
                raise RuntimeError(f"Gemini API error: {exc}") from exc

            last_exc = exc
            wait = _BASE_BACKOFF * (2 ** (attempt - 1))  # 1 s, 2 s, 4 s
            logger.warning(
                "Gemini transient error (attempt %d/%d): %s — retrying in %.0f s",
                attempt,
                _MAX_RETRIES,
                exc,
                wait,
            )
            if attempt < _MAX_RETRIES:
                time.sleep(wait)

    raise RuntimeError(
        "Gemini is temporarily unavailable after "
        f"{_MAX_RETRIES} retries. Please try again in a moment. "
        f"(Last error: {last_exc})"
    ) from last_exc
