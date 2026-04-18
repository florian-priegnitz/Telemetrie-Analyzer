"""AI Endpoint Database – Laden und Abfragen bekannter KI-Dienste.

Schema v2 (2026-04): neue optionale Felder aliases, ip_ranges, sni_patterns,
detection_confidence, last_verified, source. Backward-kompatibel zu v1.
"""

from __future__ import annotations

import fnmatch
import ipaddress
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AIEndpoint:
    """Ein bekannter KI-Dienst mit zugehörigen Domains und Risikobewertung.

    Schema v2 ergänzt optionale Felder (alle mit sinnvollen Defaults).
    """
    service: str
    provider: str
    category: str
    risk_level: str
    domains: tuple[str, ...]
    description: str = ""
    # v2-Felder (alle optional)
    aliases: tuple[str, ...] = field(default_factory=tuple)
    ip_ranges: tuple[str, ...] = field(default_factory=tuple)
    sni_patterns: tuple[str, ...] = field(default_factory=tuple)
    detection_confidence: str = "high"
    last_verified: str | None = None
    source: str = "manual"


class AIEndpointDatabase:
    """Datenbank bekannter KI-Dienste für Domain/Alias/SNI/IP-Matching."""

    def __init__(self, db_path: Path | None = None, validate: bool = False):
        """Initialisiert die DB aus einer JSON-Datei.

        Args:
            db_path: Pfad zur DB (default: data/ai_endpoints.json)
            validate: Wenn True, wird die DB gegen ai_endpoints_schema.json validiert
                      (erfordert jsonschema). Bei Fehlern: ValueError.
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "data" / "ai_endpoints.json"
        self._endpoints: list[AIEndpoint] = []
        self._domain_index: dict[str, AIEndpoint] = {}
        self._alias_index: dict[str, AIEndpoint] = {}
        self._ip_networks: list[tuple[ipaddress._BaseNetwork, AIEndpoint]] = []
        self._sni_patterns: list[tuple[str, AIEndpoint]] = []
        self._load(db_path, validate=validate)

    def _load(self, path: Path, validate: bool) -> None:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if validate:
            self._validate_schema(data, path.parent / "ai_endpoints_schema.json")

        for entry in data["endpoints"]:
            endpoint = AIEndpoint(
                service=entry["service"],
                provider=entry["provider"],
                category=entry["category"],
                risk_level=entry["risk_level"],
                domains=tuple(entry["domains"]),
                description=entry.get("description", ""),
                aliases=tuple(entry.get("aliases", [])),
                ip_ranges=tuple(entry.get("ip_ranges", [])),
                sni_patterns=tuple(entry.get("sni_patterns", [])),
                detection_confidence=entry.get("detection_confidence", "high"),
                last_verified=entry.get("last_verified"),
                source=entry.get("source", "manual"),
            )
            self._endpoints.append(endpoint)
            for domain in endpoint.domains:
                self._domain_index[domain.lower()] = endpoint
            for alias in endpoint.aliases:
                self._alias_index[alias.lower()] = endpoint
            for cidr in endpoint.ip_ranges:
                try:
                    self._ip_networks.append((ipaddress.ip_network(cidr, strict=False), endpoint))
                except ValueError:
                    # Ungültige CIDR ignorieren — Schema-Validator fängt das
                    # bei validate=True bereits ab.
                    pass
            for pattern in endpoint.sni_patterns:
                self._sni_patterns.append((pattern.lower(), endpoint))

    @staticmethod
    def _validate_schema(data: dict, schema_path: Path) -> None:
        """Validiert DB-Struktur gegen JSON-Schema. Bei Fehler: ValueError."""
        try:
            import jsonschema
        except ImportError as exc:
            raise ImportError(
                "jsonschema nicht installiert — pip install jsonschema"
            ) from exc

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema nicht gefunden: {schema_path}")

        with open(schema_path, encoding="utf-8") as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as exc:
            raise ValueError(f"AI-Endpoint-DB verletzt Schema: {exc.message}") from exc

    # ---- Lookup-Methoden ---------------------------------------------------

    def lookup(self, domain: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst anhand einer Domain (exaktes Match)."""
        return self._domain_index.get(domain.lower())

    def lookup_subdomain(self, fqdn: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst auch bei Subdomain-Matches.

        Prüft ob die angefragte Domain eine bekannte KI-Domain ist oder eine
        Subdomain davon (z.B. cdn.chat.openai.com → chat.openai.com).
        Fallback: SNI-Pattern-Match (Wildcards wie *.openai.com).
        """
        fqdn = fqdn.lower().rstrip(".")
        # Exaktes Match
        if result := self._domain_index.get(fqdn):
            return result
        # Subdomain-Match: schrittweise Labels entfernen
        parts = fqdn.split(".")
        for i in range(1, len(parts) - 1):
            parent = ".".join(parts[i:])
            if result := self._domain_index.get(parent):
                return result
        # SNI-Pattern-Fallback (Wildcards)
        for pattern, endpoint in self._sni_patterns:
            if fnmatch.fnmatch(fqdn, pattern):
                return endpoint
        return None

    def lookup_alias(self, alias: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst anhand eines Aliases (case-insensitive)."""
        return self._alias_index.get(alias.lower())

    def lookup_ip(self, ip: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst anhand einer IP (CIDR-Match der ip_ranges).

        Nur für Endpoints mit eingetragenen ip_ranges. Typischer Fallback
        wenn DNS-/Proxy-Logs keine Domain liefern (z.B. AWS VPC Flow Logs).
        """
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return None
        for network, endpoint in self._ip_networks:
            if addr in network:
                return endpoint
        return None

    # ---- Utility-Properties -----------------------------------------------

    @property
    def endpoints(self) -> list[AIEndpoint]:
        return list(self._endpoints)

    @property
    def domains(self) -> set[str]:
        return set(self._domain_index.keys())

    def by_category(self, category: str) -> list[AIEndpoint]:
        return [e for e in self._endpoints if e.category == category]

    def by_risk_level(self, level: str) -> list[AIEndpoint]:
        return [e for e in self._endpoints if e.risk_level == level]
