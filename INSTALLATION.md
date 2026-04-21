# Installation

Drei Wege zum laufenden Telemetrie Analyzer — wähle den, der zu dir passt.

## Option A — Docker (empfohlen)

**Voraussetzungen:** Docker + Docker Compose (Desktop ≥ 4.0 oder Engine ≥ 24).

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
cp .env.example .env        # optional: ANTHROPIC_API_KEY + PSEUDONYM_SALT setzen
docker compose up --build
```

→ UI unter **http://localhost:8501**

Logs persistieren: bind mounts `./reports` und `./uploads` im `docker-compose.yml`.

## Option B — Python venv (Entwicklung)

**Voraussetzungen:** Python 3.11 oder 3.12, `pip`.

### Linux / macOS

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
streamlit run app.py
```

### Windows (WSL2, empfohlen)

```powershell
wsl --install              # falls nicht vorhanden
```

Dann in WSL wie unter Linux.

### Windows (nativ)

```powershell
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
streamlit run app.py
```

## Option C — Python-API (headless Integration)

```bash
pip install git+https://github.com/florian-priegnitz/Telemetrie-Analyzer@v1.0.0
```

Anschließend Python-Skript (siehe [README.md](README.md) → „Reports CLI-frei").

## Konfiguration (Environment-Variablen)

| Variable | Zweck | Default |
|----------|-------|---------|
| `ANTHROPIC_API_KEY` | Optional: aktiviert Claude-API-Analyzer für KI-gestützte Finding-Annotation | leer → Skip-Mode |
| `REPORT_SALT` | HMAC-Salt für Report-Pseudonymisierung | zufällig pro Prozess |
| `PSEUDONYM_SALT` | HMAC-Salt für Import-Pseudonymisierung | zufällig pro Prozess |
| `RETENTION_DAYS` | Default-Retention (DSGVO Art. 5) | `90` |
| `RETENTION_CONFIG` | Pfad zu alternativer `retention.yaml` | `config/retention.yaml` |

**Wichtig:** Für reproduzierbare Pseudonyme über mehrere Sessions hinweg einen **festen Salt** setzen. **Niemals echte Salts committen** — `.env` ist in `.gitignore`.

## Erste Schritte

```bash
# 1. Testdaten generieren
python -m src.testdata.generator --scenario enterprise-mixed --format both

# 2. UI starten
streamlit run app.py

# 3. Im Browser: Sidebar → Log-Upload → testdata/pihole_sample.log → "Analyse starten"
```

Detaillierter Walkthrough: [docs/QUICKSTART.md](docs/QUICKSTART.md)

## Troubleshooting

**Fehler `ModuleNotFoundError: No module named 'src'`:** venv nicht aktiviert oder `pip install -e .` nicht ausgeführt.

**Streamlit startet, aber UI leer:** Prüfen, ob die Log-Datei dem erwarteten Format entspricht. Sidebar zeigt Fehler-Status.

**Docker-Build scheitert:** Stelle sicher, dass `buildx` aktiviert ist (`docker buildx version`).

**Claude-API antwortet nicht:** Ohne `ANTHROPIC_API_KEY` läuft der Analyzer im Skip-Mode (keine KI-Annotation — Reports sind weiterhin komplett).
