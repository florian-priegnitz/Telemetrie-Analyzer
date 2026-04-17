"""Log-Parser für verschiedene Quellen (Pi-hole DNS, Squid Proxy, ...)."""

from src.parsers.pihole import parse_pihole_log, parse_pihole_ftl_csv
from src.parsers.squid import parse_squid_log

__all__ = ["parse_pihole_log", "parse_pihole_ftl_csv", "parse_squid_log"]
