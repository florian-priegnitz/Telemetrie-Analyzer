"""Pipeline-Wrapper für die Streamlit-UI.

Einziger Punkt, an dem die UI mit der Analyse-Pipeline spricht. Pages/Components
importieren ausschliesslich aus diesem Modul (+ Components untereinander).

Caching: Wir cachen das JSON-Dict (nicht den ReportContext), weil ReportContext
Datetime + Dataclass-Listen enthält, die für Streamlits Hash-Funktion problematisch
sind. Aus dem Dict baut die UI bei Bedarf die Anzeige-Strukturen.

Parser-Dispatch: ``_PARSER_DISPATCH`` ist das UI-Gegenstück zu ``_PARSERS`` in
``src/cli.py``. Beide delegieren Format-Erkennung an ``src/parsers/detection.py``
(Single Source of Truth).
"""

from __future__ import annotations

import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import streamlit as st

from src.analytics.sessions import (
    build_session_graph,
    top_global_pairs,
    top_service_pairs_per_client,
)
from src.analytics.temporal import build_hourly_heatmap, mask_low_count_cells
from src.compliance.engine import ComplianceEngine
from src.detection.engine import DetectionEngine
from src.parsers.detection import detect_format
from src.privacy.k_anonymity import check_k_anonymity
from src.privacy.pseudonymizer import Pseudonymizer
from src.privacy.retention import apply_retention, load_policy, summarize
from src.reports.context import build_context, context_to_json_dict
from src.reports.privacy import get_default_salt, pseudonymize_client

PipelineState = Literal["empty", "uploaded", "analyzing", "analyzed", "error"]
LogFormat = str  # Ein Key aus SUPPORTED_PARSERS oder "unknown"
UNKNOWN_FORMAT = "unknown"


