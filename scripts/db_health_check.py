"""DB-Health-Check fuer ai_endpoints.json.

Loest alle Domains via DNS auf und aggregiert die `source`-Verteilung als
Stale-Proxy (mangels `last_verified`-Feld). Aufruf:

    python scripts/db_health_check.py            # Markdown-Bericht auf stdout
    python scripts/db_health_check.py --json     # JSON-Bericht (fuer Auto-Postings)

Ergebnis-Kategorien:
- ok:       mind. eine Domain pro Service ist DNS-aufloesbar
- partial:  einige Domains aufloesbar, andere nicht
- dead:     KEINE Domain ist aufloesbar
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "ai_endpoints.json"

DNS_TIMEOUT = 3.0
MAX_WORKERS = 32


def host_of(domain: str) -> str:
    """Strippt URL-Pfade und Schema. `slack.com/ai` -> `slack.com`."""
    d = domain.split("://", 1)[-1]
    return d.split("/", 1)[0].rstrip(".")


def resolve(domain: str) -> tuple[str, bool, str]:
    socket.setdefaulttimeout(DNS_TIMEOUT)
    host = host_of(domain)
    try:
        socket.getaddrinfo(host, None)
        return domain, True, ""
    except socket.gaierror as exc:
        return domain, False, f"gaierror: {exc.strerror or exc!s}"
    except TimeoutError:
        return domain, False, "timeout"
    except OSError as exc:
        return domain, False, f"oserror: {exc!s}"


def sweep(endpoints: list[dict]) -> dict[str, dict]:
    domains: dict[str, list[str]] = defaultdict(list)
    for ep in endpoints:
        for d in ep["domains"]:
            domains[d].append(ep["service"])

    results: dict[str, tuple[bool, str]] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(resolve, d): d for d in domains}
        for fut in as_completed(futs):
            domain, ok, err = fut.result()
            results[domain] = (ok, err)

    by_service: dict[str, dict] = {}
    for ep in endpoints:
        ok_count = sum(1 for d in ep["domains"] if results[d][0])
        total = len(ep["domains"])
        if ok_count == total:
            status = "ok"
        elif ok_count == 0:
            status = "dead"
        else:
            status = "partial"
        by_service[ep["service"]] = {
            "status": status,
            "ok": ok_count,
            "total": total,
            "failures": [
                {"domain": d, "error": results[d][1]}
                for d in ep["domains"]
                if not results[d][0]
            ],
            "category": ep["category"],
            "risk": ep["risk_level"],
            "source": ep.get("source", "unknown"),
        }
    return by_service


def render_markdown(db: dict, services: dict[str, dict]) -> str:
    total = len(services)
    counts = Counter(s["status"] for s in services.values())
    sources = Counter(s["source"] for s in services.values())

    out: list[str] = []
    out.append(f"## DB-Health-Check — {db.get('version', '?')} (last_updated {db.get('last_updated', '?')})")
    out.append("")
    out.append(f"**Services geprueft:** {total}")
    out.append(
        f"**Status:** ok {counts.get('ok', 0)} · partial {counts.get('partial', 0)} · dead {counts.get('dead', 0)}"
    )
    out.append("")

    out.append("### Source-Histogramm (Stale-Proxy)")
    out.append("")
    out.append("| Source-Tag | Services |")
    out.append("|------------|---------:|")
    for src, n in sources.most_common():
        out.append(f"| `{src}` | {n} |")
    out.append("")

    dead = sorted(
        ((s, info) for s, info in services.items() if info["status"] == "dead"),
        key=lambda x: (x[1]["risk"], x[0]),
    )
    if dead:
        out.append(f"### Dead Hosts ({len(dead)})")
        out.append("")
        out.append("| Service | Risk | Kategorie | Domains | Fehler |")
        out.append("|---------|------|-----------|---------|--------|")
        for s, info in dead:
            doms = ", ".join(f"`{f['domain']}`" for f in info["failures"])
            errs = "; ".join(sorted({f["error"].split(":", 1)[0] for f in info["failures"]}))
            out.append(f"| {s} | {info['risk']} | {info['category']} | {doms} | {errs} |")
        out.append("")

    partial = sorted(
        ((s, info) for s, info in services.items() if info["status"] == "partial"),
        key=lambda x: (x[1]["risk"], x[0]),
    )
    if partial:
        out.append(f"### Partial Hosts ({len(partial)}) — einzelne Domains tot")
        out.append("")
        out.append("| Service | Risk | OK / Total | Fehlende Domain(s) |")
        out.append("|---------|------|-----------:|--------------------|")
        for s, info in partial:
            doms = ", ".join(f"`{f['domain']}`" for f in info["failures"])
            out.append(f"| {s} | {info['risk']} | {info['ok']}/{info['total']} | {doms} |")
        out.append("")

    if not dead and not partial:
        out.append("**Alle 178 Services sind voll DNS-aufloesbar.**")
        out.append("")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="JSON statt Markdown")
    args = parser.parse_args()

    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    services = sweep(db["endpoints"])

    if args.json:
        print(json.dumps({"db": {"version": db["version"], "last_updated": db["last_updated"]}, "services": services}, indent=2))
    else:
        print(render_markdown(db, services))
    return 0


if __name__ == "__main__":
    sys.exit(main())
