"""tests/test_learning_path.py

Unit tests for the POST /learn/recommendations endpoint.
Uses mocks — no real Gemini API call is made.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

MOCK_RECOMMENDATIONS = (
    "## Learning Path: SQL (Beginner)\n\n"
    "### Beginner Topics\n- What is a database?\n- Basic SELECT statements\n\n"
    "### Intermediate Topics\n- JOINs\n- Subqueries\n\n"
    "### Advanced Topics\n- Indexing\n- Query optimisation\n\n"
    "### Suggested Order\n1. Databases 101\n2. SELECT basics\n3. JOINs\n"
)


# ── Happy path ────────────────────────────────────────────────

def test_learn_returns_recommendations():
    with patch("modules.learning_path.generate_text", return_value=MOCK_RECOMMENDATIONS):
        resp = client.post("/learn/recommendations", json={"topic": "SQL", "level": "beginner"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["topic"] == "SQL"
    assert data["level"] == "beginner"
    assert data["recommendations"] == MOCK_RECOMMENDATIONS


def test_learn_intermediate_level():
    with patch("modules.learning_path.generate_text", return_value=MOCK_RECOMMENDATIONS):
        resp = client.post("/learn/recommendations", json={"topic": "Python", "level": "intermediate"})
    assert resp.status_code == 200
    assert resp.json()["level"] == "intermediate"


def test_learn_advanced_level():
    with patch("modules.learning_path.generate_text", return_value=MOCK_RECOMMENDATIONS):
        resp = client.post("/learn/recommendations", json={"topic": "Machine Learning", "level": "advanced"})
    assert resp.status_code == 200
    assert resp.json()["level"] == "advanced"


def test_learn_default_level_is_beginner():
    """Omitting level should default to 'beginner'."""
    with patch("modules.learning_path.generate_text", return_value=MOCK_RECOMMENDATIONS):
        resp = client.post("/learn/recommendations", json={"topic": "SQL"})
    assert resp.status_code == 200
    assert resp.json()["level"] == "beginner"


# ── Input validation ──────────────────────────────────────────

def test_learn_empty_topic_rejected():
    resp = client.post("/learn/recommendations", json={"topic": "", "level": "beginner"})
    assert resp.status_code == 422


def test_learn_whitespace_topic_rejected():
    resp = client.post("/learn/recommendations", json={"topic": "   ", "level": "beginner"})
    assert resp.status_code == 422


def test_learn_missing_topic_rejected():
    resp = client.post("/learn/recommendations", json={"level": "beginner"})
    assert resp.status_code == 422


def test_learn_invalid_level_rejected():
    resp = client.post("/learn/recommendations", json={"topic": "SQL", "level": "expert"})
    assert resp.status_code == 422


# ── Gemini failure ────────────────────────────────────────────

def test_learn_gemini_error_returns_502():
    with patch("modules.learning_path.generate_text", side_effect=RuntimeError("Gemini down")):
        resp = client.post("/learn/recommendations", json={"topic": "SQL", "level": "beginner"})
    assert resp.status_code == 502
