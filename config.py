from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    # Keep the model configurable so a user can switch models without code changes.
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    explanation_provider: str = os.getenv("EXPLANATION_PROVIDER", "gemini").lower()
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    demo_mode: bool = _as_bool(os.getenv("DEMO_MODE"), False)

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key.strip())


settings = Settings()
