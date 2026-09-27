"""tests/test_quiz.py

Unit tests for the POST /quiz endpoint.
Verifies:
  - Exactly 3 questions
  - Exactly 4 options per question
  - correct_answer exists in options
  - Handles Markdown code fences
  - Rejects empty input
  - Handles Gemini failure
  - Handles malformed JSON from Gemini
Uses mocks — no real Gemini API call is made.
"""
import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ── Valid quiz fixture ────────────────────────────────────────

VALID_QUIZ = {
    "questions": [
        {
            "question": "What is photosynthesis?",
            "options": [
                "The process plants use to make food from sunlight",
                "A type of animal digestion",
                "A chemical reaction in volcanoes",
                "The movement of water in rivers"
            ],
            "correct_answer": "The process plants use to make food from sunlight"
        },
        {
            "question": "Which gas do plants absorb during photosynthesis?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
            "correct_answer": "Carbon Dioxide"
        },
        {
            "question": "What is produced as a by-product of photosynthesis?",
            "options": ["Carbon Dioxide", "Oxygen", "Nitrogen", "Water Vapour"],
            "correct_answer": "Oxygen"
        }
    ]
}


# ── Happy path ────────────────────────────────────────────────

def test_quiz_returns_three_questions():
    with patch("modules.quiz_module.generate_text", return_value=json.dumps(VALID_QUIZ)):
        resp = client.post("/quiz", json={"text": "Photosynthesis is the process..."})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["questions"]) == 3


def test_quiz_each_question_has_four_options():
    with patch("modules.quiz_module.generate_text", return_value=json.dumps(VALID_QUIZ)):
        resp = client.post("/quiz", json={"text": "Photosynthesis is the process..."})
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert len(q["options"]) == 4


def test_quiz_correct_answer_in_options():
    with patch("modules.quiz_module.generate_text", return_value=json.dumps(VALID_QUIZ)):
        resp = client.post("/quiz", json={"text": "Photosynthesis is the process..."})
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert q["correct_answer"] in q["options"]


def test_quiz_handles_markdown_fences():
    """Gemini sometimes wraps JSON in ```json ... ``` fences."""
    fenced = f"```json\n{json.dumps(VALID_QUIZ)}\n```"
    with patch("modules.quiz_module.generate_text", return_value=fenced):
        resp = client.post("/quiz", json={"text": "Some text about photosynthesis."})
    assert resp.status_code == 200
    assert len(resp.json()["questions"]) == 3


# ── Input validation ──────────────────────────────────────────

def test_quiz_empty_text_rejected():
    resp = client.post("/quiz", json={"text": ""})
    assert resp.status_code == 422


def test_quiz_whitespace_text_rejected():
    resp = client.post("/quiz", json={"text": "   "})
    assert resp.status_code == 422


def test_quiz_missing_field_rejected():
    resp = client.post("/quiz", json={})
    assert resp.status_code == 422


# ── Gemini failure ────────────────────────────────────────────

def test_quiz_gemini_error_returns_502():
    with patch("modules.quiz_module.generate_text", side_effect=RuntimeError("Gemini down")):
        resp = client.post("/quiz", json={"text": "Some text."})
    assert resp.status_code == 502


# ── Malformed JSON from Gemini ────────────────────────────────

def test_quiz_malformed_json_returns_422():
    with patch("modules.quiz_module.generate_text", return_value="not valid JSON {{{"):
        resp = client.post("/quiz", json={"text": "Some text."})
    assert resp.status_code == 422


def test_quiz_wrong_question_count_returns_422():
    """Gemini returns only 2 questions — should be rejected."""
    bad_quiz = {"questions": VALID_QUIZ["questions"][:2]}
    with patch("modules.quiz_module.generate_text", return_value=json.dumps(bad_quiz)):
        resp = client.post("/quiz", json={"text": "Some text."})
    assert resp.status_code == 422


def test_quiz_wrong_option_count_returns_422():
    """Gemini returns 3 options for a question — should be rejected."""
    bad_quiz = {
        "questions": [
            {
                "question": "Bad question?",
                "options": ["A", "B", "C"],     # only 3 options
                "correct_answer": "A"
            }
        ] + VALID_QUIZ["questions"][1:]
    }
    with patch("modules.quiz_module.generate_text", return_value=json.dumps(bad_quiz)):
        resp = client.post("/quiz", json={"text": "Some text."})
    assert resp.status_code == 422
