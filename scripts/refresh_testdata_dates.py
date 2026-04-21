"""Shift alle Testdaten-Zeitstempel so, dass sie im aktuellen Retention-Fenster liegen.

Motivation: Die statischen Sample-Logs (cloudflare_gateway, entra_signin,
fortinet, netskope, paloalto, umbrella, zscaler) wurden ursprünglich für
Schreib-/Parser-Tests mit festen Daten (`2024-06-23`) angelegt.
Die 90-Tage-Retention-Policy schneidet sie nun komplett weg.

Dieses Skript kopiert Samples und verschiebt Zeitstempel so, dass der
`base_date` (2024-06-23) auf einen konfigurierbaren Ziel-Tag fällt
(Default: vor 7 Tagen). So entsprechen die Samples einem frischen
Tool-Export und laufen durch die default Retention.

Idempotent — kann bei Bedarf monatlich über die Monthly-Workflow
getriggert werden (via refresh_endpoints.py).

Usage:
    python scripts/refresh_testdata_dates.py          # 7 Tage alt
    python scripts/refresh_testdata_dates.py --days-ago 14
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTDATA = ROOT / "testdata"

# Basis-Datum aller statischen Samples (Text-Format unabhängig)
BASE_DATE = date(2024, 6, 23)

# Affected files (anything else is generator-based or already recent)
FILES_WITH_OLD_DATES = [
    "cloudflare_gateway_sample.log",
    "entra_signin_sample.log",
    "fortinet_sample.log",
    "netskope_sample.log",
    "paloalto_sample.log",
    "umbrella_sample.log",
    "zscaler_sample.log",
]

MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _transform_iso_date(text: str, offset_days: int) -> str:
    """`2024-06-23` → `YYYY-MM-DD` offset-verschoben."""
    pattern = re.compile(r"(20\d{2})-(0[1-9]|1[0-2])-([0-3]\d)")

    def _shift(m: re.Match) -> str:
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return m.group(0)
        return (d + timedelta(days=offset_days)).isoformat()

    return pattern.sub(_shift, text)


def _transform_slash_date(text: str, offset_days: int) -> str:
    """`2024/06/23` → `YYYY/MM/DD` offset-verschoben."""
    pattern = re.compile(r"(20\d{2})/(0[1-9]|1[0-2])/([0-3]\d)")

    def _shift(m: re.Match) -> str:
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return m.group(0)
        return (d + timedelta(days=offset_days)).strftime("%Y/%m/%d")

    return pattern.sub(_shift, text)


def _transform_month_abbr(text: str, offset_days: int) -> str:
    """`23-Jun-2024` → `DD-Mon-YYYY` offset-verschoben (Zscaler NSS Format)."""
    pattern = re.compile(
        r"([0-3]?\d)-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(20\d{2})"
    )

    def _shift(m: re.Match) -> str:
        try:
            month = MONTH_ABBR.index(m.group(2)) + 1
            d = date(int(m.group(3)), month, int(m.group(1)))
        except ValueError:
            return m.group(0)
        shifted = d + timedelta(days=offset_days)
        return f"{shifted.day}-{MONTH_ABBR[shifted.month-1]}-{shifted.year}"

    return pattern.sub(_shift, text)


def _transform_epoch_seconds(text: str, offset_seconds: int) -> str:
    """Netskope: 10-stellige Unix-Epoch-Sekunden (2020–2033 Range).

    Erkennt `1719...` bis `2078...` Muster (keine False-Positives bei
    kleinen Integers wie Portnummern). Nur wenn >= 1_577_836_800 (2020-01-01)
    und <= 3_408_825_600 (2078) wird geshiftet.
    """
    pattern = re.compile(r"\b(1[7-9]\d{8}|20\d{8})\b")

    def _shift(m: re.Match) -> str:
        try:
            epoch = int(m.group(0))
        except ValueError:
            return m.group(0)
        if not 1_577_836_800 <= epoch <= 3_408_825_600:
            return m.group(0)
        return str(epoch + offset_seconds)

    return pattern.sub(_shift, text)


def _transform_epoch_nanoseconds(text: str, offset_seconds: int) -> str:
    """FortiGate: 19-stellige Epoch-Nanosekunden (`1719131733000000000`)."""
    pattern = re.compile(r"\b(1[7-9]\d{17}|20\d{17})\b")

    def _shift(m: re.Match) -> str:
        try:
            epoch_ns = int(m.group(0))
        except ValueError:
            return m.group(0)
        # 2020-01-01 in ns: 1577836800000000000; 2078 in ns: 3408825600000000000
        if not 1_577_836_800_000_000_000 <= epoch_ns <= 3_408_825_600_000_000_000:
            return m.group(0)
        return str(epoch_ns + offset_seconds * 1_000_000_000)

    return pattern.sub(_shift, text)


def refresh(days_ago: int = 7, dry_run: bool = False) -> int:
    target = date.today() - timedelta(days=days_ago)
    offset_days = (target - BASE_DATE).days
    offset_seconds = offset_days * 86400

    print(f"Basis-Datum im Sample: {BASE_DATE.isoformat()}")
    print(f"Ziel-Datum (heute-{days_ago}): {target.isoformat()}")
    print(f"Offset: {offset_days} Tage / {offset_seconds} Sekunden")
    print()

    changed = 0
    for filename in FILES_WITH_OLD_DATES:
        path = TESTDATA / filename
        if not path.is_file():
            print(f"  SKIP  {filename} (nicht gefunden)")
            continue

        before = path.read_text(encoding="utf-8")
        after = before
        after = _transform_iso_date(after, offset_days)
        after = _transform_slash_date(after, offset_days)
        after = _transform_month_abbr(after, offset_days)
        after = _transform_epoch_nanoseconds(after, offset_seconds)
        after = _transform_epoch_seconds(after, offset_seconds)

        if before == after:
            print(f"  NOOP  {filename} (keine Muster getroffen)")
            continue

        if dry_run:
            print(f"  WOULD {filename} ({len(before)}→{len(after)} bytes)")
        else:
            path.write_text(after, encoding="utf-8")
            print(f"  OK    {filename} aktualisiert")
        changed += 1

    print()
    print(f"{changed} von {len(FILES_WITH_OLD_DATES)} Dateien {'zu ändern' if dry_run else 'geändert'}.")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days-ago", type=int, default=7,
                        help="Ziel-Alter der Samples in Tagen (Default: 7)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur anzeigen, nichts schreiben")
    args = parser.parse_args()
    refresh(days_ago=args.days_ago, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
