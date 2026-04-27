"""Anthropic Claude API backend (cloud, default for keyed deployments)."""

from __future__ import annotations

import logging

from .base import BackendError, BackendNotAvailable

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-20250514"


class AnthropicBackend:
    """Wraps the official anthropic SDK behind LLMBackend."""

    name = "anthropic"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        client: object | None = None,
    ) -> None:
        self._model = model
        self._client = client

        if client is None and api_key:
            try:
                import anthropic  # local import — keep optional
            except ImportError:
                logger.warning("anthropic package not installed; backend unavailable")
            else:
                self._client = anthropic.Anthropic(api_key=api_key)

    @property
    def model(self) -> str:
        return self._model

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def chat(self, system: str, user: str, max_tokens: int = 4096) -> str:
        if self._client is None:
            raise BackendNotAvailable("Anthropic backend has no client configured")
        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return response.content[0].text
        except Exception as exc:
            raise BackendError(f"Anthropic API call failed: {exc}") from exc
