# BarCoach Roadmap – Gen1 & Gen2

## 🎬 Gen1 (MVP GPT)
- ✅ Manual scraping proof-of-concept
- ✅ JSON wrappers for `page_data/`
- ✅ GPT answers with text only (no visuals)
- ✅ Published free GPT in Library as a teaser

### Gen1 Notes
- Scope: Barco Event Master (E2/E3/S3/EX) + EC-50/200/210
- Behavior: Documentation-first; if not in docs → “Not in documentation.”
- Output: Steps-only answers, links optional

---

## 🎬 Gen2 (Enhanced GPT – Public Teaser)
- ✅ Figures index (≈2,632 entries)
- ✅ Filtered subset for rotation/adjust (`figures_adjust.json`)
- ✅ Robust loader routine
  - Entry: open `https://jason-vaughan.github.io/barcoach-assets/data-index.html`
  - Wrappers first (e.g., `manifest.html`, `content-fixed.html`)
  - JSON fallbacks (GitHub Pages → Raw GitHub)
  - Caching + brief diagnostics on failure
- ✅ Visuals block (caption + **clickable links** to image & manual page)
- ✅ Builder docs (`gpt/GPT_BUILDER_GUIDE.md`), PR template, repo hygiene
- ⚠️ Limitation: **No inline image rendering in GPT UI** (links only)
- 🎯 Status: **Stable & useful**, intended as the public teaser

### Gen2 Assets (public)
- Site root: `https://jason-vaughan.github.io/barcoach-assets/`
- Index: `…/data-index.html`
- Manifest: `…/manual_manifest.json` (via wrapper `manifest.html`)
- Figures: `…/figures_index.json` (full), `…/figures_adjust.json` (subset)
- Page data: `…/page_data/*.json`
- Images: `…/images/*`

### Gen2 Answer Format
1. Concise steps
2. **Visuals** (when helpful)
   - Caption (or alt)
   - Direct image **link** (clickable)
   - Manual page **link** (clickable)
3. If >3 matches: return top 3 and note “More visuals on the page.”
4. Source line: `https://jason-vaughan.github.io/barcoach-assets/manual_manifest.json`

### Gen2 Test Matrix (last run)
- Manifest load: **PASS**
- Figures wrapper → raw fallback: **PASS**
- Filename lookup via image index: **PASS**
- Caption search on large page data: **PARTIAL** (falls back to subset/wrapper)
- Inline images in chat: **BLOCKED by platform** (links used instead)

---

## 📦 What Gen2 Deliberately Defers
- Inline image rendering inside GPT chat
- Training video auto-suggestions (optional only)
- App features (accounts, history, faster caching, quotas)
