"""
EduGenie – FastAPI Application Entry Point

Powered entirely by Google Gemini API.
Run with:  uvicorn main:app --reload
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.explanation_module import explain_topic
from modules.learning_path import get_recommendations
from modules.quiz_module import generate_quiz
from modules.qna import answer_question
from modules.summary_module import summarize_text
from schemas.explain import ExplainRequest, ExplainResponse
from schemas.learning_path import LearningPathRequest, LearningPathResponse
from schemas.qa import QARequest, QAResponse
from schemas.quiz import QuizRequest, QuizResponse
from schemas.summary import SummaryRequest, SummaryResponse

# ---------------------------------------------------------------------------
# App & template setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="AI-powered learning assistant — all features driven by Google Gemini API.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def index(request: Request) -> HTMLResponse:
    """Serve the EduGenie single-page interface."""
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.post("/qa", response_model=QAResponse, tags=["Q&A"])
async def qa_endpoint(payload: QARequest) -> QAResponse:
    """Answer a student question using Gemini."""
    try:
        return answer_question(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain", response_model=ExplainResponse, tags=["Explanation"])
async def explain_endpoint(payload: ExplainRequest) -> ExplainResponse:
    """Explain a concept at beginner level using Gemini."""
    try:
        return explain_topic(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse, tags=["Quiz"])
async def quiz_endpoint(payload: QuizRequest) -> QuizResponse:
    """Generate a 3-question multiple-choice quiz using Gemini."""
    try:
        return generate_quiz(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize", response_model=SummaryResponse, tags=["Summarization"])
async def summarize_endpoint(payload: SummaryRequest) -> SummaryResponse:
    """Summarise educational text using Gemini."""
    try:
        return summarize_text(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
    tags=["Learning Path"],
)
async def learning_path_endpoint(payload: LearningPathRequest) -> LearningPathResponse:
    """Return a structured learning path for a given topic and level using Gemini."""
    try:
        return get_recommendations(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
