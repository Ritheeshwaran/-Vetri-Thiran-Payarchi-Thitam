from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import ExplainRequest, QuizRequest, SummarizeRequest
from summary_module import summarize_text


app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Any:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": settings.gemini_configured,
        "explanation_provider": settings.explanation_provider,
        "model": settings.gemini_model,
    }


@app.get("/qa")
def qa(question: str = Query(..., min_length=2, max_length=8000)) -> dict[str, str]:
    try:
        return {"question": question, "answer": answer_question(question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
def explain(request: ExplainRequest) -> dict[str, str]:
    try:
        return {"topic": request.topic, "explanation": explain_topic(request.topic)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
def summarize(request: SummarizeRequest) -> dict[str, str]:
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
def quiz(request: QuizRequest) -> dict[str, Any]:
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/learn/recommendations")
def recommendations(
    topic: str = Query(..., min_length=2, max_length=300)
) -> dict[str, str]:
    try:
        return {
            "topic": topic,
            "recommendation": get_learning_recommendations(topic),
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
