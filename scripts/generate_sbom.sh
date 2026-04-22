#!/usr/bin/env bash
# SBOM-Generator (CycloneDX) — CRA-Vorbereitung (VO EU 2024/2847)
#
# Erzeugt sbom.cdx.json im Projekt-Root. Benötigt `cyclonedx-bom`:
#   pip install cyclonedx-bom

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="${1:-sbom.cdx.json}"

if ! command -v cyclonedx-py >/dev/null 2>&1; then
    echo "ERROR: cyclonedx-py nicht gefunden. Installieren mit:" >&2
    echo "  pip install cyclonedx-bom" >&2
    exit 1
fi

echo "Erzeuge SBOM → $OUT"
cyclonedx-py environment -o "$OUT" 2>/dev/null \
    || cyclonedx-py requirements -o "$OUT" pyproject.toml

echo "Fertig. SBOM-Pfad: $ROOT/$OUT"
echo "Einträge:"
python3 -c "import json; d=json.load(open('$OUT')); print(f\"  components: {len(d.get('components', []))}\")"
