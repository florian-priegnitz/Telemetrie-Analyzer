"""Tests für den Report-Generator (HTML / Markdown / JSON)."""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.compliance.engine import ComplianceEngine
from src.compliance.models import ComplianceResult
from src.detection.engine import DetectionEngine, DetectionResult
from src.reports import ReportGenerator
from src.reports.privacy import (
    _SCRIPT_STYLE_PATTERN,
    PrivacyLeakError,
    assert_no_plaintext,
    pseudonymize_client,
)


def _strip_inline_scripts(html: str) -> str:
    """Entfernt <script>/<style>-Bloecke (z. B. inline plotly.js), bevor
    HTML-Output auf Klartext-PII oder externe URLs geprueft wird. Library-Code
    enthaelt naturgemaess numerische Tokens und Konfig-Strings, die nicht als
    Datenleck zaehlen — siehe src/reports/privacy.assert_no_plaintext."""
    return _SCRIPT_STYLE_PATTERN.sub("", html)

_FIXED_SALT = "test-salt-do-not-use-in-prod"


def _make_sample_results() -> tuple[DetectionResult, ComplianceResult]:
    """Baut realistische Sample-Results via Engine-Pipeline (vermeidet handgemachte Fixtures)."""
    df = pd.DataFrame([
        {"timestamp": "2026-04-10 09:00:00", "domain": "chat.openai.com",
         "client": "ip_aaaaaaaa", "bytes_uploaded": 800_000},
        {"timestamp": "2026-04-10 10:00:00", "domain": "chat.openai.com",
         "client": "ip_aaaaaaaa", "bytes_uploaded": 1_200},
        {"timestamp": "2026-04-11 08:00:00", "domain": "chat.openai.com",
         "client": "ip_aaaaaaaa", "bytes_uploaded": 900},
        {"timestamp": "2026-04-10 11:00:00", "domain": "claude.ai",
         "client": "ip_bbbbbbbb", "bytes_uploaded": 1_500},
        {"timestamp": "2026-04-10 12:00:00", "domain": "chat.deepseek.com",
         "client": "ip_cccccccc", "bytes_uploaded": 2_000},
        {"timestamp": "2026-04-10 13:00:00", "domain": "www.google.com",
         "client": "ip_dddddddd", "bytes_uploaded": 500},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    return detection, compliance


def _make_empty_results() -> tuple[DetectionResult, ComplianceResult]:
    detection = DetectionEngine().analyze(pd.DataFrame())
    compliance = ComplianceEngine().analyze(detection)
    return detection, compliance


def test_generator_renders_executive_html_smoke():
    det, comp = _make_sample_results()
    gen = ReportGenerator(det, comp, salt=_FIXED_SALT)
    html = gen.render(audience="executive", format="html")
    assert "<html" in html.lower()
    assert "Executive Summary" in html
    assert "Compliance-Status" in html


def test_generator_renders_it_security_html_smoke():
    det, comp = _make_sample_results()
    html = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="it_sec", format="html")
    assert "IT-Security Report" in html
    assert "Risiko-Verteilung" in html
    assert "Findings" in html


def test_generator_renders_compliance_html_smoke():
    det, comp = _make_sample_results()
    html = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="compliance", format="html")
    assert "Compliance Report" in html
    assert "Framework-Übersicht" in html
    # Alle 6 Frameworks sollten erscheinen
    for fw in ("DORA", "EU AI Act", "ISO/IEC 42001", "ISO/IEC 27001", "DSGVO", "EU CRA"):
        assert fw in html


def test_generator_renders_all_audiences_returns_dict():
    det, comp = _make_sample_results()
    out = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="all", format="html")
    assert isinstance(out, dict)
    assert set(out.keys()) == {"executive", "it_sec", "compliance"}
    for content in out.values():
        assert content.startswith("<!DOCTYPE html>")


def test_markdown_output_contains_no_html_tags():
    det, comp = _make_sample_results()
    md = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="executive", format="markdown")
    # Keine HTML-Block-Tags (lowercase Heuristik, ignoriert div/script/etc.)
    forbidden = ["<html", "<body", "<div", "<table>", "<script"]
    for tag in forbidden:
        assert tag not in md.lower(), f"Markdown enthält HTML-Tag: {tag}"


def test_json_output_matches_schema():
    det, comp = _make_sample_results()
    data = ReportGenerator(det, comp, salt=_FIXED_SALT).render(format="json")
    assert isinstance(data, dict)
    assert set(data.keys()) >= {"report_meta", "summary", "framework_scores", "findings"}
    assert data["report_meta"]["pseudonymized"] is True
    assert isinstance(data["framework_scores"], list)
    assert isinstance(data["findings"], list)
    # Jeder Finding hat compliance_mappings als Liste
    for f in data["findings"]:
        assert "client_pseudonym" in f
        assert f["client_pseudonym"].startswith("client_")
        assert isinstance(f["compliance_mappings"], list)


def test_no_plaintext_ips_in_html_output():
    det, comp = _make_sample_results()
    out = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="all", format="html")
    # Strikte IPv4-Heuristik (Oktette 0-255), <script>/<style> ausgeklammert
    # (inline plotly.js enthaelt Library-Tokens, keine Nutzerdaten).
    ipv4 = re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b",
    )
    for content in out.values():
        body = _strip_inline_scripts(content)
        matches = ipv4.findall(body)
        # RFC 5737 Doku-IPs sind ok, real-aussehende IPs nicht
        real_ips = [m for m in matches if m not in {"192.0.2.0", "198.51.100.0", "203.0.113.0"}]
        assert not real_ips, f"Klartext-IPs im HTML: {real_ips}"


