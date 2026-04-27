"""Erzeugt Beispiel-Reports fuer alle 12 Parser unter examples/test_reports/.

Sprint 10B / #73. Vertriebs- + Demo- + Audit-Bundle: pro Parser ein Set von
A+B-Reports gemaess der 108-Zellen-Klassifikation aus dem Sprint-10-Plan.
Zusaetzlich KRITIS-KMU-Sonderfall fuer Squid (50 User, ausgepraegte Schatten-KI).

Aufruf:
    python scripts/generate_example_reports.py
    python scripts/generate_example_reports.py --check          # Existenz pruefen, kein Schreiben
    python scripts/generate_example_reports.py --only squid     # nur ein Parser

Idempotent (seed=42 fuer KRITIS-KMU).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.compliance.engine import ComplianceEngine  # noqa: E402
from src.detection.engine import DetectionEngine  # noqa: E402
from src.parsers.aws_vpc_flow import VPCFlowLogsParser  # noqa: E402
from src.parsers.cloudflare_gateway import CloudflareGatewayParser  # noqa: E402
from src.parsers.elastic_ecs import ElasticECSParser  # noqa: E402
from src.parsers.entra_id import EntraIDSignInParser  # noqa: E402
from src.parsers.fortinet import FortiGateWebfilterParser  # noqa: E402
from src.parsers.netskope import NetskopeCASBParser  # noqa: E402
from src.parsers.paloalto import PanOSUrlParser  # noqa: E402
from src.parsers.pihole import parse_pihole_log  # noqa: E402
from src.parsers.squid import SquidParser  # noqa: E402
from src.parsers.sysmon import SysmonParser  # noqa: E402
from src.parsers.umbrella import UmbrellaDNSParser  # noqa: E402
from src.parsers.zscaler import ZscalerParser  # noqa: E402
from src.reports.generator import ReportGenerator  # noqa: E402
from src.testdata.generator import generate_squid_log  # noqa: E402

EXAMPLES_DIR = REPO_ROOT / "examples" / "test_reports"
TESTDATA_DIR = REPO_ROOT / "testdata"


@dataclass(frozen=True)
class ParserSpec:
    name: str
    sample: Path
    parse: Callable
    audiences: tuple[tuple[str, str], ...]  # (audience, format) Liste der A+B-Zellen


def _parser_call(parser_class):
    """Wrapper that lets us call .parse() on instance-based parsers like a function."""
    return lambda path: parser_class().parse(path)


# A+B-Klassifikation aus Sprint-10-Plan (108-Zellen-Matrix).
# C/D-Zellen werden NICHT geschrieben.
_STANDARD_AUDIENCES: tuple[tuple[str, str], ...] = (
    ("executive", "html"),    # A
    ("executive", "markdown"),  # B
    ("it_sec", "html"),       # A
    ("it_sec", "markdown"),    # B
    ("compliance", "html"),    # A
    ("compliance", "markdown"),  # A
    # JSON wird einmal pro Parser geschrieben — IT-Sec/Compliance teilen sich die Datei
    ("__json__", "json"),     # B
)

# entra_id / elastic_ecs: Exec MD = C → weglassen
_NO_EXEC_MD: tuple[tuple[str, str], ...] = tuple(
    cell for cell in _STANDARD_AUDIENCES if cell != ("executive", "markdown")
)

# aws_vpc_flow: Compliance MD/JSON = C, Compliance HTML = B (behalten)
_AWS_VPC_FLOW: tuple[tuple[str, str], ...] = tuple(
    cell for cell in _STANDARD_AUDIENCES
    if cell not in {("compliance", "markdown"), ("__json__", "json")}
)

# sysmon: Exec MD = D (nicht generieren), Exec HTML = B (behalten)
_SYSMON: tuple[tuple[str, str], ...] = tuple(
    cell for cell in _STANDARD_AUDIENCES if cell != ("executive", "markdown")
)

# elastic_ecs: Exec MD = C, Comp JSON = C
_ELASTIC: tuple[tuple[str, str], ...] = tuple(
    cell for cell in _STANDARD_AUDIENCES
    if cell not in {("executive", "markdown"), ("__json__", "json")}
)


PARSERS: dict[str, ParserSpec] = {
    "pihole": ParserSpec(
        "pihole", TESTDATA_DIR / "pihole_sample.log", parse_pihole_log, _STANDARD_AUDIENCES,
    ),
    "squid": ParserSpec(
        "squid", TESTDATA_DIR / "squid_sample.log", _parser_call(SquidParser), _STANDARD_AUDIENCES,
    ),
    "zscaler": ParserSpec(
        "zscaler", TESTDATA_DIR / "zscaler_sample.log", _parser_call(ZscalerParser), _STANDARD_AUDIENCES,
    ),
    "paloalto": ParserSpec(
        "paloalto", TESTDATA_DIR / "paloalto_sample.log", _parser_call(PanOSUrlParser), _STANDARD_AUDIENCES,
    ),
    "umbrella": ParserSpec(
        "umbrella", TESTDATA_DIR / "umbrella_sample.log", _parser_call(UmbrellaDNSParser), _STANDARD_AUDIENCES,
    ),
    "fortinet": ParserSpec(
        "fortinet", TESTDATA_DIR / "fortinet_sample.log", _parser_call(FortiGateWebfilterParser), _STANDARD_AUDIENCES,
    ),
    "aws_vpc_flow": ParserSpec(
        "aws_vpc_flow", TESTDATA_DIR / "aws_vpc_v5_sample.log", _parser_call(VPCFlowLogsParser), _AWS_VPC_FLOW,
    ),
    "entra_id": ParserSpec(
        "entra_id", TESTDATA_DIR / "entra_signin_sample.log", _parser_call(EntraIDSignInParser), _NO_EXEC_MD,
    ),
    "cloudflare_gateway": ParserSpec(
        "cloudflare_gateway", TESTDATA_DIR / "cloudflare_gateway_sample.log",
        _parser_call(CloudflareGatewayParser), _STANDARD_AUDIENCES,
    ),
    "netskope": ParserSpec(
        "netskope", TESTDATA_DIR / "netskope_sample.log", _parser_call(NetskopeCASBParser), _STANDARD_AUDIENCES,
    ),
    "sysmon": ParserSpec(
        "sysmon", TESTDATA_DIR / "sysmon_sample.log", _parser_call(SysmonParser), _SYSMON,
    ),
    "elastic_ecs": ParserSpec(
        "elastic_ecs", TESTDATA_DIR / "elastic_ecs_sample.log", _parser_call(ElasticECSParser), _ELASTIC,
    ),
}


_FILE_EXT = {"html": "html", "markdown": "md", "json": "json"}


def _expected_files(spec: ParserSpec, prefix: str = "") -> list[Path]:
    """Liste der zu erzeugenden Dateipfade fuer einen Parser-Lauf."""
    out_dir = EXAMPLES_DIR / spec.name
    files: list[Path] = []
    for audience, fmt in spec.audiences:
        ext = _FILE_EXT[fmt]
        if audience == "__json__":
            files.append(out_dir / f"{prefix}report.json")
        else:
            files.append(out_dir / f"{prefix}report_{audience}.{ext}")
    return files


def _run_pipeline(spec: ParserSpec, sample_override: Path | None = None) -> ReportGenerator:
    sample = sample_override or spec.sample
    df = spec.parse(sample)
    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    return ReportGenerator(detection, compliance)


def _write_reports(gen: ReportGenerator, spec: ParserSpec, prefix: str = "") -> list[Path]:
    out_dir = EXAMPLES_DIR / spec.name
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    json_written = False
    for audience, fmt in spec.audiences:
        ext = _FILE_EXT[fmt]
        if audience == "__json__":
            if json_written:
                continue
            data = gen.render(format="json")
            path = out_dir / f"{prefix}report.json"
            import json as _json
            path.write_text(
                _json.dumps(data, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            json_written = True
        else:
            content = gen.render(audience=audience, format=fmt)
            path = out_dir / f"{prefix}report_{audience}.{ext}"
            path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def _generate_kritis_kmu_log() -> Path:
    """Erzeugt das KRITIS-KMU-50-User-Squid-Log unter examples/test_reports/squid/."""
    out_dir = EXAMPLES_DIR / "squid"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "kritis_kmu_50users_raw.log"
    generate_squid_log(
        path,
        days=14,
        queries_per_day=800,
        seed=42,
        scenario="kritis-kmu-shadow-ai",
    )
    return path


def _generate_kritis_kmu_reports() -> list[Path]:
    """KRITIS-KMU bekommt 9 Reports (3 Audiences x 3 Formate, alle = A)."""
    log_path = _generate_kritis_kmu_log()
    spec = PARSERS["squid"]
    gen = _run_pipeline(spec, sample_override=log_path)

    out_dir = EXAMPLES_DIR / "squid"
    written: list[Path] = []
    import json as _json
    for audience in ("executive", "it_sec", "compliance"):
        for fmt in ("html", "markdown"):
            content = gen.render(audience=audience, format=fmt)
            ext = _FILE_EXT[fmt]
            path = out_dir / f"kritis_kmu_50users_{audience}.{ext}"
            path.write_text(content, encoding="utf-8")
            written.append(path)
    data = gen.render(format="json")
    path = out_dir / "kritis_kmu_50users_report.json"
    path.write_text(
        _json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    written.append(path)
    return written


def cmd_generate(only: str | None = None) -> int:
    """Erzeugt alle Reports."""
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, spec in PARSERS.items():
        if only and name != only:
            continue
        if not spec.sample.exists():
            print(f"  SKIP {name} (Sample fehlt: {spec.sample})")
            continue
        print(f"  {name} … ", end="", flush=True)
        gen = _run_pipeline(spec)
        files = _write_reports(gen, spec)
        print(f"{len(files)} Reports")
        total += len(files)

    if only is None or only == "squid":
        print("  squid (KRITIS-KMU 50 User) … ", end="", flush=True)
        files = _generate_kritis_kmu_reports()
        print(f"{len(files)} Reports + 1 Raw-Log")
        total += len(files)

    print(f"\nFertig: {total} Reports unter {EXAMPLES_DIR.relative_to(REPO_ROOT)}/")
    return 0


def cmd_check(only: str | None = None) -> int:
    """Listet erwartete Files und prueft Existenz."""
    missing: list[Path] = []
    present = 0
    for name, spec in PARSERS.items():
        if only and name != only:
            continue
        for path in _expected_files(spec):
            if path.exists():
                present += 1
            else:
                missing.append(path)
    # KRITIS extras
    if only is None or only == "squid":
        kritis_dir = EXAMPLES_DIR / "squid"
        for fname in (
            "kritis_kmu_50users_raw.log",
            "kritis_kmu_50users_report.json",
            "kritis_kmu_50users_executive.html",
            "kritis_kmu_50users_executive.md",
            "kritis_kmu_50users_it_sec.html",
            "kritis_kmu_50users_it_sec.md",
            "kritis_kmu_50users_compliance.html",
            "kritis_kmu_50users_compliance.md",
        ):
            p = kritis_dir / fname
            if p.exists():
                present += 1
            else:
                missing.append(p)

    if missing:
        print(f"FEHLEND ({len(missing)}):")
        for p in missing:
            print(f"  - {p.relative_to(REPO_ROOT)}")
        print(f"\nVorhanden: {present}, Fehlend: {len(missing)}")
        return 1
    print(f"OK: {present}/{present} Reports vorhanden.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--check", action="store_true", help="nur Existenz pruefen, nichts schreiben")
    parser.add_argument(
        "--only", choices=sorted(PARSERS.keys()),
        help="nur einen einzelnen Parser bearbeiten",
    )
    args = parser.parse_args()
    if args.check:
        return cmd_check(args.only)
    return cmd_generate(args.only)


if __name__ == "__main__":
    raise SystemExit(main())
