# CI Style-Guide — Telemetrie Analyzer

*TELEMETRIE · CI · 2026-05-18*

━━━━━━━━━━━━ ─ ▪

Dieses Dokument beschreibt die CI-Konventionen für UI, Reports und Doku
des Telemetrie-Analyzers. Das Design-System heißt **TA Design System**
(Kurzform **TA-CI**). Source-of-Truth für die Design-Tokens ist das
Modul [`src/ui/branding.py`](../../src/ui/branding.py) und die zugehörige
[`src/ui/static/branding.css`](../../src/ui/static/branding.css);
HTML-Reports embeden seit Sprint 13b (#91) die Tokens inline in
[`src/reports/templates/base.html.j2`](../../src/reports/templates/base.html.j2)
ohne externen Font- oder JS-Call.

Geltungsbereich: Streamlit-UI, HTML-Reports, Markdown-Reports, neue Doku-Seiten.

## Inhalt

1. [Designprinzipien](#designprinzipien)
2. [Farb-Tokens](#farb-tokens)
3. [Schriften](#schriften)
4. [Spacing](#spacing)
5. [Severity-Skala (4-stufig)](#severity-skala-4-stufig)
6. [Compliance-Status-Mapping](#compliance-status-mapping)
7. [Branding-API](#branding-api)
8. [Lineal-Bildmarke](#lineal-bildmarke)
9. [Markdown-Konventionen](#markdown-konventionen)
10. [Mikro-Konventionen](#mikro-konventionen)

## Designprinzipien

- **Reduktion vor Dekoration.** Keine Schatten, Gradienten, Rundungen, Farbverläufe.
- **Kein Schwarz als Hintergrund.** Hintergrund ist `#FFFFFF`, Text ist `#0C1A32`
  (Ink-Blue). Hohe Lesbarkeit ist Pflicht.
- **Geometrische Akzente.** Lineal-Bildmarke (Bar · Linie · Quadrat) statt Logo.
- **Mono für Maschinendaten.** Monospaced-Schrift für Hashes, IDs, Salt-Fingerprints,
  Achsen-Ticks.
- **Sans für Inhalt.** Heading-Hierarchie via Schriftgewicht (700 / 900) statt
  Farbänderung.
- **Audit-Tauglichkeit.** HTML-Reports rendern self-contained, ohne externe
  HTTP-Calls (kein CDN, keine Google-Fonts) — verifiziert durch den Test
  `test_default_html_has_no_external_http_calls` in
  [`tests/test_reports.py`](../../tests/test_reports.py).

### Namens-Konvention

Das Design-System heißt **TA Design System** (Lang) bzw. **TA-CI** (Kurz, im
Fließtext und in Commit-Messages). Der CSS-Klassen-Präfix ist `.ta-*` und ist
projekt-spezifisch — andere Projekte (cloud-monitor, civicLens etc.) sollten
beim Übernehmen der Tokens einen eigenen Präfix wählen, nicht `.ta-*` mit-
kopieren.

## Farb-Tokens

| Token | Hex | Verwendung |
|-------|-----|------------|
| `--c-bg` | `#FFFFFF` | Page-Background |
| `--c-layer` | `#F6F8FC` | Sidebar, Code-Inline-Background |
| `--c-ink` | `#0C1A32` | Body-Text, Borders |
| `--c-bright` | `#060D1E` | Headings (h1-h4) |
| `--c-acc` | `#9B4A2F` | Rostrot — Akzent, Primary-Buttons, Bullets |
| `--c-gold` | `#B07A10` | Lineal-Quadrat, Severity Medium |
| `--c-green` | `#1A6B3A` | Compliance-Status Compliant |
| `--c-mid` | `rgba(12, 26, 50, 0.09)` | Plot-Gridlines |
| `--c-line` | `rgba(12, 26, 50, 0.16)` | Sidebar-Border, Tab-Underlines |

Streamlit-Theme-Mapping (`.streamlit/config.toml`):

```toml
[theme]
primaryColor = "#9B4A2F"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F6F8FC"
textColor = "#0C1A32"
font = "sans serif"
```

## Schriften

| Token | Stack | Verwendung |
|-------|-------|------------|
| `--font-sans` | `'DM Sans', system-ui, -apple-system, sans-serif` | Body, Headings |
| `--font-mono` | `'Share Tech Mono', ui-monospace, 'Courier New', monospace` | Code, Achsen-Ticks, Mono-Meta-Blocks |

DM Sans wird via `@import` von Google Fonts geladen (Streamlit-UI; nur dort,
weil ein laufender Browser ohnehin online ist). HTML-Reports (Sprint 13b, #91)
nutzen ausschließlich den System-Stack — kein externer Font-Call, weil die
Reports als Audit-Artefakt auch offline lesbar sein müssen. Markdown-Reports
verwenden keine Fonts (System-Default des jeweiligen Viewers).

## Spacing

8px-basiertes Raster mit 4px-Halbschritt:

| Token | Pixel |
|-------|------:|
| `--s-1` | 4 |
| `--s-2` | 8 |
| `--s-3` | 12 |
| `--s-4` | 16 |
| `--s-5` | 20 |
| `--s-6` | 24 |
| `--s-7` | 28 |
| `--s-8` | 32 |
| `--s-9` | 48 |
| `--s-10` | 64 |

## Severity-Skala (4-stufig)

| Level | Hex | CSS-Klasse | Verwendung |
|-------|-----|------------|------------|
| `critical` | `#9B4A2F` | `.ta-sev-critical` | Risk-Score 80–100, sofortige Aktion |
| `high` | `#C26B4A` | `.ta-sev-high` | Risk-Score 60–79, 30-Tage-Maßnahme |
| `medium` | `#B07A10` | `.ta-sev-medium` | Risk-Score 30–59, Quartals-Review |
| `low` | `rgba(12, 26, 50, 0.40)` | `.ta-sev-low` | Risk-Score 0–29, Inventar-Hinweis |

Programmierschnittstelle:

```python
from src.ui.branding import severity_color, SEVERITY_COLORS

severity_color("critical")    # -> "#9B4A2F"
SEVERITY_COLORS["high"]       # -> "#C26B4A"
```

## Compliance-Status-Mapping

| Status | Hex | CSS-Klasse |
|--------|-----|------------|
| `compliant` | `#1A6B3A` | `.ta-status-compliant` |
| `partially_compliant` | `#B07A10` | `.ta-status-partial` |
| `non_compliant` | `#9B4A2F` | `.ta-status-non-compliant` |
| `needs_review` | `rgba(12, 26, 50, 0.40)` | (Severity-Low) |

Programmierschnittstelle:

```python
from src.ui.branding import compliance_status_color, COMPLIANCE_STATUS_COLORS

compliance_status_color("compliant")  # -> "#1A6B3A"
```

## Branding-API

Alle Branding-Symbole werden aus `src.ui.branding` exportiert:

### Streamlit-Integration — Minimal-Beispiel

```python
import streamlit as st
from src.ui.branding import (
    inject_global_css,
    render_lineal,
    FAVICON_PATH,
)

st.set_page_config(
    page_title="Telemetrie Analyzer",
    page_icon=str(FAVICON_PATH),
    layout="wide",
)
inject_global_css()

with st.sidebar:
    render_lineal()
    st.title("Telemetrie")

st.header("Findings")
```

### Plotly-Integration

```python
import plotly.graph_objects as go
from src.ui.branding import get_plotly_template

fig = go.Figure(data=[...])
fig.update_layout(**get_plotly_template()["layout"])
```

`get_plotly_template()` liefert Colorway, Achsen-Style, Mono-Tickfonts und einen
sequenziellen Color-Scale (Layer-Hellgrau → Hellrostrot → Rostrot).

## Lineal-Bildmarke

Die Lineal-Bildmarke ersetzt das klassische Logo. Drei Segmente in fester Geometrie:

```
[ 6px Rostrot Bar ─────── 2px Ink Linie ─── 16px Gold Quadrat ]
```

CSS-Klassen (`.ta-lineal__bar`, `.ta-lineal__line`, `.ta-lineal__square`) werden
von `render_lineal()` ausgegeben. Verwendungsregeln:

- **Streamlit-UI:** 1× pro Page-Load am Anfang der Sidebar (oder oberhalb des
  Main-Title-Blocks).
- **HTML-Reports:** Im Page-Header oberhalb des Titels — als CSS-Block
  (`.ta-lineal__bar` / `__line` / `__square`), gerendert direkt in
  [`base.html.j2`](../../src/reports/templates/base.html.j2#L289).
- **Markdown-Reports:** ASCII-Approximation `━━━━━━━━━━━━ ─ ▪` zwischen Mono-
  Meta-Block und Title (siehe `partials/_md_header.md.j2`).

Maximal 1 Lineal pro logischer Section. Nicht inflationär einsetzen.

## Markdown-Konventionen

Das Partial [`src/reports/templates/partials/_md_header.md.j2`](../../src/reports/templates/partials/_md_header.md.j2)
definiert das Standard-Header-Macro für alle Markdown-Reports:

```jinja
{%- from "partials/_md_header.md.j2" import render with context -%}
{{ render("Executive Summary — Shadow AI Telemetrie", "Executive Summary") }}
```

Render-Output (gekürzt):

```
*TELEMETRIE · EXECUTIVE SUMMARY · 2026-05-04*

━━━━━━━━━━━━ ─ ▪

# Executive Summary — Shadow AI Telemetrie

Generiert: **04.05.2026 07:20 UTC**

> **DSGVO:** Alle Client-Identifikatoren sind pseudonymisiert (HMAC-SHA256). Salt-Fingerprint: `3f61df3c`
```

Die Mono-Meta-Zeile (Audience · Datum) eröffnet den Report; das ASCII-Lineal
trennt Mono-Meta vom Title; die DSGVO-Note schliesst den Header ab.

## Mikro-Konventionen

### Bullets in Streamlit-Markdown

Streamlit rendert Markdown-Listen automatisch im CI-Stil — Standardpunkt wird
durch eine 10×2 Pixel breite Rostrot-Bar ersetzt (definiert in `branding.css`).
**Nicht** mit Custom-CSS überschreiben.

### Code-Inline und Code-Blocks

Inline-Code (`` `…` ``) hat Layer-Hintergrund (`--c-layer`), Blöcke (` ``` `) haben
einen 2px Rostrot-Linker am linken Rand. Keine zusätzlichen Block-Border.

### Tabs (Streamlit)

Tabs nutzen Mono-Schrift in Uppercase mit 0.08em Letter-Spacing. Aktive Tab-
Lasche hat Ink-Blue-Hintergrund, weiße Schrift. Wird via `branding.css`
automatisch geladen.

### KPI-Tiles (`st.metric`)

Werte rendern in DM Sans 900 + Bright-Ink (`#060D1E`). Labels rendern in Share
Tech Mono 10px Uppercase mit 0.14em Letter-Spacing in Rostrot.

### Bullets-Heuristik in Markdown-Reports (Plain MD)

Markdown-Reports werden **rohe** als `.md` ausgeliefert (kein Streamlit-Render).
Hier gilt der Markdown-Default. Keine Custom-Bullets in roher Markdown.

## Verwandte Dokumente

- [`src/ui/branding.py`](../../src/ui/branding.py) — Branding-API (inject_global_css, render_lineal, severity_color, get_plotly_template, FAVICON_PATH)
- [`src/ui/static/branding.css`](../../src/ui/static/branding.css) — CSS-Tokens und Komponenten-Klassen
- [`src/reports/templates/base.html.j2`](../../src/reports/templates/base.html.j2) — HTML-Report-Master mit inline-Tokens (Sprint 13b)
- [`src/reports/templates/partials/_md_header.md.j2`](../../src/reports/templates/partials/_md_header.md.j2) — Markdown-Header-Partial
- [`CHANGELOG.md`](../../CHANGELOG.md) — Versionshistorie der Branding-Sprints

## Sprint-Historie

| Sprint | PR | Datum | Inhalt |
|--------|----|-------|--------|
| 13a | #85 | 2026-05-04 | TA-CI auf Streamlit-UI (config.toml, branding.css, render_lineal, plotly_theme) |
| 13b | #94 | 2026-05-18 | HTML-Reports auf TA-CI; offline=True als Default; plotly.js once-per-report; assert_no_plaintext hardening |
| 13c | (in Arbeit) | — | Markdown-Header-Partial, dieser Style-Guide, 21 Demo-Screenshots |
