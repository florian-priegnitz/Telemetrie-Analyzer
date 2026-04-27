"""Pluggable LLM backends (Anthropic / Ollama / Skip)."""

from __future__ import annotations

import logging
import os

from .anthropic_backend import AnthropicBackend
from .base import BackendError, BackendNotAvailable, LLMBackend
from .ollama_backend import OllamaBackend

logger = logging.getLogger(__name__)


VALID_BACKENDS = {"anthropic", "ollama", "skip"}


def select_backend(
    name: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
) -> LLMBackend | None:
    """Pick a backend based on env var, explicit name, or available credentials.

    Resolution order:
      1. explicit `name` argument
      2. env LLM_BACKEND
      3. auto: anthropic if ANTHROPIC_API_KEY, else None (skip mode)

    Returns None for skip mode — callers must handle the no-backend case.
    """
    choice = (name or os.environ.get("LLM_BACKEND") or "").strip().lower()

    if choice and choice not in VALID_BACKENDS:
        logger.warning("Unknown LLM_BACKEND=%r; falling back to auto", choice)
        choice = ""

    api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY")

    if choice == "skip":
        return None
    if choice == "ollama":
        kwargs = {"model": model} if model else {}
        return OllamaBackend(**kwargs)
    if choice == "anthropic":
        if not api_key:
            logger.warning("LLM_BACKEND=anthropic but no ANTHROPIC_API_KEY; skip mode")
            return None
        kwargs = {"model": model} if model else {}
        return AnthropicBackend(api_key=api_key, **kwargs)

    # Auto mode
    if api_key:
        kwargs = {"model": model} if model else {}
        return AnthropicBackend(api_key=api_key, **kwargs)
    return None


__all__ = [
    "AnthropicBackend",
    "BackendError",
    "BackendNotAvailable",
    "LLMBackend",
    "OllamaBackend",
    "VALID_BACKENDS",
    "select_backend",
]
