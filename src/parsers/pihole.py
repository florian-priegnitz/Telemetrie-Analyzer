"""Parser für Pi-hole DNS Query Logs → pandas DataFrame.

Pi-hole Log-Format (Standard, /var/log/pihole.log):
    Mar  9 08:15:32 dnsmasq[1234]: query[A] chat.openai.com from 192.168.1.42
    Mar  9 08:15:32 dnsmasq[1234]: query[AAAA] chat.openai.com from 192.168.1.42

Unterstützt auch das Long-Term Query Format (FTL database export / CSV):
    timestamp,type,domain,client,status,dnssec,reply,response_time,cname
"""

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.privacy.pseudonymizer import Pseudonymizer

# Pattern für Standard Pi-hole syslog
_SYSLOG_PATTERN = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"dnsmasq\[\d+\]:\s+query\[(?P<qtype>[A-Z0-9]+)\]\s+"
    r"(?P<domain>\S+)\s+from\s+(?P<client>\S+)"
)

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def parse_pihole_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    year: int | None = None,
) -> pd.DataFrame:
    """Parst ein Pi-hole syslog und gibt ein DataFrame zurück.

    Args:
        source: Pfad zur Log-Datei
        pseudonymizer: Pseudonymizer-Instanz für DSGVO-konforme IP-Maskierung.
                       Wenn None, wird automatisch einer erzeugt.
        year: Jahr für Timestamps (syslog enthält kein Jahr). Default: aktuelles Jahr.

    Returns:
        DataFrame mit Spalten: timestamp, query_type, domain, client, source_file
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()
    if year is None:
        year = datetime.now().year

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _SYSLOG_PATTERN.match(line.strip())
            if not m:
                continue

            month = _MONTHS.get(m.group("month"), 1)
            day = int(m.group("day"))
            time_parts = m.group("time").split(":")
            ts = datetime(
                year, month, day,
                int(time_parts[0]), int(time_parts[1]), int(time_parts[2]),
            )

            records.append({
                "timestamp": ts,
                "query_type": m.group("qtype"),
                "domain": m.group("domain").lower().rstrip("."),
                "client": pseudonymizer.pseudonymize_ip(m.group("client")),
                "source_file": source.name,
            })

    df = pd.DataFrame(records)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def parse_pihole_ftl_csv(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst Pi-hole FTL CSV-Export.

    Erwartet Spalten: timestamp, type, domain, client, status
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    df = pd.read_csv(source)

    required = {"timestamp", "domain", "client"}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Fehlende Spalten im CSV: {missing}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["domain"] = df["domain"].str.lower().str.rstrip(".")
    df["client"] = df["client"].apply(pseudonymizer.pseudonymize_ip)
    df["query_type"] = df.get("type", "A")
    df["source_file"] = source.name

    return df[["timestamp", "query_type", "domain", "client", "source_file"]]
