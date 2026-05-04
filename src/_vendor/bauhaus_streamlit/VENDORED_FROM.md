# Vendored Source

Diese Kopie von `bauhaus_streamlit` ist ein Snapshot aus:

- **Repository:** https://github.com/florian-priegnitz/Bauhaus-Streamlit (private)
- **Tag:** v0.1.0
- **Lizenz:** MIT (siehe LICENSE in diesem Verzeichnis)

## Aktualisierung

```bash
rm -rf src/_vendor/bauhaus_streamlit
cp -r ~/projects/bauhaus-streamlit/src/bauhaus_streamlit src/_vendor/
cp ~/projects/bauhaus-streamlit/LICENSE src/_vendor/bauhaus_streamlit/
# Anschliessend in src/_vendor/bauhaus_streamlit/branding.py:
#   files("bauhaus_streamlit") -> files(__package__)
```

Tests laufen weiter, da `from src._vendor.bauhaus_streamlit import ...` der Import-Pfad ist.
