"""DSGVO-konforme Pseudonymisierung mit HMAC-SHA256."""

import hashlib
import hmac
import secrets


def normalize_username(raw: str) -> str:
    """Normalisiert Username-Input vor der Pseudonymisierung.

    Strippt Domain-Präfixe und -Suffixe, damit `DOMAIN\\user`, `user@corp.tld`
    und `user` auf dasselbe Pseudonym abbilden. Notwendig, damit User-Level-
    Korrelation über unterschiedliche Auth-Schemata hinweg funktioniert, ohne
    den Klartext der Domain-Kennung zu verewigen.

    Formate:
    - ``DOMAIN\\user``  → ``user``  (Windows NT / AD down-level)
    - ``user@corp.tld`` → ``user``  (UPN / E-Mail)
    - ``CN=user,OU=...``→ ``user``  (LDAP DN, CN-Teil)
    - alles andere      → unverändert getrimmt + lowercase
    """
    value = (raw or "").strip()
    if not value:
        return ""
    if "\\" in value:
        value = value.rsplit("\\", 1)[-1]
    if "@" in value:
        value = value.split("@", 1)[0]
    if value.lower().startswith("cn="):
        value = value[3:].split(",", 1)[0]
    return value.lower()


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
        """Pseudonymisiert einen Username nach vorheriger Normalisierung.

        ``normalize_username`` eliminiert Auth-Provider-spezifische
        Präfixe/Suffixe, damit `DOMAIN\\jdoe`, `jdoe@corp.tld` und `jdoe`
        deterministisch auf dasselbe `user_<hash>` fallen. Leerer Input
        liefert leeren String zurück (kein `user_`-Pseudonym auf "").
        """
        normalized = normalize_username(username)
        if not normalized:
            return ""
        return self.pseudonymize(normalized, prefix="user_")

    @property
    def key(self) -> bytes:
        return self._key
