"""tests/test_summary.py

Unit tests for the POST /summarize endpoint.
Uses mocks — no real Gemini API call is made.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MOCK_SUMMARY = "Photosynthesis converts sunlight into chemical energy stored as glucose in plants."

LONG_TEXT = (
    "Photosynthesis is a process used by plants and other organisms to convert light energy, "
    "usually from the Sun, into chemical energy that can be later released to fuel the "
    "organism's activities. This process involves the absorption of carbon dioxide and water, "
    "which are converted into glucose and oxygen using the energy from sunlight. Photosynthesis "
    "occurs primarily in leaves, in the chloroplasts, where chlorophyll pigments absorb light."
)


# ── Happy path ────────────────────────────────────────────────

def test_summarize_returns_summary():
    with patch("modules.summary_module.generate_text", return_value=MOCK_SUMMARY):
        resp = client.post("/summarize", json={"text": LONG_TEXT})
    assert resp.status_code == 200
    assert resp.json()["summary"] == MOCK_SUMMARY


def test_summarize_response_not_empty():
    with patch("modules.summary_module.generate_text", return_value=MOCK_SUMMARY):
        resp = client.post("/summarize", json={"text": LONG_TEXT})
    assert resp.json()["summary"]


# ── Input validation ──────────────────────────────────────────

def test_summarize_empty_text_rejected():
    resp = client.post("/summarize", json={"text": ""})
    assert resp.status_code == 422


def test_summarize_whitespace_text_rejected():
    resp = client.post("/summarize", json={"text": "   "})
    assert resp.status_code == 422


def test_summarize_missing_field_rejected():
    resp = client.post("/summarize", json={})
    assert resp.status_code == 422


# ── Gemini failure ────────────────────────────────────────────

def test_summarize_gemini_error_returns_502():
    with patch("modules.summary_module.generate_text", side_effect=RuntimeError("Gemini down")):
        resp = client.post("/summarize", json={"text": LONG_TEXT})
    assert resp.status_code == 502
