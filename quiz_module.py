from __future__ import annotations

import json

from gemini_client import generate_text
from schemas import QuizResponse


def _clean_json_block(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def generate_quiz(text: str) -> list[dict]:
    prompt = f"""
You are EduGenie's quiz generator.

From the educational passage below, create EXACTLY 3 multiple-choice questions.
Each question must have EXACTLY 4 options and exactly one correct answer.

Return ONLY valid JSON in this shape:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The exact text of the correct option"
    }}
  ]
}}

Rules:
- Questions must be answerable from the passage.
- Options must be distinct.
- The answer must exactly match one option.
- Avoid trick questions.
- Do not use Markdown.

Passage:
{text}
""".strip()

    raw = generate_text(prompt, temperature=0.2, max_output_tokens=1400)
    cleaned = _clean_json_block(raw)

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini returned invalid quiz JSON: {exc}") from exc

    validated = QuizResponse.model_validate(payload)
    return [question.model_dump() for question in validated.questions]
