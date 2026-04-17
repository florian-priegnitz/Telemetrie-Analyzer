"""DSGVO-konforme Pseudonymisierung mit HMAC-SHA256."""

import hashlib
import hmac
import secrets


class Pseudonymizer:
    """Pseudonymisiert personenbezogene Daten (IPs, Usernamen) mit HMAC-SHA256.

    Der Schlüssel wird pro Analyse-Session generiert oder kann extern
    vorgegeben werden. Gleicher Input + gleicher Schlüssel = gleicher Output,
    sodass Korrelationen erhalten bleiben.
    """

    def __init__(self, key: bytes | None = None):
        self._key = key or secrets.token_bytes(32)

    def pseudonymize(self, value: str, prefix: str = "") -> str:
        """Erzeugt ein HMAC-SHA256-Pseudonym.

        Args:
            value: Der zu pseudonymisierende Wert (IP, Username, etc.)
            prefix: Optionaler Präfix zur Lesbarkeit (z.B. "ip_", "user_")

        Returns:
            Pseudonymisierter String, z.B. "ip_a3f8c1d2"
        """
        digest = hmac.new(self._key, value.encode("utf-8"), hashlib.sha256).hexdigest()
        short = digest[:8]
        return f"{prefix}{short}"

    def pseudonymize_ip(self, ip: str) -> str:
        return self.pseudonymize(ip, prefix="ip_")

    def pseudonymize_user(self, username: str) -> str:
        return self.pseudonymize(username, prefix="user_")

    @property
    def key(self) -> bytes:
        return self._key
