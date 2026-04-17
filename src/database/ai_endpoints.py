"""AI Endpoint Database – Laden und Abfragen bekannter KI-Dienste."""

import json
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class AIEndpoint:
    """Ein bekannter KI-Dienst mit zugehörigen Domains und Risikobewertung."""
    service: str
    provider: str
    category: str
    risk_level: str
    domains: tuple[str, ...]
    description: str


class AIEndpointDatabase:
    """Datenbank bekannter KI-Dienste für Domain-Matching."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "data" / "ai_endpoints.json"
        self._endpoints: list[AIEndpoint] = []
        self._domain_index: dict[str, AIEndpoint] = {}
        self._load(db_path)

    def _load(self, path: Path) -> None:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for entry in data["endpoints"]:
            endpoint = AIEndpoint(
                service=entry["service"],
                provider=entry["provider"],
                category=entry["category"],
                risk_level=entry["risk_level"],
                domains=tuple(entry["domains"]),
                description=entry["description"],
            )
            self._endpoints.append(endpoint)
            for domain in endpoint.domains:
                self._domain_index[domain.lower()] = endpoint

    def lookup(self, domain: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst anhand einer Domain (exaktes Match)."""
        return self._domain_index.get(domain.lower())

    def lookup_subdomain(self, fqdn: str) -> AIEndpoint | None:
        """Findet einen KI-Dienst auch bei Subdomain-Matches.

        Prüft ob die angefragte Domain eine bekannte KI-Domain ist
        oder eine Subdomain davon (z.B. cdn.chat.openai.com → chat.openai.com).
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
        return None

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