def init_session_state() -> None:
    """Initialisiert Session-State mit Default-Werten (idempotent)."""
    defaults: dict[str, Any] = {
        "pipeline_state": "empty",
        "uploaded_filename": None,
        "uploaded_bytes": None,
        "detected_format": None,
        "report_data": None,  # JSON-Dict (siehe Modul-Docstring)
        "report_salt": get_default_salt(),
        # Double-Opt-in Squid-Username-Parsing (Issue #22).
        # Parser-Flag: aktiviert `%un`-Extraktion inkl. DSFA-Verantwortung
        # beim Operator. UI-Reveal: zweite Opt-in-Stufe, zeigt Pseudonyme
        # in der Users-Page unmaskiert an. Beides Default False.
        "squid_username_parsing_enabled": False,
        "squid_username_reveal": False,
        # Filter-Keys werden NICHT vor-initialisiert: ein st.multiselect mit
        # key=<...> liest zuerst aus st.session_state[key]. Wenn dort bereits
        # eine leere Liste steht, ignoriert Streamlit den `default`-Parameter
        # und zeigt eine leere Auswahl — Filter wäre sofort "zeig nichts".
        "error_message": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def load_scenario(scenario_key: str) -> None:
    """Lädt ein Demo-Scenario in den Session-State, als wäre es hochgeladen.

    Wird von ``upload_widget.render_scenario_buttons()`` und dem Empty-State-
    Onboarding aufgerufen. Setzt `uploaded_bytes`, `uploaded_filename`,
    `detected_format`, `pipeline_state="uploaded"` — danach rendert die UI
    den „Analyse starten"-Button wie bei einem echten Upload.
    """
    from src.ui.scenarios import get_scenario

    scenario = get_scenario(scenario_key)
    if scenario is None or not scenario.exists:
        st.session_state.pipeline_state = "error"
        st.session_state.error_message = f"Scenario {scenario_key!r} nicht verfügbar."
        return

    st.session_state.uploaded_bytes = scenario.file_path.read_bytes()
    st.session_state.uploaded_filename = scenario.file_path.name
    st.session_state.detected_format = scenario.parser
    st.session_state.pipeline_state = "uploaded"
    st.session_state.report_data = None
    st.session_state.error_message = None


def detect_log_format(content: bytes | str) -> LogFormat:
    """Thin-Wrapper um ``src.parsers.detection.detect_format()``.

    Akzeptiert bytes oder str (UI liefert bytes vom Upload-Widget).
    Liefert immer einen String — entweder einen Key aus ``SUPPORTED_PARSERS``
    oder ``"unknown"`` — nie None.
    """
    sample_bytes = content if isinstance(content, bytes) else content.encode("utf-8", errors="replace")
    return detect_format(sample_bytes) or UNKNOWN_FORMAT


def _build_parser_dispatch() -> dict[str, Callable[..., pd.DataFrame]]:
    """Lazy-initialisierte Parser-Registry (analog zu ``src/cli.py::_PARSERS``).

    Wird beim ersten ``run_pipeline()``-Aufruf populiert, um Import-Zeit
    klein zu halten (Streamlit-Cold-Start).
    """
    from src.parsers.aws_vpc_flow import parse_aws_vpc_flow_log
    from src.parsers.cloudflare_gateway import parse_cloudflare_gateway_log
    from src.parsers.elastic_ecs import parse_elastic_ecs_log
    from src.parsers.entra_id import parse_entra_signin_log
    from src.parsers.fortinet import parse_fortinet_log
    from src.parsers.netskope import parse_netskope_log
    from src.parsers.paloalto import parse_paloalto_log
    from src.parsers.pihole import parse_pihole_log
    from src.parsers.squid import parse_squid_log
    from src.parsers.sysmon import parse_sysmon_log
    from src.parsers.umbrella import parse_umbrella_log
    from src.parsers.zscaler import parse_zscaler_log

    return {
        "pihole": parse_pihole_log,
        "squid": parse_squid_log,
        "zscaler": parse_zscaler_log,
        "paloalto": parse_paloalto_log,
        "umbrella": parse_umbrella_log,
        "fortinet": parse_fortinet_log,
        "aws_vpc_flow": parse_aws_vpc_flow_log,
        "entra_id": parse_entra_signin_log,
        "cloudflare_gateway": parse_cloudflare_gateway_log,
        "netskope": parse_netskope_log,
        "sysmon": parse_sysmon_log,
        "elastic_ecs": parse_elastic_ecs_log,
    }


_PARSER_DISPATCH: dict[str, Callable[..., pd.DataFrame]] | None = None


def _get_parser(log_format: str) -> Callable[..., pd.DataFrame]:
    global _PARSER_DISPATCH
    if _PARSER_DISPATCH is None:
        _PARSER_DISPATCH = _build_parser_dispatch()
    if log_format not in _PARSER_DISPATCH:
        supported = ", ".join(sorted(_PARSER_DISPATCH))
        raise ValueError(
            f"Unbekannter Parser {log_format!r}. Verfügbar: {supported}"
        )
    return _PARSER_DISPATCH[log_format]


def _bytes_to_temp(file_bytes: bytes, suffix: str = ".log") -> Path:
    """Schreibt File-Bytes in eine temporäre Datei (Parser akzeptieren nur Pfade)."""
    f = tempfile.NamedTemporaryFile(mode="wb", suffix=suffix, delete=False)
    f.write(file_bytes)
    f.close()
    return Path(f.name)


@st.cache_data(show_spinner="Analysiere Log…", max_entries=5, ttl=3600)
def run_pipeline(
    file_bytes: bytes,
    filename: str,
    salt: str,
    log_format: LogFormat,
    squid_username_parsing: bool = False,
) -> dict[str, Any]:
    """Führt Parser → Detection → Compliance → ReportContext-Aufbau aus.

    Caching erfolgt anhand aller Parameter automatisch. ``squid_username_parsing``
    ist Teil des Cache-Keys, damit das Umschalten des Flags eine frische
    Pipeline-Ausführung erzwingt.

    Returns:
        JSON-serialisiertes Dict (entspricht `context_to_json_dict()`).

    Raises:
        ValueError bei unbekanntem Format oder leerem Result.
    """
    if log_format == UNKNOWN_FORMAT:
        raise ValueError(
            "Log-Format konnte nicht erkannt werden. Bitte Format manuell "
            "über das Upload-Widget wählen oder siehe '📚 Formate'-Page."
        )

    parse_fn = _get_parser(log_format)
    pseudo = Pseudonymizer(key=salt.encode("utf-8"))
    tmp_path = _bytes_to_temp(file_bytes)
    try:
        # Squid-Parser kennt ``parse_username`` opt-in (Issue #22). Andere
        # Parser haben diesen Parameter nicht — deshalb nur squid-spezifisch
        # durchreichen, damit der generische Dispatch nicht mit unbekannten
        # kwargs bricht.
        if log_format == "squid" and squid_username_parsing:
            df = parse_fn(tmp_path, pseudonymizer=pseudo, parse_username=True)
        else:
            df = parse_fn(tmp_path, pseudonymizer=pseudo)
    finally:
        tmp_path.unlink(missing_ok=True)

    if df.empty:
        raise ValueError(f"Keine parsbaren Einträge in {filename!r} gefunden.")

    policy = load_policy()
    df_trimmed = apply_retention(df, policy, log_type=log_format)
    retention_report = summarize(df, df_trimmed, policy, log_type=log_format)
    if df_trimmed.empty:
        raise ValueError(
            f"Nach Retention-Trim ({retention_report['days']} Tage) sind keine Einträge "
            f"mehr in {filename!r} vorhanden. Log-Horizont älter als Retention."
        )
    df = df_trimmed

    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    ctx = build_context(detection, compliance, salt=salt)
    result = context_to_json_dict(ctx)
    result["user_patterns"] = _build_user_patterns(df, result["findings"], salt)
    result["sessions"] = _build_sessions(
        df, salt,
        redacted=bool(result["user_patterns"].get("privacy_redacted")),
    )
    result["retention"] = retention_report
    result["user_aggregation"] = _build_user_aggregation(
        df, salt,
        redacted=bool(result["user_patterns"].get("privacy_redacted")),
    )

    # df enthält pseudonymisierte, aber nach DSGVO Art. 4(5) immer noch
    # personenbezogene Zeitreihen-Daten. Expliziter Discard nach letzter
    # Nutzung, analog zum `uploaded_bytes = None`-Pattern in overview.py.
    del df, df_trimmed

    # Pre-rendern aller Report-Varianten, während DetectionResult noch
    # in-scope ist. Wird später vom UI-Export-Button in der Overview-
    # Page direkt als Download ausgegeben. Overhead: ~50-200 KB je nach
    # Finding-Zahl. Erspart Pipeline-Rerun (Bytes sind nach DSGVO weg).
    from src.reports import ReportGenerator
    try:
        gen = ReportGenerator(detection, compliance, salt=salt)
        result["_exports"] = {
            "html": gen.render(audience="all", format="html"),
            "markdown": gen.render(audience="all", format="markdown"),
        }
    except Exception as exc:  # Export-Fehler darf die Analyse nicht brechen
        result["_exports"] = {"error": f"{type(exc).__name__}: {exc}"}

    return result


def _build_user_patterns(
    df: pd.DataFrame,
    findings_json: list[dict[str, Any]],
    salt: str,
) -> dict[str, Any]:
    """Verhaltens-Auswertung pro Client für die 'Users & Patterns'-Page (E2-4).

    Liefert k-Anonymitäts-Check, Top-Clients-Ranking und eine pseudonymisierte
    Stunden-Heatmap. DataFrame wird vor Discard konsumiert; alle Client-Keys
    werden über pseudonymize_client auf `client_<hash>` normalisiert.

    Privacy-Enforcement (DSGVO Art. 25):
    - Heatmap-Zellen mit Count < 3 werden maskiert (Re-ID-Schutz über
      24h-Aktivitätsmuster).
    - Bei ``reidentification_risk == "high"`` (beobachtetes k unterhalb
      ``minimum_k / 2``) wird das Top-Clients-Ranking redigiert, Heatmap
      komplett unterdrückt, und ein ``privacy_redacted``-Flag gesetzt, damit
      die UI eine Warnung rendert.
    """
    k = check_k_anonymity(df, field="client", minimum_k=5)
    high_reid_risk = k.reidentification_risk == "high"

    heatmap_by_client: dict[str, list[int]] = {}
    if not high_reid_risk:
        heatmap = build_hourly_heatmap(df)
        heatmap = mask_low_count_cells(heatmap, min_count=3)
        if not heatmap.empty:
            for raw_client, row in heatmap.iterrows():
                heatmap_by_client[pseudonymize_client(str(raw_client), salt)] = [
                    int(v) for v in row.tolist()
                ]

    by_client: dict[str, dict[str, Any]] = {}
    risk_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    for f in findings_json:
        c = f["client_pseudonym"]
        entry = by_client.setdefault(c, {
            "client_pseudonym": c,
            "services": set(),
            "total_queries": 0,
            "risk_max": 0,
            "risk_level_max": "low",
            "upload_events": 0,
            "has_document_upload": False,
        })
        entry["services"].add(f["service"])
        entry["total_queries"] += f["total_queries"]
        if f["risk_score"] > entry["risk_max"]:
            entry["risk_max"] = f["risk_score"]
        if risk_rank.get(f["risk_level"], 0) > risk_rank.get(entry["risk_level_max"], 0):
            entry["risk_level_max"] = f["risk_level"]
        entry["upload_events"] += f.get("upload_events", 0)
        entry["has_document_upload"] = entry["has_document_upload"] or f.get("has_document_upload", False)

    if high_reid_risk:
        # DSGVO Art. 25 Redaktion: k-Wert unterhalb minimum_k/2 → kein Ranking.
        top_clients: list[dict[str, Any]] = []
    else:
        top_clients = sorted(
            (
                {
                    "client_pseudonym": e["client_pseudonym"],
                    "service_count": len(e["services"]),
                    "total_queries": e["total_queries"],
                    "risk_max": e["risk_max"],
                    "risk_level_max": e["risk_level_max"],
                    "upload_events": e["upload_events"],
                    "has_document_upload": e["has_document_upload"],
                }
                for e in by_client.values()
            ),
            key=lambda e: (e["risk_max"], e["total_queries"]),
            reverse=True,
        )

    return {
        "k_anonymity": {
            "observed_k": k.observed_k,
            "minimum_k": k.minimum_k,
            "is_sufficient": k.is_sufficient,
            "reidentification_risk": k.reidentification_risk,
        },
        "privacy_redacted": high_reid_risk,
        "top_clients": top_clients,
        "hourly_heatmap": heatmap_by_client,
    }


def _build_user_aggregation(
    df: pd.DataFrame,
    salt: str,
    *,
    redacted: bool,
) -> dict[str, Any]:
    """Aggregiert Client → {user_pseudonyms} für die Users-Page (#22).

    Liefert ein Mapping pseudonymisierter Client → sortierte Liste der
    zugehörigen `user_<hash>`-Werte, sofern der Parser die ``user_pseudonym``-
    Spalte gefüllt hat (nur aktiv, wenn ``squid_username_parsing=True``
    gesetzt wurde).

    Bei ``redacted=True`` (k-Anonymität deutlich unterschritten) wird die
    Aggregation analog zu Top-Clients unterdrückt — DSGVO Art. 25 verlangt
    hier zusätzliche Schutzmaßnahmen gegen Re-Identifikation.
    """
    if "user_pseudonym" not in df.columns or redacted:
        return {"enabled": False, "per_client": {}, "unique_users": 0}

    aggregation: dict[str, set[str]] = {}
    all_users: set[str] = set()
    for _, row in df.iterrows():
        pseudo_user = row.get("user_pseudonym") or ""
        if not pseudo_user:
            continue
        pseudo_client = pseudonymize_client(str(row["client"]), salt)
        aggregation.setdefault(pseudo_client, set()).add(pseudo_user)
        all_users.add(pseudo_user)

    return {
        "enabled": True,
        "per_client": {
            client: sorted(users) for client, users in aggregation.items()
        },
        "unique_users": len(all_users),
    }


def _build_sessions(
    df: pd.DataFrame,
    salt: str,
    *,
    window_minutes: int = 30,
    redacted: bool = False,
) -> dict[str, Any]:
    """Service-Co-Occurrence-Analyse für die Sessions-Page (#23, E2-6).

    - ``top_pairs``: Dict pseudonymisierte_client → Top-5-SessionPair-Dicts.
      Bei ``redacted=True`` leer (analog user_patterns).
    - ``global_top_pairs``: Top-20-Paare globaler Graph (immer gesetzt,
      Graph ist Service-zentriert und enthält keine Client-Information).
    - ``graph_nodes`` / ``graph_edges``: JSON-taugliche Node/Edge-Listen für
      die Streamlit-Plotly-Visualisierung.
    - ``window_minutes``: Für Report-Disclaimer und Tests.
    """
    graph = build_session_graph(df, window_minutes=window_minutes)
    global_pairs = [p.as_dict() for p in top_global_pairs(graph, top_n=20)]

    if redacted:
        per_client = {}
    else:
        per_client = {
            pseudo: [pair.as_dict() for pair in pairs]
            for pseudo, pairs in top_service_pairs_per_client(
                df, salt, window_minutes=window_minutes, top_n=5,
            ).items()
        }

    return {
        "window_minutes": window_minutes,
        "top_pairs": per_client,
        "global_top_pairs": global_pairs,
        "graph_nodes": sorted(graph.nodes()),
        "graph_edges": [
            {
                "a": a, "b": b,
                "weight": int(data.get("weight", 0)),
                "clients": int(data.get("clients", 0)),
            }
            for a, b, data in graph.edges(data=True)
        ],
    }


def _rebuild_report_artifacts(
    report_data: dict[str, Any],
    audience: str,
    format: str,
) -> str:
    """Rendert HTML/Markdown-Report aus dem Session-State-Dict.

    Der Streamlit-Cache hält nur das serialisierte ``report_data``,
    nicht die DetectionResult/ComplianceResult-Dataclasses. Für den
    Export rendern wir die Jinja2-Templates direkt auf einem
    SimpleNamespace-Context, der dem Dict Attribut-Zugriff gibt.

    Anschließend wird ``assert_no_plaintext()`` ausgeführt — die
    DSGVO-Invariante bleibt auch beim UI-Export erhalten.
    """
    from pathlib import Path

    from jinja2 import Environment, FileSystemLoader, select_autoescape

    from src.reports.privacy import assert_no_plaintext

    _TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "reports" / "templates"
    _TEMPLATE_NAMES = {
        ("executive", "html"): "executive.html.j2",
        ("it_sec", "html"): "it_security.html.j2",
        ("compliance", "html"): "compliance.html.j2",
        ("executive", "markdown"): "executive.md.j2",
        ("it_sec", "markdown"): "it_security.md.j2",
        ("compliance", "markdown"): "compliance.md.j2",
    }

    if (audience, format) not in _TEMPLATE_NAMES:
        raise ValueError(f"Keine Template-Kombination für ({audience}, {format})")

    ctx = _dict_to_namespace(report_data)
    env = Environment(
        loader=FileSystemLoader(_TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "html.j2", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(_TEMPLATE_NAMES[(audience, format)])
    rendered = template.render(ctx=ctx)
    assert_no_plaintext(rendered)
    return rendered


def _dict_to_namespace(obj):
    """Rekursive dict→SimpleNamespace-Konvertierung.

    Erlaubt Jinja2-Templates den Zugriff via ``ctx.summary.total_queries``
    statt ``ctx['summary']['total_queries']``. Listen bleiben Listen,
    deren Einträge werden mitkonvertiert.
    """
    from types import SimpleNamespace

    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_dict_to_namespace(x) for x in obj]
    return obj


def reset_pipeline() -> None:
    """Setzt den Pipeline-State auf empty zurück. Behält Salt-Konfiguration."""
    keys = [
        "uploaded_filename", "uploaded_bytes", "detected_format",
        "report_data", "error_message",
    ]
    for k in keys:
        st.session_state[k] = None
    st.session_state.pipeline_state = "empty"
    # Filter-Keys entfernen (nicht auf [] setzen) — sonst ignoriert Streamlit
    # beim nächsten Render den multiselect-Default und zeigt leere Auswahl.
    for filter_key in ("filter_risk_levels", "filter_frameworks"):
        st.session_state.pop(filter_key, None)
    run_pipeline.clear()


def trigger_analysis() -> None:
    """Liest die hochgeladenen Bytes und startet die Pipeline. Setzt State."""
    fb = st.session_state.uploaded_bytes
    fname = st.session_state.uploaded_filename
    fmt = st.session_state.detected_format
    salt = st.session_state.report_salt
    squid_user_flag = bool(st.session_state.get("squid_username_parsing_enabled"))

    if not fb or not fname or not fmt:
        st.session_state.pipeline_state = "error"
        st.session_state.error_message = "Datei oder Format fehlt."
        return

    st.session_state.pipeline_state = "analyzing"
    try:
        st.session_state.report_data = run_pipeline(
            fb, fname, salt, fmt,
            squid_username_parsing=squid_user_flag,
        )
        st.session_state.pipeline_state = "analyzed"
        st.session_state.error_message = None
        # DSGVO Art. 25: Klartext-Bytes nach Pseudonymisierung im Session-State verwerfen.
        st.session_state.uploaded_bytes = None
    except Exception as exc:
        st.session_state.pipeline_state = "error"
        st.session_state.error_message = f"{type(exc).__name__}: {exc}"
