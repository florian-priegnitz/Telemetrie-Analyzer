"""Pluggable LLM backend protocol.

Allows the Telemetrie-Analyzer to switch between cloud-hosted Anthropic
and self-hosted Ollama without touching analyzer logic. Selection is
controlled via env LLM_BACKEND or constructor argument.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class BackendError(Exception):
    """Raised on backend-level transport or protocol failures."""


class BackendNotAvailable(BackendError):
    """Raised when a backend was selected but cannot serve requests."""


@runtime_checkable
class LLMBackend(Protocol):
    """Protocol every backend implementation must satisfy.

    A backend is a thin chat-completion wrapper. It hides whether the
    request goes to a cloud API (Anthropic) or a local server (Ollama),
    so the analyzer can stay agnostic.
    """

    name: str

    @property
    def model(self) -> str: ...

    @property
    def is_available(self) -> bool: ...

    def chat(self, system: str, user: str, max_tokens: int = 4096) -> str: ...
