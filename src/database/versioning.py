"""AI Endpoint Database Versioning und Diff (E1-6, Issue #14).

Semver-basierte Versionierung der ``data/ai_endpoints.json`` mit vollständigen
Snapshots unter ``data/versions/<semver>.json``. Der ``compute_diff``-Helper
produziert strukturierte Delta-Reports (Added / Removed / Changed) zwischen
zwei Versionen, formatiert für CLI oder Reports.

Semver-Konvention (siehe ``data/CHANGELOG_AI_ENDPOINTS.md``):
- MAJOR: Kategorie-Änderungen, Entfernen von Endpoints, Risk-Level-Shift
- MINOR: neue Endpoints, neue Aliases/IP-Ranges, Schema-Erweiterungen
- PATCH: Beschreibung/Metadata-Korrekturen, Source-Attribution
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

_VERSIONS_DIR = Path(__file__).parent.parent.parent / "data" / "versions"

# Felder, die eine strukturell relevante Änderung anzeigen (MAJOR/MINOR-Signal).
_TRACKED_FIELDS = (
    "provider",
    "category",
    "risk_level",
    "domains",
    "aliases",
    "ip_ranges",
    "sni_patterns",
    "detection_confidence",
)


@dataclass(frozen=True)
class EndpointChange:
    """Eine einzelne Änderung an einem Endpoint (service-level)."""
    service: str
    field_name: str
    from_value: object
    to_value: object


@dataclass
class DiffReport:
    """Delta zwischen zwei Endpoint-DB-Versionen."""
    from_version: str
    to_version: str
    added: list[dict] = field(default_factory=list)
    removed: list[dict] = field(default_factory=list)
    changed: list[EndpointChange] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.removed or self.changed)

    def format_text(self) -> str:
        """Menschenlesbarer Text-Report für CLI-Output."""
        lines: list[str] = []
        lines.append(f"# AI Endpoint DB Diff: {self.from_version} → {self.to_version}")
        lines.append("")

        if self.is_empty:
            lines.append("Keine Änderungen.")
            return "\n".join(lines)

        if self.added:
            lines.append(f"## Hinzugefügt ({len(self.added)})")
            for ep in self.added:
                lines.append(
                    f"  + {ep['service']} ({ep['provider']}) — "
                    f"Kategorie {ep['category']}, Risk {ep['risk_level']}"
                )
            lines.append("")

        if self.removed:
            lines.append(f"## Entfernt ({len(self.removed)})")
            for ep in self.removed:
                lines.append(
                    f"  - {ep['service']} ({ep['provider']}) — "
                    f"ehemals Kategorie {ep['category']}"
                )
            lines.append("")

        if self.changed:
            lines.append(f"## Geändert ({len(self.changed)})")
            for change in self.changed:
                lines.append(
                    f"  ~ {change.service}.{change.field_name}: "
                    f"{_format_value(change.from_value)} → "
                    f"{_format_value(change.to_value)}"
                )
            lines.append("")

        return "\n".join(lines)


def _format_value(value: object) -> str:
    if isinstance(value, (list, tuple)):
        if not value:
            return "[]"
        return "[" + ", ".join(str(v) for v in value) + "]"
    return str(value)


def version_path(version: str, versions_dir: Path | None = None) -> Path:
    """Pfad zu einem Versions-Snapshot (z. B. ``data/versions/2.2.0.json``)."""
    return (versions_dir or _VERSIONS_DIR) / f"{version}.json"


def load_version(version: str, versions_dir: Path | None = None) -> dict:
    """Lädt einen Snapshot. Wirft FileNotFoundError mit hilfreichem Hinweis."""
    path = version_path(version, versions_dir)
    if not path.exists():
        available = list_versions(versions_dir)
        hint = (
            f"Verfügbare Versionen: {', '.join(available)}"
            if available
            else "Keine Versions-Snapshots vorhanden — erwarte data/versions/*.json"
        )
        raise FileNotFoundError(f"Snapshot {version} nicht gefunden. {hint}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_versions(versions_dir: Path | None = None) -> list[str]:
    """Gibt eine sortierte Liste aller vorhandenen Versions-Snapshots zurück."""
    base = versions_dir or _VERSIONS_DIR
    if not base.exists():
        return []
    return sorted(p.stem for p in base.glob("*.json"))


def compute_diff(
    from_version: str,
    to_version: str,
    versions_dir: Path | None = None,
) -> DiffReport:
    """Berechnet ein Delta zwischen zwei Snapshot-Versionen."""
    from_db = load_version(from_version, versions_dir)
    to_db = load_version(to_version, versions_dir)
    return diff_databases(from_db, to_db, from_version, to_version)


def diff_databases(
    from_db: dict,
    to_db: dict,
    from_version: str = "",
    to_version: str = "",
) -> DiffReport:
    """Berechnet ein Delta zwischen zwei geladenen DB-Dicts.

    Vergleich basiert auf ``service`` als Primary Key. Normalisiert
    list-basierte Felder (domains, aliases, ...) vor Vergleich, damit
    reine Reihenfolge-Änderungen nicht als Diff auftauchen.
    """
    from_by_service = {e["service"]: e for e in from_db.get("endpoints", [])}
    to_by_service = {e["service"]: e for e in to_db.get("endpoints", [])}

    added_keys = set(to_by_service) - set(from_by_service)
    removed_keys = set(from_by_service) - set(to_by_service)
    common_keys = set(from_by_service) & set(to_by_service)

    added = [to_by_service[k] for k in sorted(added_keys)]
    removed = [from_by_service[k] for k in sorted(removed_keys)]

    changed: list[EndpointChange] = []
    for service in sorted(common_keys):
        old = from_by_service[service]
        new = to_by_service[service]
        for field_name in _TRACKED_FIELDS:
            old_val = _normalize(old.get(field_name))
            new_val = _normalize(new.get(field_name))
            if old_val != new_val:
                changed.append(EndpointChange(
                    service=service,
                    field_name=field_name,
                    from_value=old_val,
                    to_value=new_val,
                ))

    return DiffReport(
        from_version=from_version or str(from_db.get("version", "")),
        to_version=to_version or str(to_db.get("version", "")),
        added=added,
        removed=removed,
        changed=changed,
    )


def _normalize(value: object) -> object:
    """Stabilisiert list-/tuple-Vergleiche (set-basiert, um Reihenfolge zu ignorieren)."""
    if isinstance(value, (list, tuple)):
        return tuple(sorted(value))
    return value
