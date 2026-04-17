"""Framework-Score-Card mit HTML-Inline-Progress-Bar (portiert aus Compliance Dashboard)."""

from __future__ import annotations

from typing import Any

import streamlit as st


def _bar_color(percent: float) -> str:
    if percent >= 80:
        return "#0E8A16"
    if percent >= 50:
        return "#D4A72C"
    return "#B60205"


def render_framework_card(framework_view: dict[str, Any]) -> None:
    """Rendert eine Score-Card für ein einzelnes Framework."""
    label = framework_view.get("framework_label", framework_view.get("framework", "?"))
    percent = framework_view.get("score_percent", 0.0)
    triggered = framework_view.get("triggered_controls", 0)
    total = framework_view.get("total_controls", 0)
    non_c = framework_view.get("non_compliant", 0)
    partial = framework_view.get("partially_compliant", 0)
    review = framework_view.get("needs_review", 0)
    color = _bar_color(percent)

    st.markdown(
        f"""
        <div style="background:white;border:1px solid #d0d7de;border-radius:6px;
                    padding:1rem;margin-bottom:.6rem;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <strong style="font-size:1.1em;">{label}</strong>
            <span style="color:{color};font-weight:700;font-size:1.4em;">{percent:.1f}%</span>
          </div>
          <div style="height:8px;border-radius:4px;background:#eaeef2;margin:.5rem 0;">
            <div style="height:8px;border-radius:4px;width:{percent}%;background:{color};"></div>
          </div>
          <div style="color:#57606a;font-size:.9em;">
            {triggered}/{total} Controls betroffen ·
            <strong style="color:#B60205;">{non_c}</strong> non-compliant ·
            <strong style="color:#D4A72C;">{partial}</strong> partial ·
            <strong style="color:#0969da;">{review}</strong> review
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
