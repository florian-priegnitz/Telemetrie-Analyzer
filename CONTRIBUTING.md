# Contributing

Danke, dass du zum **Telemetrie Analyzer** beitragen möchtest. Dieses Dokument erklärt Setup, Konventionen und Review-Prozess.

## Setup

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Tests ausführen:

```bash
pytest tests/ -v
```

Lint + Security:

```bash
ruff check src/ tests/
bandit -r src/ -lll
```

## Branch- & Commit-Konvention

- **Branches:** `sprint-N/<topic>`, z. B. `sprint-8/retention-tuning`
- **Commit-Typen:** `feat`, `fix`, `docs`, `ci`, `chore`, `test`, `refactor` (Conventional-ähnlich)
- **PR-Titel:** `[Sprint N] Titel`
- **PR-Referenzen:** `Closes #N` oder `Refs #N` im Body
- **Merge-Strategie:** Merge-Commit (kein Squash) — Historie bleibt erhalten

Beispiel:

```
feat(retention): apply_retention hook in pipeline

Closes #38
```

## Code-Konventionen

- **Sprache im Code:** Englisch (Funktionen, Variablen, Klassen)
- **Dokumentation & Reports:** Deutsch
- **Formatierung:** `ruff` (Line-Length 110, py311-Target)
- **Typing:** Wo sinnvoll, insbesondere öffentliche Schnittstellen
- **Imports:** via `ruff` (`I`-Regel) automatisch sortiert

## Privacy-by-Design-Invarianten

Diese Regeln gelten projektweit — **jeder PR, der eine davon verletzt, wird abgelehnt**:

1. **HMAC-SHA256-Pseudonymisierung** für alle IPs/Usernames beim Import
2. **`assert_no_plaintext()`** muss in allen Report-Ausgaben laufen
3. **Uploaded-Bytes** werden nach erfolgreicher Pipeline aus Session-State verworfen
4. **Salt-Wechsel** triggert `reset_pipeline()` (Hard-Reset aller Analyse-Daten)
5. **Neue Parser** müssen `BaseParser`-Contract erfüllen (siehe `src/parsers/base.py`) und Path/Username-Felder gemäß DSGVO Art. 25 minimieren
6. **k-Anonymität** (Default k=5) für UI-Drill-Downs

## Tests

- **Mindeststandard:** Neue Features brauchen Tests (pytest)
- **Test-Daten:** synthetisch via `src/testdata/generator.py` — **niemals echte Logs committen**
- **DSGVO-Smoketests:** `tests/test_privacy.py` enthält Klartext-Leak-Assertions, neue Output-Pfade dort ergänzen
- **Parser-Contract:** neue Parser werden automatisch gegen `tests/test_parser_base.py` getestet

## Review-Prozess

1. PR öffnen gegen `main`
2. CI muss grün sein (pytest, ruff, bandit)
3. Mindestens 1 Review für Code-PRs
4. Privacy-relevante PRs (UI, Parser, Reports) erfordern explizites Label `privacy:reviewed`
5. Nach Merge: CHANGELOG-Eintrag im **Unreleased**-Block (wenn noch nicht geschehen)

## Issues

- Bugs: Reproduktions-Schritte, Log-Typ, Scenario-Profil (falls reproduzierbar mit Testdaten)
- Features: Use-Case, betroffene Compliance-Frameworks, vorgeschlagenes Risk-Scoring

## Fragen?

Öffne ein Issue oder schreibe an den Maintainer (siehe `SECURITY.md` für sensible Themen).
