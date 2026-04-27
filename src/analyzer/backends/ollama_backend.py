"""Ollama backend — self-hosted LLM via local HTTP server.

Uses stdlib urllib to avoid pulling in httpx as a hard dependency.
Talks to Ollama's /api/chat endpoint (https://github.com/ollama/ollama/blob/main/docs/api.md).
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request

from .base import BackendError, BackendNotAvailable

logger = logging.getLogger(__name__)

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TIMEOUT = 120.0
HEALTH_TIMEOUT = 2.0


class OllamaBackend:
    """Talks to a local Ollama server (default localhost:11434)."""

    name = "ollama"

    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._host = (host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST).rstrip("/")
        self._model = model or os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL
        self._timeout = timeout

    @property
    def model(self) -> str:
        return self._model

    @property
    def host(self) -> str:
        return self._host

    @property
    def is_available(self) -> bool:
        url = f"{self._host}/api/tags"
        try:
            with urllib.request.urlopen(url, timeout=HEALTH_TIMEOUT) as resp:
                return resp.status == 200
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            logger.debug("Ollama health check failed (%s): %s", url, exc)
            return False

    def chat(self, system: str, user: str, max_tokens: int = 4096) -> str:
        if not self.is_available:
            raise BackendNotAvailable(f"Ollama server not reachable at {self._host}")

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        req = urllib.request.Request(
            f"{self._host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise BackendError(f"Ollama HTTP {exc.code}: {exc.reason}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise BackendError(f"Ollama transport error: {exc}") from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            raise BackendError(f"Ollama returned non-JSON body: {body[:200]}") from exc

        message = data.get("message")
        if not isinstance(message, dict) or "content" not in message:
            raise BackendError(f"Ollama response missing 'message.content': {data}")
        return message["content"]
