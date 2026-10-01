from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.gemini_configured:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to the .env file and restart EduGenie."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
