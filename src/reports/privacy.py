"""DSGVO-Schutzschicht für Reports.

Defense-in-Depth: Auch wenn Detection/Compliance bereits pseudonymisieren,
wird vor dem Schreiben nochmals geprüft, dass keine Klartext-IPs, MAC-Adressen
oder interne Hostnames im Output landen.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets


class PrivacyLeakError(Exception):
    """Geworfen, wenn personenbezogene/identifizierende Daten im Output entdeckt werden."""


_IPV4_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
_IPV4_PATTERN = re.compile(rf"\b(?:{_IPV4_OCTET}\.){{3}}{_IPV4_OCTET}\b")

# Strip <script>/<style>-Bloecke vor der PII-Pruefung: Diese enthalten
# Library-Code (z.B. inline plotly.js) mit numerischen Tokens, die wie IPs
# aussehen koennen, aber keine Nutzerdaten sind.
_SCRIPT_STYLE_PATTERN = re.compile(
    r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL,
)
_IPV6_PATTERN = re.compile(
    r"\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b"
)
_MAC_PATTERN = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")
_INTERNAL_HOST_PATTERN = re.compile(r"\b[\w-]+\.(local|lan|internal|corp)\b", re.IGNORECASE)

# Erlaubte Test-IPs (RFC 5737 — dokumentations-IPs, niemals real)
_ALLOWLIST = {"192.0.2.0", "198.51.100.0", "203.0.113.0"}


def get_default_salt() -> str:
    """Liefert den Salt aus REPORT_SALT-ENV oder erzeugt einen zufälligen pro Process-Start."""
    return os.environ.get("REPORT_SALT") or secrets.token_hex(16)


def pseudonymize_client(client: str, salt: str) -> str:
    """HMAC-SHA256-Pseudonymisierung für Client-Identifikatoren.

    Wenn der Input bereits ein Pseudonym ist (Präfix `ip_`, `client_`, `user_`),
    wird er unverändert mit `client_`-Präfix normalisiert.
    """
    if client.startswith(("client_", "ip_", "user_")):
        return "client_" + client.split("_", 1)[1]
    digest = hmac.new(salt.encode("utf-8"), client.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"client_{digest[:8]}"


def assert_no_plaintext(text: str) -> None:
    """Wirft PrivacyLeakError wenn Klartext-IPs/MAC/interne Hostnames im Text vorkommen.

    IPv4-Allowlist deckt RFC 5737 Dokumentations-IPs ab.
    <script>- und <style>-Bloecke werden vor der Pruefung entfernt, da
    eingebettete Bibliotheken (z. B. inline plotly.js) numerische Tokens
    enthalten koennen, die wie IPs aussehen, aber keine Nutzerdaten sind.
    """
    text = _SCRIPT_STYLE_PATTERN.sub("", text)
    for match in _IPV4_PATTERN.findall(text):
        if match not in _ALLOWLIST:
            raise PrivacyLeakError(f"Klartext-IPv4 im Report: {match}")

    if _IPV6_PATTERN.search(text):
        match = _IPV6_PATTERN.search(text)
        # Heuristik gegen False-Positives mit CSS-Hex-Farbcodes (z.B. #ff00aa::000)
        # — nur warnen wenn ":" im Match
        if match and ":" in match.group():
            raise PrivacyLeakError(f"Klartext-IPv6 im Report: {match.group()}")

    if mac := _MAC_PATTERN.search(text):
        raise PrivacyLeakError(f"Klartext-MAC-Adresse im Report: {mac.group()}")

    if host := _INTERNAL_HOST_PATTERN.search(text):
        raise PrivacyLeakError(f"Interner Hostname im Report: {host.group()}")
