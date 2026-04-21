"""Format-Detection + Parser-Registry (Single Source of Truth).

Dieses Modul ist der zentrale Katalog unterstützter Log-Formate und die
gemeinsame Detection-Heuristik für CLI (``src/cli.py``) und UI
(``src/ui/state.py``). Vor dieser Extraktion gab es zwei parallele
Detection-Pfade — das divergierte bereits in v1.0 (UI kannte nur 2
Parser, CLI kannte 12). Jetzt wird aus einer einzigen Quelle gespeist.

**Entry-Points:**
- ``SUPPORTED_PARSERS`` — Tuple aller Parser-Keys, in deterministischer Reihenfolge
- ``PARSER_LABELS`` — Mapping Key → menschlich lesbares Label (UI-Dropdowns)
- ``PARSER_METADATA`` — Erweiterte Metadaten für die 📚 Formate-Page
  (Quelle, Feld-Mapping, Risiko-Signal, Sample-Dateiname)
- ``detect_format(bytes) -> str | None`` — Heuristik, None bei Unbekanntem

**Heuristik-Prinzipien:**
- Erste ~4 KB lesen, decode replace
- Erste 5 nicht-leere Zeilen inspizieren
- Reihenfolge: spezifisch → generisch (JSON-Marker vor JSON-Fallback,
  konkrete CSV-Keywords vor IP-Prefix-Patterns)
- Niemals Exception werfen — bei Mehrdeutigkeit ``None`` zurückgeben,
  UI/CLI bieten dann manuellen Override
"""

from __future__ import annotations

SUPPORTED_PARSERS: tuple[str, ...] = (
    "pihole",
    "squid",
    "zscaler",
    "paloalto",
    "umbrella",
    "fortinet",
    "aws_vpc_flow",
    "entra_id",
    "cloudflare_gateway",
    "netskope",
    "sysmon",
    "elastic_ecs",
)

PARSER_LABELS: dict[str, str] = {
    "pihole": "Pi-hole DNS (dnsmasq Syslog / FTL-CSV)",
    "squid": "Squid Proxy (native / common log)",
    "zscaler": "Zscaler ZIA NSS (TSV Web Proxy)",
    "paloalto": "Palo Alto PAN-OS URL-Filtering (CSV)",
    "umbrella": "Cisco Umbrella DNS Security (CSV)",
    "fortinet": "FortiGate webfilter.log (key=value Syslog)",
    "aws_vpc_flow": "AWS VPC Flow Logs (v2 default / v5 Custom)",
    "entra_id": "Azure Entra ID Sign-In Logs (JSONL)",
    "cloudflare_gateway": "Cloudflare Gateway (DNS + HTTP NDJSON)",
    "netskope": "Netskope CASB/SWG (NDJSON Log Shipper)",
    "sysmon": "Windows Sysmon Event 22 (DNS-Query JSONL)",
    "elastic_ecs": "Elastic Common Schema 8.x (NDJSON)",
}


