from __future__ import annotations

from config import settings
from gemini_client import generate_text


def _gemini_explain(topic: str) -> str:
    prompt = f"""
Explain the topic "{topic}" to a beginner student.

Requirements:
- Start with a one-sentence definition.
- Explain the idea in simple language.
- Give a small example or analogy when useful.
- Include key points as bullets.
- Keep it concise enough for quick revision.
- Do not assume advanced background knowledge.
""".strip()

    return generate_text(prompt, temperature=0.3, max_output_tokens=900)


def _local_explain(topic: str) -> str:
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires requirements-local.txt. "
            "Install it and restart the application."
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(settings.local_explanation_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(settings.local_explanation_model)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    prompt = (
        f"Explain the concept of {topic} in a simple and clear way "
        "for a beginner student. Give a short example."
    )
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def explain_topic(topic: str) -> str:
    provider = settings.explanation_provider

    if provider == "local":
        return _local_explain(topic)

    return _gemini_explain(topic)
