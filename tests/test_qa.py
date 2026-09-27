"""tests/test_qa.py

Unit tests for the POST /qa endpoint.
Uses mocks — no real Gemini API call is made.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MOCK_ANSWER = "Photosynthesis is the process by which plants make food using sunlight."


# ── Happy path ────────────────────────────────────────────────

def test_qa_returns_answer():
    with patch("modules.qna.generate_text", return_value=MOCK_ANSWER):
        resp = client.post("/qa", json={"question": "What is photosynthesis?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["question"] == "What is photosynthesis?"
    assert data["answer"] == MOCK_ANSWER


def test_qa_answer_not_empty():
    with patch("modules.qna.generate_text", return_value=MOCK_ANSWER):
        resp = client.post("/qa", json={"question": "What is gravity?"})
    assert resp.status_code == 200
    assert resp.json()["answer"]


# ── Input validation ──────────────────────────────────────────

def test_qa_empty_question_rejected():
    resp = client.post("/qa", json={"question": ""})
    assert resp.status_code == 422


def test_qa_whitespace_question_rejected():
    resp = client.post("/qa", json={"question": "   "})
    assert resp.status_code == 422


def test_qa_missing_field_rejected():
    resp = client.post("/qa", json={})
    assert resp.status_code == 422


# ── Gemini failure ────────────────────────────────────────────

def test_qa_gemini_error_returns_502():
    with patch("modules.qna.generate_text", side_effect=RuntimeError("Gemini down")):
        resp = client.post("/qa", json={"question": "What is DNA?"})
    assert resp.status_code == 502