PARSER_METADATA: dict[str, dict] = {
    "pihole": {
        "source": "Pi-hole DNS-Resolver (dnsmasq) — Syslog oder pihole-FTL CSV-Export",
        "file_type": ".log / .csv",
        "sample_file": "pihole_sample.log",
        "field_mapping": {
            "timestamp (Syslog Mon Tag HH:MM:SS)": "timestamp (aktuelles Jahr unterstellt)",
            "from <IP>": "client (HMAC-pseudonymisiert als `ip_<hash>`)",
            "query[TYPE] <domain>": "domain (lowercase, trailing dot entfernt)",
        },
        "risk_signal": (
            "Client-seitige DNS-Auflösung ist die primäre Spur unmanaged Shadow-AI — "
            "direkte Zuordnung Query → AI-Endpoint-DB."
        ),
    },
    "squid": {
        "source": "Squid Proxy (native access.log oder common log format)",
        "file_type": ".log",
        "sample_file": "squid_sample.log",
        "field_mapping": {
            "ts.ms elapsed": "timestamp (Epoch-Sekunden)",
            "client_ip": "client (HMAC-pseudonymisiert)",
            "url / HIER-Hostname": "domain (lowercase, Pfad getrennt)",
            "bytes (response size)": "bytes_uploaded (für Upload-Heuristik ≥500 KB)",
        },
        "risk_signal": (
            "Proxy-Logs zeigen HTTP-Methode und Volumen — Upload-Heuristik "
            "(≥500 KB POST) markiert Dokumenten-Abflüsse zu LLM-APIs."
        ),
    },
    "zscaler": {
        "source": "Zscaler ZIA NSS (Nanolog Streaming Service) — TSV Web Proxy Log",
        "file_type": ".log (TAB-separiert)",
        "sample_file": "zscaler_sample.log",
        "field_mapping": {
            "login": "user (HMAC-pseudonymisiert als `user_<hash>`)",
            "ciip": "client (HMAC-pseudonymisiert als `ip_<hash>`)",
            "url": "domain + url_path (Query-String-Strip, DSGVO Art. 25)",
            "urlcategory / urlclass": "urlcategory",
            "reqsize / respsize": "bytes_uploaded / bytes_downloaded",
        },
        "risk_signal": (
            "Zscaler kategorisiert AI-Apps als `Generative AI` oder `ChatGPT` — "
            "plus URL-Filter-Entscheidung (Allow/Block) → Policy-Audit-Spur."
        ),
    },
    "paloalto": {
        "source": "Palo Alto PAN-OS URL-Filtering Log (threat/url csv über Syslog oder panlog)",
        "file_type": ".csv (komma-separiert, Syslog-Prefix möglich)",
        "sample_file": "paloalto_sample.log",
        "field_mapping": {
            "receive_time (2024/06/23 08:15:32)": "timestamp",
            "src": "client",
            "url / category": "domain + urlcategory",
            "srcuser": "user (wenn User-ID aktiv)",
            "action (allow/block/continue)": "action",
        },
        "risk_signal": (
            "PAN-OS URL-Filter klassifiziert Tool-Kategorie — Regel-Entscheidung "
            "ist direkt für DORA Art. 28 (Third-Party-Policy) relevant."
        ),
    },
    "umbrella": {
        "source": "Cisco Umbrella DNS Security — CSV Export aus dem Umbrella-Dashboard",
        "file_type": ".csv (quoted, mit Header)",
        "sample_file": "umbrella_sample.log",
        "field_mapping": {
            "timestamp": "timestamp",
            "most_granular_identity (user/computer/AD)": "user / client (pseudonymisiert je Identity-Type)",
            "external_ip": "client (Fallback)",
            "domain": "domain",
            "categories": "urlcategory",
            "action (Allowed/Blocked)": "action",
        },
        "risk_signal": (
            "Cloud-DNS mit Identity-Awareness — verknüpft AI-Lookups "
            "mit AD-Benutzer/Rollen, wichtig für Asset-Inventar (ISO 27001 A.5.9)."
        ),
    },
    "fortinet": {
        "source": "FortiGate webfilter.log — Syslog key=value Format",
        "file_type": ".log (key=value, syslog prefix möglich)",
        "sample_file": "fortinet_sample.log",
        "field_mapping": {
            "eventtime (Epoch-ns)": "timestamp (mit Fallback auf date+time)",
            "srcip": "client",
            "user": "user",
            "hostname / url": "domain",
            "cat / catdesc": "urlcategory",
            "action (passthrough/blocked)": "action",
        },
        "risk_signal": (
            "UTM-Webfilter sieht TLS-SNI auch ohne Proxy-MITM — deckt "
            "direkte AI-API-Zugriffe (ohne Webseite) auf."
        ),
    },
    "aws_vpc_flow": {
        "source": "AWS VPC Flow Logs (v2 default oder v5 Custom mit pkt-*-aws-service)",
        "file_type": ".log (space-separiert; v5 mit Header-Zeile)",
        "sample_file": "aws_vpc_v5_sample.log",
        "field_mapping": {
            "start (Epoch)": "timestamp",
            "srcaddr": "client",
            "dstaddr / pkt-dst-aws-service": "domain (Service-Name wenn v5 vorhanden)",
            "bytes": "bytes_uploaded (pro Flow-Summe)",
            "action (ACCEPT/REJECT)": "action",
        },
        "risk_signal": (
            "Layer-4-Signal für cloud-native AI-Services (Bedrock, SageMaker, "
            "API-Gateway-Endpoints) — ohne Layer-7 dennoch AI-Service-zuordenbar."
        ),
    },
    "entra_id": {
        "source": "Azure Entra ID Sign-In Logs — JSONL Export aus Entra Monitoring",
        "file_type": ".json / .jsonl",
        "sample_file": "entra_signin_sample.log",
        "field_mapping": {
            "TimeGenerated / CreatedDateTime": "timestamp",
            "UserPrincipalName": "user",
            "IPAddress": "client",
            "AppDisplayName": "domain (App-Name, via Alias-Lookup in Detection)",
            "Status (success/failure)": "action (3-Wege success/blocked/failed)",
        },
        "risk_signal": (
            "Entra-Sign-Ins zeigen OAuth-/SSO-Nutzung von AI-SaaS-Apps — "
            "Alias-Match `ChatGPT Enterprise` / `GitHub Copilot` per AppDisplayName."
        ),
    },
    "cloudflare_gateway": {
        "source": "Cloudflare Gateway Logpush — NDJSON (DNS + HTTP in einer Datei)",
        "file_type": ".log (NDJSON)",
        "sample_file": "cloudflare_gateway_sample.log",
        "field_mapping": {
            "Datetime": "timestamp",
            "Email / UserID": "user",
            "SrcIP / DeviceID": "client",
            "QueryName / HTTPHost": "domain (DNS- oder HTTP-Variante)",
            "QueryCategoryIDs / PolicyName": "urlcategory",
            "Action (allow/block)": "action",
            "source_type": "Differenzierung `dns` vs `http` pro Zeile",
        },
        "risk_signal": (
            "Cloudflare Zero Trust Gateway — kombiniert DNS + HTTP in einer Quelle, "
            "ideal für Remote-Mitarbeiter ohne Corporate-Proxy."
        ),
    },
    "netskope": {
        "source": "Netskope CASB/SWG — NDJSON Log Shipper (Application Events)",
        "file_type": ".log (NDJSON)",
        "sample_file": "netskope_sample.log",
        "field_mapping": {
            "_insertion_epoch_timestamp / timestamp": "timestamp (Epoch-s oder -ms)",
            "user": "user",
            "src_ip / userip": "client",
            "hostname / app": "domain (Service-Name als Fallback)",
            "activity (Prompt/Completion/Upload File)": "activity (AI-spezifisches Signal)",
            "appcategory": "urlcategory",
        },
        "risk_signal": (
            "Netskope klassifiziert 1.550+ AI-Apps nativ — Activity 'Upload File' "
            "bei AI-App zeigt Datenabfluss-Risiko (DSGVO Art. 32)."
        ),
    },
    "sysmon": {
        "source": "Windows Sysmon Event ID 22 (DNS Query) — JSONL via evtx2json / Winlogbeat",
        "file_type": ".json / .jsonl",
        "sample_file": "sysmon_sample.log",
        "field_mapping": {
            "UtcTime / @timestamp": "timestamp",
            "Computer / host.name": "client (HMAC-pseudonymisiert als `ip_<hash>`)",
            "QueryName": "domain",
            "User (DOMAIN\\user)": "user",
            "Image (voller Pfad)": "process (nur Basename, DSGVO Art. 25)",
            "QueryStatus": "status_code",
        },
        "risk_signal": (
            "Endpunkt-zentrisches DNS-Log mit Prozess-Attribution — "
            "zeigt welches Executable die AI-Query abgesetzt hat."
        ),
    },
    "elastic_ecs": {
        "source": "Elastic Common Schema 8.x NDJSON — universeller Fallback-Parser",
        "file_type": ".log / .ndjson",
        "sample_file": "elastic_ecs_sample.log",
        "field_mapping": {
            "@timestamp": "timestamp",
            "source.ip / client.ip": "client",
            "dns.question.name / url.domain": "domain",
            "user.name / user.email": "user",
            "http.request.method / status_code": "method / status_code",
            "http.request.body.bytes": "bytes_uploaded",
        },
        "risk_signal": (
            "ECS ist vendor-agnostisch — deckt jede Quelle ab, die als Beat, "
            "Logstash oder SIEM-Connector nach ECS exportiert (Fallback-Parser)."
        ),
    },
}