def test_no_plaintext_ips_in_json_output():
    det, comp = _make_sample_results()
    data = ReportGenerator(det, comp, salt=_FIXED_SALT).render(format="json")
    text = json.dumps(data, default=str)
    # assert_no_plaintext wirft bei Verstoss
    assert_no_plaintext(text)


def test_no_internal_hostnames_in_output():
    det, comp = _make_sample_results()
    html = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="executive", format="html")
    body = _strip_inline_scripts(html)
    assert ".local" not in body
    assert ".lan" not in body
    assert ".internal" not in body


def test_empty_detection_result_renders_clean_fallback():
    det, comp = _make_empty_results()
    gen = ReportGenerator(det, comp, salt=_FIXED_SALT)
    for audience in ("executive", "it_sec", "compliance"):
        html = gen.render(audience=audience, format="html")
        assert "<html" in html.lower()
    # Markdown auch
    md = gen.render(audience="executive", format="markdown")
    assert "Compliance-Status" in md


def test_pseudonymize_client_is_deterministic_with_salt():
    a = pseudonymize_client("192.168.1.42", salt="my-salt")
    b = pseudonymize_client("192.168.1.42", salt="my-salt")
    c = pseudonymize_client("192.168.1.42", salt="other-salt")
    assert a == b
    assert a != c
    assert a.startswith("client_")


def test_pseudonymize_client_passes_through_existing_pseudonyms():
    """Bereits pseudonymisierte IDs werden auf client_-Präfix normalisiert, nicht doppelt gehasht."""
    out = pseudonymize_client("ip_a3f8c1d2", salt="any-salt")
    assert out == "client_a3f8c1d2"


def test_charts_embedded_as_html_snippets():
    det, comp = _make_sample_results()
    html = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="it_sec", format="html")
    # plotly's to_html mit full_html=False gibt <div ...>-Wrapper zurück
    assert "<div" in html
    # Plotly-Bibliothek wird inline eingebettet (offline-Default)
    assert "plotly" in html.lower()


def test_default_html_has_no_external_http_calls():
    """Audit-Reports muessen offline lesbar sein — keine externen HTTP-Calls (Sprint 13b / #91).

    Geprueft wird der Markup-Teil ausserhalb <script>/<style>. Plotly-Library-Code
    enthaelt zwar interne Default-URL-Strings (z. B. 'cdn.plot.ly' als Config-Wert),
    feuert sie aber nicht im Auto-Boot der Reports.
    """
    det, comp = _make_sample_results()
    out = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="all", format="html")
    forbidden_hosts = (
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdn.plot.ly",
        "cdnjs.cloudflare.com",
        "cdn.jsdelivr.net",
        "unpkg.com",
    )
    for audience, html in out.items():
        body = _strip_inline_scripts(html).lower()
        for host in forbidden_hosts:
            assert host not in body, f"{audience}: externer HTTP-Call zu {host}"


def test_default_html_uses_bauhaus_ci_tokens():
    """Visueller Smoke: Bauhaus-CI-Marker (Lineal, ta-meta, Rostrot-Accent) sind im Output (Sprint 13b)."""
    det, comp = _make_sample_results()
    html = ReportGenerator(det, comp, salt=_FIXED_SALT).render(audience="executive", format="html")
    assert "ta-lineal" in html, "Bauhaus-Lineal-Header fehlt"
    assert "ta-meta" in html, "ta-meta-Block fehlt"
    assert "#9B4A2F" in html, "Rostrot-Akzent (--c-acc) fehlt"
    assert "ta-sev-" in html or "ta-kpi" in html, "Bauhaus-Komponentenklassen fehlen"


def test_write_creates_files_in_output_dir():
    det, comp = _make_sample_results()
    with tempfile.TemporaryDirectory() as tmp:
        gen = ReportGenerator(det, comp, salt=_FIXED_SALT)
        paths = gen.write(Path(tmp), audience="all", format="html")
        assert len(paths) == 3
        for p in paths:
            assert p.exists()
            assert p.stat().st_size > 0


def test_write_json_creates_single_file():
    det, comp = _make_sample_results()
    with tempfile.TemporaryDirectory() as tmp:
        paths = ReportGenerator(det, comp, salt=_FIXED_SALT).write(Path(tmp), format="json")
        assert len(paths) == 1
        loaded = json.loads(paths[0].read_text(encoding="utf-8"))
        assert loaded["report_meta"]["pseudonymized"] is True


def test_assert_no_plaintext_raises_on_real_ip():
    with pytest.raises(PrivacyLeakError):
        assert_no_plaintext("Client 192.168.1.42 detected")


def test_assert_no_plaintext_raises_on_internal_hostname():
    with pytest.raises(PrivacyLeakError):
        assert_no_plaintext("workstation01.corp accessed openai")


def test_assert_no_plaintext_passes_clean_text():
    # Wirft NICHT
    assert_no_plaintext("client_a3f8 used chat.openai.com 12 times today")
