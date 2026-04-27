# Offline-KI-Setup mit Docker + Ollama

Der Telemetrie-Analyzer kann die KI-gestützte Analyse-Stufe (Risk-Bewertung, Handlungsempfehlungen, Executive Summary) wahlweise gegen die **Anthropic-Cloud** oder einen **lokal gehosteten Ollama-Server** fahren. Diese Anleitung zeigt, wie der Offline-Modus eingerichtet wird.

## 1. Warum offline?

| Treiber | Konsequenz |
|---|---|
| **DSGVO Art. 28** (Auftragsverarbeitung) | Auch pseudonymisierte Daten bleiben personenbezogen. Ein Cloud-LLM-Anbieter wird zum Auftragsverarbeiter und braucht einen AVV (Art. 28 Abs. 3). Offline-Betrieb eliminiert die Drittparteien-Verarbeitung. |
| **DORA Art. 28** (ICT-Drittparteien-Risiken) | Finanzdienstleister müssen ICT-Drittparteien (inkl. Cloud-LLM) registrieren und Konzentrationsrisiken überwachen. Ollama-on-Premise vermeidet das Drittparteien-Register komplett. |
| **EU CRA** (Reg. 2024/2847) | Cyber-Resilience-Anforderungen schlagen auf alle ICT-Komponenten durch — interne Modelle sind besser auditierbar als externe APIs. |
| **KRITIS / Daten-Lokationsgebote** | Sektoren wie Energie, Gesundheit, kommunale Verwaltung verlangen häufig Daten-Verarbeitung in der EU oder on-premises. Anthropic-API ist EU-hosted, aber das Verlassen des Perimeters ist trotzdem dokumentationspflichtig. |
| **Kostenkontrolle** | Bei systematischer Nutzung in größeren Umgebungen wird API-Volumen zum Posten. |

Wichtig: Auch im Offline-Modus bleiben die Privacy-Invarianten (HMAC-Pseudonymisierung, k-Anonymität, `assert_no_plaintext`) wirksam. Offline ersetzt nicht die Privacy-Maßnahmen — es addiert eine zweite Schutzschicht (Daten verlassen das Netz nicht).

## 2. Quickstart

```bash
# Variante A: lokaler Ollama-Service (manuell)
ollama serve &
ollama pull llama3.1:8b
LLM_BACKEND=ollama streamlit run app.py

# Variante B: Docker-Compose (kommt in Issue #75)
docker compose --profile offline up -d
docker compose --profile offline exec ollama ollama pull llama3.1:8b
# UI: http://localhost:8501
```

Anschließend in der UI unter **⚙️ Einstellungen → KI-Backend** auf "Ollama (Offline)" umschalten oder vorab via Env-Variable `LLM_BACKEND=ollama` konfigurieren.

## 3. Backend-Konfiguration

Selection-Logik (in [src/analyzer/backends/__init__.py](../src/analyzer/backends/__init__.py)):

1. Explizites `LLM_BACKEND`-Env oder Settings-UI-Auswahl
2. Auto: `anthropic` wenn `ANTHROPIC_API_KEY` gesetzt
3. Sonst Skip-Mode (Reports ohne LLM-Empfehlungen)

| Env-Variable | Default | Wirkung |
|---|---|---|
| `LLM_BACKEND` | `anthropic` (mit Key) bzw. `skip` | `anthropic` \| `ollama` \| `skip` |
| `ANTHROPIC_API_KEY` | — | Pflicht für `anthropic`. Ohne Key fällt Auto auf `skip` zurück. |
| `OLLAMA_HOST` | `http://localhost:11434` | Endpoint des Ollama-Servers |
| `OLLAMA_MODEL` | `llama3.1:8b` | Modellname (muss vorab `ollama pull`-ed sein) |
| `OLLAMA_TIMEOUT` | `120` | Sekunden für Chat-Requests; bei großen Modellen erhöhen |

Beispiel `.env` (Offline):

```bash
LLM_BACKEND=ollama
OLLAMA_HOST=http://ollama:11434      # Compose-internes Hostname
OLLAMA_MODEL=qwen2.5:14b
OLLAMA_TIMEOUT=240
```

## 4. Modell-Empfehlungen

Indikative Werte — die tatsächliche Latenz hängt von CPU/GPU, RAM und Modell-Quantisierung ab. Werte beziehen sich auf den **Risk-Assessment-Prompt** (~3 KB Input, ~1.5 KB Output, JSON-Antwort).

