"""Regressionstests für die Findings-Filter-Semantik (UI-Page findings.py).

Hintergrund: Bis zum Fix in PR #56 wurden die Filter-Keys in
``init_session_state`` auf leere Listen vorbelegt. Streamlits multiselect
liest bei vorhandenem Session-State-Key den Wert aus dem State und
ignoriert den ``default``-Parameter — Ergebnis: leere Auswahl,
keine Findings sichtbar.

Dieses Modul testet die reine Filter-Logik unabhängig von Streamlit
(ohne AppTest, da nur die Semantik validiert werden soll).
"""

from __future__ import annotations


def _sample_findings() -> list[dict]:
    return [
        {
            "service": "OpenAI ChatGPT",
            "risk_level": "critical",
            "compliance_mappings": [{"framework": "DORA"}, {"framework": "DSGVO"}],
        },
        {
            "service": "Anthropic Claude",
            "risk_level": "high",
            "compliance_mappings": [{"framework": "ISO_27001"}],
        },
        {
            "service": "Grammarly AI",
            "risk_level": "medium",
            "compliance_mappings": [{"framework": "EU_AI_ACT"}],
        },
    ]


def _apply_filter(findings, selected_risk, selected_fw, service_filter):
    """Dieselbe Filter-Semantik wie in src/ui/pages/findings.py."""
    risk_filter_active = bool(selected_risk)
    fw_filter_active = bool(selected_fw)
    return [
        f for f in findings
        if (not risk_filter_active or f.get("risk_level") in selected_risk)
        and (not fw_filter_active or any(
            m.get("framework") in selected_fw
            for m in f.get("compliance_mappings", [])
        ))
        and (not service_filter or service_filter.lower() in f.get("service", "").lower())
    ]


class TestFindingsFilter:

    def test_empty_risk_selection_shows_all(self):
        """Regression: leere Risk-Auswahl darf nicht alle Findings wegfiltern."""
        out = _apply_filter(_sample_findings(), [], ["DORA", "DSGVO", "ISO_27001",
                                                     "EU_AI_ACT", "ISO_42001"], "")
        assert len(out) == 3

    def test_empty_framework_selection_shows_all(self):
        out = _apply_filter(_sample_findings(),
                            ["critical", "high", "medium", "low"], [], "")
        assert len(out) == 3

    def test_both_filters_empty_shows_all(self):
        """Die häufigste Bug-Konstellation vor dem Fix: alles leer."""
        out = _apply_filter(_sample_findings(), [], [], "")
        assert len(out) == 3

    def test_specific_risk_filter_narrows(self):
        out = _apply_filter(_sample_findings(), ["critical"], [], "")
        assert len(out) == 1
        assert out[0]["service"] == "OpenAI ChatGPT"

    def test_specific_framework_filter_narrows(self):
        out = _apply_filter(_sample_findings(), [], ["DORA"], "")
        assert len(out) == 1
        assert out[0]["service"] == "OpenAI ChatGPT"

    def test_service_text_filter_case_insensitive(self):
        out = _apply_filter(_sample_findings(), [], [], "claude")
        assert len(out) == 1
        assert out[0]["service"] == "Anthropic Claude"

    def test_combined_filters_intersect(self):
        out = _apply_filter(_sample_findings(), ["high", "medium"],
                            ["EU_AI_ACT"], "")
        assert len(out) == 1
        assert out[0]["service"] == "Grammarly AI"

    def test_finding_without_mappings_dropped_by_fw_filter(self):
        findings = [
            {"service": "X", "risk_level": "high", "compliance_mappings": []},
            {"service": "Y", "risk_level": "high",
             "compliance_mappings": [{"framework": "DORA"}]},
        ]
        out = _apply_filter(findings, [], ["DORA"], "")
        # X hat kein Mapping → fällt raus; Y hat DORA → bleibt
        assert len(out) == 1
        assert out[0]["service"] == "Y"
