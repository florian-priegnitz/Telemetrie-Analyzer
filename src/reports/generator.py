"""ReportGenerator — orchestriert Context, Charts, Templates und DSGVO-Schutz.

API:
    gen = ReportGenerator(detection_result, compliance_result, salt=None, offline=False)
    html = gen.render(audience="executive", format="html")
    docs = gen.render(audience="all", format="html")          # dict[str, str]
    paths = gen.write(Path("reports/"), audience="all", format="html")
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.compliance.models import ComplianceResult
from src.detection.engine import DetectionResult
from src.reports.charts import build_all_charts
from src.reports.context import (
    ReportContext,
    build_context,
    context_to_json_dict,
)
from src.reports.privacy import assert_no_plaintext, get_default_salt

_TEMPLATE_DIR = Path(__file__).parent / "templates"

Audience = Literal["executive", "it_sec", "compliance", "all"]
Format = Literal["html", "markdown", "json"]

_TEMPLATE_NAMES: dict[tuple[str, str], str] = {
    ("executive", "html"): "executive.html.j2",
    ("it_sec", "html"): "it_security.html.j2",
    ("compliance", "html"): "compliance.html.j2",
    ("executive", "markdown"): "executive.md.j2",
    ("it_sec", "markdown"): "it_security.md.j2",
    ("compliance", "markdown"): "compliance.md.j2",
}

_AUDIENCES: tuple[str, ...] = ("executive", "it_sec", "compliance")


class ReportGenerator:
    """Erzeugt HTML/Markdown/JSON-Reports aus Detection + Compliance Results."""

    def __init__(
        self,
        detection_result: DetectionResult,
        compliance_result: ComplianceResult,
        salt: str | None = None,
        offline: bool = False,
    ):
        self._detection = detection_result
        self._compliance = compliance_result
        self._salt = salt or get_default_salt()
        self._offline = offline
        self._env = Environment(
            loader=FileSystemLoader(_TEMPLATE_DIR),
            autoescape=select_autoescape(["html", "html.j2", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._context: ReportContext | None = None

    def _get_context(self) -> ReportContext:
        if self._context is None:
            ctx_no_charts = build_context(self._detection, self._compliance, self._salt)
            charts = build_all_charts(ctx_no_charts, offline=self._offline)
            self._context = build_context(
                self._detection, self._compliance, self._salt, charts=charts,
            )
        return self._context

    def render(self, audience: Audience = "all", format: Format = "html") -> str | dict | dict[str, str]:
        """Render einen einzelnen Report oder alle drei Audiences.

        Returns:
            - audience="all", format="html"|"markdown" → dict[str, str]
            - audience=concrete, format="html"|"markdown" → str
            - format="json" → dict (immer alle Daten, audience-unabhängig)
        """
        if format == "json":
            return context_to_json_dict(self._get_context())

        if audience == "all":
            return {a: self._render_one(a, format) for a in _AUDIENCES}

        return self._render_one(audience, format)

    def _render_one(self, audience: str, format: str) -> str:
        try:
            template_name = _TEMPLATE_NAMES[(audience, format)]
        except KeyError:
            raise ValueError(f"Keine Template-Kombination für ({audience}, {format})")

        template = self._env.get_template(template_name)
        rendered = template.render(ctx=self._get_context())
        assert_no_plaintext(rendered)
        return rendered

    def write(
        self,
        output_dir: Path | str,
        audience: Audience = "all",
        format: Format = "html",
    ) -> list[Path]:
        """Schreibt Reports auf die Platte. Gibt geschriebene Pfade zurück."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        date_tag = datetime.now().strftime("%Y%m%d")
        ext = {"html": "html", "markdown": "md", "json": "json"}[format]
        written: list[Path] = []

        if format == "json":
            data = self.render(format="json")
            path = output_dir / f"report_{date_tag}.json"
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
            written.append(path)
            return written

        if audience == "all":
            outputs = self.render(audience="all", format=format)
            for aud, content in outputs.items():
                path = output_dir / f"report_{aud}_{date_tag}.{ext}"
                path.write_text(content, encoding="utf-8")
                written.append(path)
            return written

        content = self.render(audience=audience, format=format)
        path = output_dir / f"report_{audience}_{date_tag}.{ext}"
        path.write_text(content, encoding="utf-8")
        written.append(path)
        return written