| Modell | RAM-Bedarf | Latenz | Genauigkeit (subjektiv) | Empfohlen für |
|---|---|---|---|---|
| `llama3.1:8b` | ~16 GB | ~5–10 s | gut für Klassifikation, Empfehlungen okay | **KMU / Standard-Hardware** |
| `qwen2.5:14b` | ~32 GB | ~15–25 s | bessere Strukturierung, stärker bei Compliance-Begriffen | mittlere Unternehmen / DSFA-relevante Reports |
| `mixtral:8x7b` | ~48 GB | ~20–30 s | nahe an Cloud-Modellen für strukturierte Aufgaben | Enterprise / Audit-Pack |
| `llama3.1:70b` (4-bit) | ~64 GB | ~30–60 s | sehr nah an Anthropic-Sonnet für Risk-Bewertung | wenn Hardware vorhanden |

Pulling:

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:14b
ollama pull mixtral:8x7b
ollama list                  # zeigt installierte Modelle
```

## 5. Privacy-Vorteile gegenüber Cloud-Modus

| Schutzebene | Cloud (Anthropic) | Offline (Ollama) |
|---|---|---|
| HMAC-SHA256-Pseudonymisierung | ✅ aktiv | ✅ aktiv |
| k-Anonymitäts-Hard-Redaktion | ✅ aktiv | ✅ aktiv |
| `assert_no_plaintext()` über Reports | ✅ aktiv | ✅ aktiv |
| Daten verlassen das eigene Netz | ❌ JA (an Anthropic) | ✅ NEIN |
| Drittparteien-AVV erforderlich | ✅ JA (Anthropic) | ❌ entfällt |
| ICT-Drittparteien-Register (DORA) | ✅ JA | ❌ entfällt |
| Audit-Trail vollständig lokal | ❌ Logs nur Anthropic-seitig | ✅ vollständig im Netz |

Ollama-Backend leakt keine Daten an externe APIs — die einzigen ausgehenden Requests gehen an `OLLAMA_HOST` (per Default localhost). In abgeschotteten Netzen kann der Compose-Stack komplett ohne Internet-Zugang gefahren werden, sobald die Modell-Dateien einmal vorgehalten sind.

## 6. Troubleshooting

**Symptom:** "Ollama nicht erreichbar unter http://localhost:11434"
- Server läuft? `curl http://localhost:11434/api/tags` muss JSON zurückgeben.
- In Docker-Compose: `docker compose --profile offline ps` zeigt Service-Status.
- Firewall / Port-Belegung prüfen.

**Symptom:** "Ollama HTTP 404: model 'llama3.1:8b' not found"
- Modell wurde nicht gepulled. `ollama pull llama3.1:8b` ausführen.
- Bei Compose: `docker compose --profile offline exec ollama ollama pull llama3.1:8b`.

**Symptom:** Timeout-Fehler bei langen Reports / vielen Findings
- `OLLAMA_TIMEOUT` erhöhen (z. B. `300` für 14B-Modelle).
- Kleineres Modell wählen oder Hardware aufstocken.

**Symptom:** Out-of-Memory beim Modell-Laden
- Kleineres Modell (`llama3.1:8b` statt `qwen2.5:14b`).
- Ollama unterstützt 4-bit-Quantisierungen mit `:q4_0`-Suffix für noch geringeren RAM-Bedarf.

**Fallback ohne Backend:** Wenn weder Anthropic noch Ollama verfügbar sind, läuft der Analyzer im **Skip-Mode** weiter. Detection, Compliance-Mapping und Report-Generierung funktionieren ohne LLM-Anreicherung — die Reports enthalten dann keine LLM-generierten Risikobewertungen und Handlungsempfehlungen, die übrigen Sections (Findings, Compliance-Mappings, KPIs) bleiben vollständig.

## 7. Verweise

- Implementation: [src/analyzer/backends/ollama_backend.py](../src/analyzer/backends/ollama_backend.py) (stdlib-`urllib`, keine `httpx`-Dependency)
- UI-Auswahl: [src/ui/pages/settings.py](../src/ui/pages/settings.py) (Block "KI-Backend" mit Live-Verbindungs-Test)
- Privacy-Engineering: [docs/PRIVACY.md](PRIVACY.md)
- Tests: [tests/test_llm_backends.py](../tests/test_llm_backends.py), [tests/test_analyzer_backend_dispatch.py](../tests/test_analyzer_backend_dispatch.py)
- Issues: [#72](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues/72) (Backend-Implementierung), [#75](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues/75) (DevOps-Stack)
