"""Bauhaus Streamlit — wiederverwendbares CI-Theme für Streamlit-Apps."""

from ._config import CONFIG_TOML_TEMPLATE, install_config
from .branding import (
    COMPLIANCE_STATUS_COLORS,
    FAVICON_PATH,
    SEVERITY_COLORS,
    compliance_status_color,
    get_plotly_template,
    inject_global_css,
    render_lineal,
    severity_color,
)

__version__ = "0.1.0"

__all__ = [
    "inject_global_css",
    "render_lineal",
    "severity_color",
    "compliance_status_color",
    "get_plotly_template",
    "SEVERITY_COLORS",
    "COMPLIANCE_STATUS_COLORS",
    "FAVICON_PATH",
    "CONFIG_TOML_TEMPLATE",
    "install_config",
    "__version__",
]
