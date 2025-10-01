# Pull Request

## Summary
<!-- What changed and why? Keep it tight. -->

## Changes
- [ ] Data (docs/page_data/*, figures_*.json, images/)
- [ ] Wrappers / index (docs/*.html, data-index.html)
- [ ] Scripts (scripts/*.py)
- [ ] GPT docs (gpt/*)
- [ ] Other (describe)

## Test Plan
- [ ] Opened `https://jason-vaughan.github.io/barcoach-assets/data-index.html`
- [ ] Checked affected JSON endpoints return **200**
  - [ ] figures_index.json / figures_adjust.json (if changed)
  - [ ] page_data/*.json (if changed)
- [ ] Manual page(s) load and images render (spot check)

### Paste curl checks (example)
```bash
curl -I https://jason-vaughan.github.io/barcoach-assets/figures_index.json
curl -I https://jason-vaughan.github.io/barcoach-assets/figures_adjust.json

---

## Contributor Notes
- This repository (Gen1 / Gen2) is public for transparency and learning.  
- Internal planning docs, Cursor configs, and Gen3 (monetized) will remain private.  
- Please avoid including secrets or credentials in PRs.  
- PRs are welcome for:
  - Bug fixes
  - Loader improvements
  - Documentation clarity
  - Workflow simplification