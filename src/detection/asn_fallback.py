"""ASN-Fallback-Detection (E1-7, Issue #15).

Provider-Level-CIDR-Matching als letzter Detection-Fallback, wenn Domain-,
Alias- und Service-IP-Range-Lookup alle fehlschlagen. Matches werden
grundsätzlich als ``low``-Konfidenz geflaggt: ein Treffer auf eine
Provider-IP bedeutet nicht zwangsläufig KI-Nutzung (CDN-Shared-IPs,
Multi-Tenant-Cloud, nicht-KI-Services hinter derselben Anycast-Range).

DSGVO-Hinweis: Nur lokale Cache-Datei ``data/ai_ip_ranges.json``; keine
externen WHOIS-/ASN-Lookups zur Laufzeit.
"""

from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_DB_PATH = Path(__file__).parent.parent.parent / "data" / "ai_ip_ranges.json"


@dataclass(frozen=True)
class AsnMatch:
    """Ergebnis eines Provider-Level-IP-Lookups."""
    provider: str
    service_hint: str
    category: str
    risk_level: str
    source: str
    confidence: str = "low"


class AsnDatabase:
    """Lädt und indiziert Provider-CIDRs aus ``data/ai_ip_ranges.json``.

    Der Index ist eine Liste aus ``(ip_network, match)``-Tupeln. Linearer
    Scan ist ausreichend für O(N<100) Ranges; bei größeren Datasets sollte
    ein Radix-Trie (z. B. ``pytricia``) ersetzt werden.
    """

    def __init__(self, db_path: Path | None = None):
        self._networks: list[tuple[ipaddress._BaseNetwork, AsnMatch]] = []
        self._version: str = ""
        self._updated: str = ""
        self._load(db_path or _DEFAULT_DB_PATH)

    def _load(self, path: Path) -> None:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self._version = data.get("version", "")
        self._updated = data.get("updated", "")
        for provider in data.get("providers", []):
            match = AsnMatch(
                provider=provider["provider"],
                service_hint=provider["service_hint"],
                category=provider["category"],
                risk_level=provider["risk_level"],
                source=provider.get("source", ""),
            )
            for cidr in provider.get("cidrs", []):
                self._networks.append((ipaddress.ip_network(cidr), match))

    @property
    def version(self) -> str:
        return self._version

    @property
    def updated(self) -> str:
        return self._updated

    def lookup(self, ip: str) -> AsnMatch | None:
        """Gibt den Provider-Match für eine IP zurück, oder None.

        Args:
            ip: IPv4- oder IPv6-Adresse als String. Ungültige Werte
                liefern None (kein Raise — Aufrufer dürfen beliebige
                Log-Felder durchreichen).
        """
        try:
            address = ipaddress.ip_address(ip)
        except ValueError:
            return None
        for network, match in self._networks:
            if address.version == network.version and address in network:
                return match
        return None
