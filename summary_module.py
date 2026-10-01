from __future__ import annotations

from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text for a student.

Requirements:
- Preserve the important facts and meaning.
- Remove repetition and unnecessary wording.
- Use clear, simple language.
- Prefer short paragraphs and bullet points where useful.
- Do not add information that is not supported by the input.

Text:
{text}
""".strip()

    return generate_text(prompt, temperature=0.2, max_output_tokens=1200)
