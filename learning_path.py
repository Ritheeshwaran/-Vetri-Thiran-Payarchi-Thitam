from __future__ import annotations

from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for a learner who wants to study: {topic}

Structure the response as:
1. Beginner level
2. Intermediate level
3. Advanced level
4. Suggested practice/projects
5. Recommended resource types (books, documentation, tutorials, videos)
6. A realistic weekly study sequence

For each level, include important topics and a short purpose for learning them.
Keep the plan practical and adaptable. Do not fabricate specific URLs.
""".strip()

    return generate_text(prompt, temperature=0.4, max_output_tokens=1800)
