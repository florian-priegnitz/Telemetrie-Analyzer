"""Pruef-Skript: Existieren alle in docs/screenshots/CHECKLIST.md gelisteten PNGs?

Liest die Markdown-Checkliste, extrahiert PNG-Filenames aus '- [ ] NN_xxx.png'-Zeilen
und prueft `Path.exists()` fuer jede. Default: warn (Exit 0). Mit `--strict` Exit 1
bei fehlenden Files (fuer Release-CI).

Sprint 10D / #75.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHECKLIST = REPO_ROOT / "docs" / "screenshots" / "CHECKLIST.md"
SCREENSHOTS_DIR = REPO_ROOT / "docs" / "screenshots"

# Match `- [ ] 00_filename.png` oder `- [x] 00_filename.png` mit optionalem Trailing-Text.
_LINE_RE = re.compile(r"^\s*-\s*\[(?P<state>[ xX])\]\s+(?P<file>\d{2}_[\w.-]+\.png)\b")


def parse_checklist(checklist_path: Path) -> list[str]:
    """Gib geordnete Liste der erwarteten PNG-Dateinamen zurueck."""
    if not checklist_path.exists():
        return []
    text = checklist_path.read_text(encoding="utf-8")
    expected: list[str] = []
    for line in text.splitlines():
        match = _LINE_RE.match(line)
        if match:
            expected.append(match.group("file"))
    return expected


def check(checklist_path: Path, screenshots_dir: Path) -> tuple[list[str], list[str]]:
    """Liefere (vorhanden, fehlend) als zwei Listen von Dateinamen."""
    expected = parse_checklist(checklist_path)
    present: list[str] = []
    missing: list[str] = []
    for name in expected:
        if (screenshots_dir / name).exists():
            present.append(name)
        else:
            missing.append(name)
    return present, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prueft, ob alle in docs/screenshots/CHECKLIST.md gelisteten PNGs vorliegen."
        )
    )
    parser.add_argument(
        "--checklist", type=Path, default=DEFAULT_CHECKLIST,
        help="Pfad zur CHECKLIST.md (default: docs/screenshots/CHECKLIST.md)",
    )
    parser.add_argument(
        "--screenshots-dir", type=Path, default=SCREENSHOTS_DIR,
        help="Pfad zum Screenshots-Verzeichnis (default: docs/screenshots/)",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit 1 bei fehlenden Files (default: warn + Exit 0)",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Nur Summary ausgeben, keine Datei-Listen",
    )
    args = parser.parse_args()

    if not args.checklist.exists():
        # Doku-PR (#74) ggf. noch nicht gemerged — kein Fehler im Default.
        msg = f"WARN: CHECKLIST.md nicht gefunden unter {args.checklist}"
        print(msg, file=sys.stderr)
        return 1 if args.strict else 0

    present, missing = check(args.checklist, args.screenshots_dir)
    total = len(present) + len(missing)

    if total == 0:
        print(f"WARN: {args.checklist} enthaelt keine '- [ ] NN_*.png' Eintraege.")
        return 1 if args.strict else 0

    if missing and not args.quiet:
        print(f"FEHLEND ({len(missing)}/{total}):", file=sys.stderr)
        for name in missing:
            print(f"  - {args.screenshots_dir.name}/{name}", file=sys.stderr)

    summary = f"OK: {len(present)}/{total}, FEHLEND: {len(missing)}"
    print(summary)

    if missing:
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
