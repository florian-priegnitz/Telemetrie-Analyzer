# Telemetrie Analyzer — Developer Tasks
# Nutzung: `make <target>`. `make help` zeigt alle Targets.

.PHONY: help install dev test lint security sbom docker docker-run \
        clean testdata validate-db analyze-sample pre-commit \
        offline-up offline-down offline-pull verify-screenshots \
        generate-examples check-all

PYTHON ?= python3.11
VENV ?= .venv
ACTIVATE := $(VENV)/bin/activate
IMAGE ?= telemetrie-analyzer:dev
SAMPLE ?= testdata/pihole_sample.log

help: ## Zeigt alle verfügbaren Targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Installiert das Paket samt Dev-Dependencies in ein venv
	$(PYTHON) -m venv $(VENV)
	. $(ACTIVATE) && pip install -U pip && pip install -e ".[dev]"

dev: install ## Alias für install (Developer-Setup)

test: ## Führt alle pytest-Tests aus
	. $(ACTIVATE) && pytest tests/ -v

test-quick: ## pytest ohne verbose Output
	. $(ACTIVATE) && pytest tests/ -q

lint: ## Ruff-Lint auf src/ und tests/
	. $(ACTIVATE) && ruff check src/ tests/

lint-fix: ## Ruff-Auto-Fix
	. $(ACTIVATE) && ruff check --fix src/ tests/

security: ## Bandit-Security-Scan (High/Medium/Low)
	. $(ACTIVATE) && bandit -r src/ -lll

sbom: ## Generiert CycloneDX-SBOM (sbom.cdx.json)
	. $(ACTIVATE) && pip install -q cyclonedx-bom && ./scripts/generate_sbom.sh

validate-db: ## Prüft ai_endpoints.json gegen das Schema
	. $(ACTIVATE) && telemetrie-analyzer validate-db

analyze-sample: ## Analysiert testdata/pihole_sample.log → reports/ (HTML)
	. $(ACTIVATE) && telemetrie-analyzer analyze $(SAMPLE) \
	    --parser pihole --format html --audience all --out reports/

streamlit: ## Startet Streamlit-Dashboard auf :8501
	. $(ACTIVATE) && streamlit run app.py

docker: ## Baut Docker-Image ($(IMAGE))
	docker build -t $(IMAGE) .

docker-run: ## Startet Docker-Container auf :8501
	docker run --rm -p 8501:8501 --env-file .env $(IMAGE)

offline-up: ## Startet Telemetrie-Analyzer + Ollama-Sidecar (Compose-Profile offline)
	docker compose -f docker-compose.yml -f docker-compose.offline.yml --profile offline up -d

offline-down: ## Stoppt den Offline-Stack
	docker compose -f docker-compose.yml -f docker-compose.offline.yml --profile offline down

offline-pull: ## Pulled das Default-Modell (llama3.1:8b) im laufenden Ollama-Container
	docker compose -f docker-compose.yml -f docker-compose.offline.yml --profile offline exec ollama ollama pull $${OLLAMA_MODEL:-llama3.1:8b}

verify-screenshots: ## Prueft Vollstaendigkeit der docs/screenshots/ gegen CHECKLIST.md
	. $(ACTIVATE) && python scripts/verify_screenshots.py

generate-examples: ## Erzeugt 86 Beispiel-Reports (Idempotent, seed=42)
	. $(ACTIVATE) && python scripts/generate_example_reports.py

check-all: ## pytest + ruff + verify-screenshots + generate-examples --check
	. $(ACTIVATE) && pytest tests/ -q
	. $(ACTIVATE) && ruff check src/ tests/ scripts/
	. $(ACTIVATE) && python scripts/verify_screenshots.py
	. $(ACTIVATE) && python scripts/generate_example_reports.py --check

testdata: ## Generiert synthetische Testdaten (enterprise-mixed Szenario)
	. $(ACTIVATE) && python -m src.testdata.generator --scenario enterprise-mixed --format both --seed 42

enrich-samples: ## Erzeugt angereicherte Demo-Samples in testdata/demo/
	. $(ACTIVATE) && python scripts/enrich_samples.py

refresh-testdata-dates: ## Verschiebt Zeitstempel in Samples auf Retention-Fenster
	. $(ACTIVATE) && python scripts/refresh_testdata_dates.py

screenshots: ## README-Screenshots via Playwright (setzt laufende Streamlit-Instanz voraus)
	. $(ACTIVATE) && pip install -q playwright && playwright install chromium
	. $(ACTIVATE) && python scripts/capture_screenshots.py

refresh-endpoints: ## Monthly-Refresh der AI-Endpoint-DB (dry-run)
	. $(ACTIVATE) && python scripts/refresh_endpoints.py --dry-run

pre-commit: ## Installiert pre-commit Hooks ins lokale Repo
	. $(ACTIVATE) && pip install -q pre-commit && pre-commit install

clean: ## Räumt __pycache__, .pytest_cache, build/dist weg
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache build dist *.egg-info htmlcov sbom.cdx.json

.DEFAULT_GOAL := help
