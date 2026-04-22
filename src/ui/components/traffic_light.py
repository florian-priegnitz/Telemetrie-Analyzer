"""Compliance-Ampel: gross, farbig, prominent."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.ui.components.badges import traffic_light_dot


def render_compliance_traffic_light(report_data: dict[str, Any]) -> None:
    summary = report_data.get("summary", {})
    state = summary.get("compliance_traffic_light", "red")
    percent = summary.get("overall_compliance_percent", 0.0)

    label_map = {"green": "Compliant", "yellow": "Handlungsbedarf", "red": "Kritisch"}
    label = label_map.get(state, "—")

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:1rem;
                    padding:1rem;background:#f6f8fa;border-radius:8px;
                    border:1px solid #d0d7de;">
          {traffic_light_dot(state, size_px=48)}
          <div>
            <div style="font-size:1.6em;font-weight:700;">{percent:.1f}% — {label}</div>
            <div style="color:#57606a;">Erfüllungsgrad über alle 6 Frameworks</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
