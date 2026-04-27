"""Tests for the pluggable LLM backend layer (#72, Sprint 10A)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from src.analyzer.backends import (
    AnthropicBackend,
    BackendError,
    BackendNotAvailable,
    LLMBackend,
    OllamaBackend,
    select_backend,
)

# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------

class TestProtocolConformance:

    def test_anthropic_satisfies_protocol(self):
        backend = AnthropicBackend(api_key=None)
        assert isinstance(backend, LLMBackend)

    def test_ollama_satisfies_protocol(self):
        backend = OllamaBackend(host="http://localhost:11434")
        assert isinstance(backend, LLMBackend)


# ---------------------------------------------------------------------------
# AnthropicBackend
# ---------------------------------------------------------------------------

class TestAnthropicBackend:

    def test_no_key_unavailable(self):
        backend = AnthropicBackend(api_key=None)
        assert backend.name == "anthropic"
        assert backend.is_available is False

    def test_chat_without_client_raises(self):
        backend = AnthropicBackend(api_key=None)
        with pytest.raises(BackendNotAvailable):
            backend.chat("sys", "user")

    def test_chat_dispatches_to_messages_api(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="hello back")]
        mock_client.messages.create.return_value = mock_response

        backend = AnthropicBackend(api_key="test", client=mock_client, model="m1")
        assert backend.is_available is True
        out = backend.chat("system prompt", "user prompt", max_tokens=512)

        assert out == "hello back"
        mock_client.messages.create.assert_called_once_with(
            model="m1",
            max_tokens=512,
            system="system prompt",
            messages=[{"role": "user", "content": "user prompt"}],
        )

    def test_chat_wraps_exceptions(self):
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = RuntimeError("boom")
        backend = AnthropicBackend(api_key="test", client=mock_client)
        with pytest.raises(BackendError, match="boom"):
            backend.chat("s", "u")


# ---------------------------------------------------------------------------
# OllamaBackend
# ---------------------------------------------------------------------------

class TestOllamaBackend:

    def test_defaults_from_env(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_HOST", "http://example.test:9999")
        monkeypatch.setenv("OLLAMA_MODEL", "qwen2.5:14b")
        backend = OllamaBackend()
        assert backend.host == "http://example.test:9999"
        assert backend.model == "qwen2.5:14b"

    def test_explicit_args_override_env(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_HOST", "http://from-env:1")
        backend = OllamaBackend(host="http://override:2", model="m")
        assert backend.host == "http://override:2"
        assert backend.model == "m"

    def test_strips_trailing_slash(self):
        backend = OllamaBackend(host="http://localhost:11434/")
        assert backend.host == "http://localhost:11434"

    def test_is_available_handles_unreachable(self):
        backend = OllamaBackend(host="http://127.0.0.1:1")  # closed port
        assert backend.is_available is False

    def test_is_available_true_on_ok(self):
        with patch("urllib.request.urlopen") as mock_open:
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_open.return_value.__enter__.return_value = mock_resp
            backend = OllamaBackend(host="http://stub")
            assert backend.is_available is True

    def test_chat_posts_correct_payload(self):
        responses = []

        def fake_urlopen(req_or_url, timeout=None):
            ctx = MagicMock()
            resp = MagicMock()
            if isinstance(req_or_url, str):
                # health probe
                resp.status = 200
                ctx.__enter__.return_value = resp
                return ctx
            # chat post
            responses.append(req_or_url)
            resp.read.return_value = json.dumps({
                "message": {"role": "assistant", "content": "ollama-says-hi"},
            }).encode("utf-8")
            ctx.__enter__.return_value = resp
            return ctx

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            backend = OllamaBackend(host="http://stub", model="llama3.1:8b")
            out = backend.chat("sys", "user-text", max_tokens=256)

        assert out == "ollama-says-hi"
        assert len(responses) == 1
        request = responses[0]
        body = json.loads(request.data.decode("utf-8"))
        assert body["model"] == "llama3.1:8b"
        assert body["stream"] is False
        assert body["options"]["num_predict"] == 256
        assert body["messages"][0] == {"role": "system", "content": "sys"}
        assert body["messages"][1] == {"role": "user", "content": "user-text"}

    def test_chat_raises_when_unavailable(self):
        backend = OllamaBackend(host="http://127.0.0.1:1")  # closed
        with pytest.raises(BackendNotAvailable):
            backend.chat("s", "u")

    def test_chat_raises_on_malformed_response(self):
        def fake_urlopen(req_or_url, timeout=None):
            ctx = MagicMock()
            resp = MagicMock()
            if isinstance(req_or_url, str):
                resp.status = 200
            else:
                resp.read.return_value = b"{\"unexpected\": true}"
            ctx.__enter__.return_value = resp
            return ctx

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            backend = OllamaBackend(host="http://stub")
            with pytest.raises(BackendError, match="message.content"):
                backend.chat("s", "u")


# ---------------------------------------------------------------------------
# Factory: select_backend
# ---------------------------------------------------------------------------

class TestSelectBackend:

    def test_explicit_skip_returns_none(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "x")  # should be ignored
        assert select_backend(name="skip") is None

    def test_env_skip_returns_none(self, monkeypatch):
        monkeypatch.setenv("LLM_BACKEND", "skip")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
        assert select_backend() is None

    def test_explicit_ollama(self, monkeypatch):
        monkeypatch.delenv("LLM_BACKEND", raising=False)
        backend = select_backend(name="ollama")
        assert isinstance(backend, OllamaBackend)

    def test_explicit_anthropic_without_key_returns_none(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        assert select_backend(name="anthropic", api_key=None) is None

    def test_explicit_anthropic_with_key(self, monkeypatch):
        backend = select_backend(name="anthropic", api_key="sk-test")
        assert isinstance(backend, AnthropicBackend)

    def test_auto_no_key_returns_none(self, monkeypatch):
        monkeypatch.delenv("LLM_BACKEND", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        assert select_backend() is None

    def test_auto_with_key_picks_anthropic(self, monkeypatch):
        monkeypatch.delenv("LLM_BACKEND", raising=False)
        backend = select_backend(api_key="sk-test")
        assert isinstance(backend, AnthropicBackend)

    def test_unknown_backend_falls_back_to_auto(self, monkeypatch):
        monkeypatch.setenv("LLM_BACKEND", "openai-not-supported")
        backend = select_backend(api_key="sk-test")
        assert isinstance(backend, AnthropicBackend)
