"""
JSON utility helpers.

Safely strips Markdown code fences that Gemini sometimes wraps JSON in,
then parses the cleaned string.
"""
from __future__ import annotations

import json
import re


def strip_markdown_fences(text: str) -> str:
    """
    Remove leading/trailing Markdown code fences such as:
      ```json ... ```   or   ``` ... ```
    Returns the raw content between the fences (or the original text if
    no fences are present).
    """
    # Match an optional language identifier after the opening fence
    pattern = r"^```[a-zA-Z]*\s*\n?(.*?)\n?```\s*$"
    match = re.match(pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def safe_parse_json(text: str) -> dict | list:
    """
    Strip Markdown fences then parse JSON.

    Raises:
        ValueError: if the text cannot be decoded as JSON.
    """
    cleaned = strip_markdown_fences(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON from Gemini response: {exc}\nRaw: {cleaned}") from exc
