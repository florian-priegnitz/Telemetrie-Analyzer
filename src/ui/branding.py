"""CI-Branding fuer Streamlit-UI — projekt-spezifischer Wrapper.

Re-exportiert die generischen Bauhaus-Streamlit-Symbole und ergaenzt
telemetrie-analyzer-spezifische Severity-Mappings.

Quelle: bauhaus-streamlit (interner Styleguide, vendoring siehe src/_vendor/).
"""
from __future__ import annotations

from src._vendor.bauhaus_streamlit import (
    COMPLIANCE_STATUS_COLORS,
    FAVICON_PATH,
    SEVERITY_COLORS,
    compliance_status_color,
    get_plotly_template,
    inject_global_css,
    render_lineal,
    severity_color,
)

__all__ = [
    "inject_global_css",
    "render_lineal",
    "severity_color",
    "compliance_status_color",
    "get_plotly_template",
    "SEVERITY_COLORS",
    "COMPLIANCE_STATUS_COLORS",
    "FAVICON_PATH",
]
