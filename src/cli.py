"""Command-Line Interface für den Telemetrie Analyzer.

Issue #3 (Sprint 3 / reaktiviert in Wave 2). Ermöglicht headless Automation,
z.B. in Cron-Jobs, GitHub Actions oder SIEM-Post-Processing-Skripten, ohne
Streamlit-UI.

Beispiele::

    telemetrie-analyzer analyze testdata/pihole_sample.log \\
        --out reports/ --format html --audience all

    # Kurzform (Auto-Detect, JSON-Output nach stdout):
    telemetrie-analyzer analyze my.log --format json --stdout

    # DB-Validierung:
    telemetrie-analyzer validate-db

Unterstützte Formate werden automatisch erkannt. Bei mehrdeutigen Dateien
kann `--parser` explizit gesetzt werden.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from src.compliance.engine import ComplianceEngine
from src.database.ai_endpoints import AIEndpointDatabase
from src.database.versioning import compute_diff, list_versions
from src.detection.engine import DetectionEngine
from src.parsers.detection import detect_format
from src.privacy.pseudonymizer import Pseudonymizer
from src.privacy.retention import apply_retention, load_policy, summarize
from src.reports import ReportGenerator

_PARSERS: dict[str, Callable[..., Any]] = {}


def _register_parsers() -> None:
    """Lazy-import aller verfügbaren Parser. Vermeidet Import-Overhead für
    `validate-db` und reduziert Coupling zu Streamlit-ABhängigkeiten."""
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

    _PARSERS.update({
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
    })


def _auto_detect_parser(path: Path) -> str:
    """Heuristik-Wrapper um ``detect_format()`` aus ``src/parsers/detection.py``.

    Signatur bleibt erhalten für Rückwärts-Kompatibilität der Tests —
    die eigentliche Heuristik lebt jetzt im Shared-Modul (Single Source
    of Truth für CLI und UI). Bei unbekanntem Format wird analog zur
    alten Signatur eine ``ValueError`` geraist.
    """
    sample_bytes = path.read_bytes()
    if not sample_bytes.strip():
        raise ValueError("Datei ist leer oder enthält nur Whitespace.")
    result = detect_format(sample_bytes)
    if result is None:
        first = sample_bytes[:200].decode("utf-8", errors="replace").splitlines()
        first_line = first[0] if first else ""
        raise ValueError(
            "Parser konnte nicht automatisch erkannt werden. "
            f"Bitte --parser explizit setzen. Erste Zeile: {first_line[:120]!r}"
        )
    return result


def _analyze(args: argparse.Namespace) -> int:
    _register_parsers()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.is_file():
        print(f"ERROR: Input-Datei nicht gefunden: {input_path}", file=sys.stderr)
        return 2

    parser_key = args.parser or _auto_detect_parser(input_path)
    if parser_key not in _PARSERS:
        print(f"ERROR: Unbekannter Parser: {parser_key!r}. "
              f"Verfügbar: {', '.join(sorted(_PARSERS))}", file=sys.stderr)
        return 2

    salt = args.salt or ""
    pseudo = Pseudonymizer(key=salt.encode("utf-8") if salt else None)

    if args.verbose:
        print(f"[cli] Parse {input_path} als {parser_key}", file=sys.stderr)
    df = _PARSERS[parser_key](input_path, pseudonymizer=pseudo)
    if df.empty:
        print(f"ERROR: Keine parsbaren Einträge in {input_path}", file=sys.stderr)
        return 3

    if not args.no_retention:
        policy = load_policy()
        df_trimmed = apply_retention(df, policy, log_type=parser_key)
        summary = summarize(df, df_trimmed, policy, log_type=parser_key)
        if args.verbose:
            print(f"[cli] Retention: {summary['rows_before']} → {summary['rows_after']} Zeilen "
                  f"({summary['rows_dropped']} verworfen, Policy {summary['days']}d)", file=sys.stderr)
        df = df_trimmed
        if df.empty:
            print("ERROR: Nach Retention sind keine Einträge mehr übrig.", file=sys.stderr)
            return 3

    if args.verbose:
        print(f"[cli] {len(df)} Events → DetectionEngine", file=sys.stderr)
    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)

    report_salt = salt or None
    gen = ReportGenerator(detection, compliance, salt=report_salt)

    if args.stdout or args.format == "json":
        from src.reports.context import build_context, context_to_json_dict
        ctx = build_context(detection, compliance, salt=report_salt)
        payload = context_to_json_dict(ctx)
        out_str = json.dumps(payload, indent=2, ensure_ascii=False, default=str)
        if args.stdout:
            sys.stdout.write(out_str + "\n")
        elif args.out:
            out_path = Path(args.out).expanduser()
            out_path.mkdir(parents=True, exist_ok=True)
            (out_path / "report.json").write_text(out_str, encoding="utf-8")
            if args.verbose:
                print(f"[cli] JSON → {out_path / 'report.json'}", file=sys.stderr)
        if args.format == "json":
            return 0

    if args.format in ("html", "markdown"):
        out_path = Path(args.out).expanduser() if args.out else Path("reports")
        out_path.mkdir(parents=True, exist_ok=True)
        paths = gen.write(out_path, audience=args.audience, format=args.format)
        if args.verbose:
            for p in paths if isinstance(paths, list) else [paths]:
                print(f"[cli] {args.format} → {p}", file=sys.stderr)
        else:
            items = paths if isinstance(paths, list) else [paths]
            for p in items:
                print(p)

    return 0


def _validate_db(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve() if args.path else None
    try:
        db = AIEndpointDatabase(db_path=path, validate=True)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {len(db.endpoints)} Endpoints, Schema valid.")
    return 0


def _diff_db(args: argparse.Namespace) -> int:
    """CLI-Handler für ``diff-db`` (#14). Ohne Args: verfügbare Snapshots listen."""
    if not args.from_version or not args.to_version:
        available = list_versions()
        if not available:
            print("Keine Versions-Snapshots unter data/versions/ gefunden.", file=sys.stderr)
            return 1
        print("Verfügbare Endpoint-DB-Versionen:")
        for v in available:
            print(f"  {v}")
        print("\nUsage: telemetrie-analyzer diff-db <from> <to>")
        return 0
    try:
        report = compute_diff(args.from_version, args.to_version)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(report.format_text())
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telemetrie-analyzer",
        description="Shadow-AI-Detection via DNS/Proxy-Log-Analyse.",
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Fortschritts-Logs auf stderr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze",
        help="Log-Datei analysieren und Report erzeugen")
    analyze.add_argument("input", help="Pfad zur Log-Datei")
    analyze.add_argument("--parser", choices=[
        "pihole", "squid", "zscaler", "paloalto", "umbrella", "fortinet",
        "aws_vpc_flow", "entra_id", "cloudflare_gateway", "netskope",
        "sysmon", "elastic_ecs",
    ], help="Parser erzwingen (Default: Auto-Detect)")
    analyze.add_argument("--format", choices=["html", "markdown", "json"],
                         default="html", help="Report-Format (Default: html)")
    analyze.add_argument("--audience", choices=["executive", "it_sec", "compliance", "all"],
                         default="all", help="Zielgruppe (Default: all)")
    analyze.add_argument("--out", "-o",
                         help="Ausgabe-Verzeichnis (Default: reports/)")
    analyze.add_argument("--stdout", action="store_true",
                         help="JSON-Report auf stdout (ignoriert --out)")
    analyze.add_argument("--salt",
                         help="Pseudonymisierungs-Salt (Default: random)")
    analyze.add_argument("--no-retention", action="store_true",
                         help="Retention-Hook überspringen (nur Testing!)")
    analyze.set_defaults(func=_analyze)

    validate = subparsers.add_parser("validate-db",
        help="AI-Endpoint-Database gegen Schema validieren")
    validate.add_argument("--path", help="Alternativer DB-Pfad")
    validate.set_defaults(func=_validate_db)

    diff_db = subparsers.add_parser("diff-db",
        help="Delta-Report zwischen zwei Endpoint-DB-Versionen")
    diff_db.add_argument("from_version", nargs="?",
                         help="Quell-Version (z. B. 2.1.0). Ohne Args: Liste aller Snapshots.")
    diff_db.add_argument("to_version", nargs="?",
                         help="Ziel-Version (z. B. 2.2.0)")
    diff_db.set_defaults(func=_diff_db)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n[cli] abgebrochen", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        if getattr(args, "verbose", False):
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