def _head_sample(sample_bytes: bytes, max_bytes: int = 4096) -> tuple[str, list[str]]:
    text = sample_bytes[:max_bytes].decode("utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return text, lines[:5]


def detect_format(sample_bytes: bytes) -> str | None:
    """Erkennt das Log-Format anhand der ersten ~4 KB.

    Args:
        sample_bytes: Rohe Bytes der Log-Datei (nur der Anfang wird inspiziert).

    Returns:
        Parser-Key aus ``SUPPORTED_PARSERS`` oder ``None`` wenn kein
        Format sicher zugeordnet werden kann. CLI und UI sollen in diesem
        Fall einen manuellen Override anbieten.

    Reihenfolge-Begründung: JSON-Marker zuerst (eindeutige Felder sind hart),
    danach Syslog-Signaturen, zuletzt CSV/TSV-Heuristiken (mehrdeutig).
    """
    if not sample_bytes:
        return None

    _text, head_lines = _head_sample(sample_bytes)
    if not head_lines:
        return None

    first = head_lines[0]
    first_lower = first.lower()

    # ---- JSON-Shape: spezifische Marker-Keys pro Provider ----
    if first.startswith("{"):
        # Cloudflare Gateway: `Datetime` + `SrcIP` + `QueryName` (DNS)
        # oder `HTTPHost`/`PolicyName` (HTTP-Variante)
        if '"datetime"' in first_lower and (
            '"srcip"' in first_lower or '"queryname"' in first_lower
            or '"httphost"' in first_lower or '"policyname"' in first_lower
            or '"querycategoryid"' in first_lower
        ):
            return "cloudflare_gateway"
        # Netskope: `_insertion_epoch_timestamp` ist eindeutig
        if '"_insertion_epoch_timestamp"' in first_lower or (
            '"appcategory"' in first_lower and '"activity"' in first_lower
        ):
            return "netskope"
        # Entra Sign-In: UserPrincipalName + TimeGenerated/CreatedDateTime
        if '"userprincipalname"' in first_lower or '"appdisplayname"' in first_lower \
                or '"signinactivity"' in first_lower:
            return "entra_id"
        # Sysmon: EventID=22 + QueryName ODER sysmon-Block
        if '"queryname"' in first_lower and (
            '"eventid"' in first_lower or '"utctime"' in first_lower
            or '"winlog"' in first_lower or '"sysmon"' in first_lower
        ):
            return "sysmon"
        # Elastic ECS: @timestamp + event.category/event.type (nested oder flat)
        if '"@timestamp"' in first_lower and (
            '"event"' in first_lower or '"ecs"' in first_lower
            or '"event.category"' in first_lower
        ):
            return "elastic_ecs"
        # Generische Sysmon (EventID-Feld): Fallback
        if '"eventid"' in first_lower and '"utctime"' in first_lower:
            return "sysmon"
        return None

    # ---- Syslog / key=value / bekannte Line-Strukturen ----

    # Pi-hole dnsmasq Syslog
    if "dnsmasq[" in first and "query[" in first:
        return "pihole"

    # FortiGate webfilter.log — key=value mit date=/type=
    if "date=" in first_lower and 'type="utm"' in first_lower:
        return "fortinet"
    if "date=" in first_lower and "subtype=\"webfilter\"" in first_lower:
        return "fortinet"

    # Palo Alto PAN-OS CSV — "N,YYYY/MM/DD HH:MM:SS,serial,THREAT,url,..."
    # Erkennungsmuster: Kommata UND zweites Feld sieht aus wie PAN-OS-Timestamp
    parts = first.split(",")
    if len(parts) >= 5 and _looks_like_panos_timestamp(parts[1] if len(parts) > 1 else ""):
        if "threat" in first_lower or "url" in first_lower:
            return "paloalto"

    # AWS VPC Flow v2: "2 account-id eni-... srcip dstip ..."
    if first.startswith(("2 ", "3 ")) and first.count(" ") >= 10:
        return "aws_vpc_flow"

    # AWS VPC Flow v5 Header-Zeile: "version account-id interface-id srcaddr..."
    if first.startswith("version ") and "srcaddr" in first_lower and "dstaddr" in first_lower:
        return "aws_vpc_flow"

    # Squid Native: Epoch-Timestamp mit Millisekunden als erstes Feld
    # Beispiel: "1719131732.123    42 10.0.1.42 TCP_MISS/200 ..."
    if "." in first[:15]:
        ts_candidate = first.split()[0] if first.split() else ""
        if _is_epoch_float(ts_candidate):
            return "squid"

    # Zscaler NSS TSV: "DD-Mon-YYYY HH:MM:SS\tlogin\tciip\thttps://..."
    if "\t" in first and first.count("\t") >= 4:
        # Validiere Tag-Monat-Jahr-Prefix
        if _looks_like_zscaler_timestamp(first[:20]):
            return "zscaler"

    # Cisco Umbrella CSV: quoted Header mit "timestamp","identity",...
    if first.startswith('"') and "most_granular_identity" in first_lower:
        return "umbrella"
    # Umbrella ohne Header (reine Datenzeile) — ersten 5 Zeilen prüfen
    for line in head_lines:
        if '"most_granular_identity"' in line.lower() or (
            line.startswith('"') and '"identities"' in line.lower()
        ):
            return "umbrella"

    return None


def _looks_like_panos_timestamp(s: str) -> bool:
    """Check ob s = 'YYYY/MM/DD HH:MM:SS' ist (PAN-OS Format)."""
    if len(s) < 19:
        return False
    try:
        date_part, time_part = s[:19].split(" ", 1)
        yyyy, mm, dd = date_part.split("/")
        hh, mi, ss = time_part.split(":")
        return all(p.isdigit() for p in (yyyy, mm, dd, hh, mi, ss))
    except (ValueError, IndexError):
        return False


def _looks_like_zscaler_timestamp(prefix: str) -> bool:
    """Check ob prefix = 'DD-Mon-YYYY HH:MM:SS' (Zscaler NSS Format)."""
    # Beispiel: "23-Jun-2024 08:15:32"
    months = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
    try:
        date_part = prefix.split(" ", 1)[0]
        dd, mon, yyyy = date_part.split("-")
        return dd.isdigit() and mon in months and yyyy.isdigit() and len(yyyy) == 4
    except (ValueError, IndexError):
        return False


def _is_epoch_float(s: str) -> bool:
    """Check ob s ein Squid-Style-Epoch-Float ist (10 Stellen . 3+ Stellen)."""
    if "." not in s:
        return False
    try:
        int_part, frac_part = s.split(".", 1)
        return (len(int_part) == 10 and int_part.isdigit()
                and len(frac_part) >= 3 and frac_part.isdigit())
    except ValueError:
        return False
