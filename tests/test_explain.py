"""tests/test_explain.py

Unit tests for the POST /explain endpoint.
Uses mocks — no real Gemini API call is made.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MOCK_EXPLANATION = (
    "TCP/IP stands for Transmission Control Protocol/Internet Protocol. "
    "It is the fundamental communication language of the internet."
)


# ── Happy path ────────────────────────────────────────────────

def test_explain_returns_explanation():
    with patch("modules.explanation_module.generate_text", return_value=MOCK_EXPLANATION):
        resp = client.post("/explain", json={"topic": "TCP/IP"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["topic"] == "TCP/IP"
    assert data["explanation"] == MOCK_EXPLANATION


def test_explain_response_not_empty():
    with patch("modules.explanation_module.generate_text", return_value=MOCK_EXPLANATION):
        resp = client.post("/explain", json={"topic": "Gravity"})
    assert resp.json()["explanation"]


# ── Input validation ──────────────────────────────────────────

def test_explain_empty_topic_rejected():
    resp = client.post("/explain", json={"topic": ""})
    assert resp.status_code == 422


def test_explain_whitespace_topic_rejected():
    resp = client.post("/explain", json={"topic": "   "})
    assert resp.status_code == 422


def test_explain_missing_field_rejected():
    resp = client.post("/explain", json={})
    assert resp.status_code == 422


# ── Gemini failure ────────────────────────────────────────────

def test_explain_gemini_error_returns_502():
    with patch("modules.explanation_module.generate_text", side_effect=RuntimeError("Gemini down")):
        resp = client.post("/explain", json={"topic": "TCP/IP"})
    assert resp.status_code == 502
