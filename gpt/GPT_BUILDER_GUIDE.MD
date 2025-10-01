# BarCoach – GPT Builder Guide (Teaser)

This guide explains how to update the **Custom GPT** safely without breaking the data loader or visuals behavior.

---

## 1) What this GPT is
- **Scope:** Barco Event Master (E2/E3/S3/EX) + EC-50/200/210.
- **Canon:** Documentation-first. If not in docs → say “Not in documentation.”
- **Visuals:** Provide **clickable links** to images + manual pages (inline previews are not supported in GPT chat).

---

## 2) Where the data lives
- GitHub Pages root: `https://jason-vaughan.github.io/barcoach-assets/`
- Index page (entry): `…/data-index.html`
- Manifest: `…/manual_manifest.json`
- Figures:
  - Full: `…/figures_index.json`
  - Filtered (rotate/adjust): `…/figures_adjust.json`
- Per-page data: `…/page_data/*.json`

> These URLs are exposed on `data-index.html` with **clickable IDs** the GPT can follow.

---

## 3) Loader routine (do not change order)
**Entry / click path (robust):**
1. SEARCH for either query and OPEN the first result:
   - `data-index.html site:jason-vaughan.github.io`
   - `site:jason-vaughan.github.io/barcoach-assets data-index.html`
2. If SEARCH yields nothing usable, directly OPEN  
   `https://jason-vaughan.github.io/barcoach-assets/data-index.html`

**Manifest (wrapper first, JSON fallback):**
- Click `id="manifest-html"` → parse `<script id="manifest-json" type="application/json">…`
- If that fails: click `id="manifest-primary"`; if that fails: `id="manifest-raw"`
- Set:
  - `MANUAL.manifest = parsed`
  - `MANUAL.site_root = MANUAL.manifest.site_root`

**On-demand datasets (lazy):**
- **Figures (fast search):**
  - Try `id="figures-html"` → parse `<script id="figures-json">`
  - Else `id="figures-index"` → else `id="figures-index-raw"`
  - Cache as `MANUAL.figures`
- **Filtered figures (rotate/adjust fast-path):**
  - `id="figures-adjust"` → else `id="figures-adjust-raw"`
- **Per-page data (when needed):**
  - Primary ids: `pd-bookmarks`, `pd-content-fixed`, `pd-content`, `pd-headings`, `pd-index`
  - Raw fallbacks: corresponding `*-raw`
  - Cache to `MANUAL.pages_cache[file]`

**Retries & diagnostics:**
- Retry each fetch up to 3×, then move to the next mirror (wrapper → primary → raw).
- If **manifest** fails after all:  
  `⚠️ Manual manifest fetch failed after retries. I will answer from memory only.`
- When a fetch fails, briefly report: URL/mirror/step/error.

---

## 4) Lookup logic & visuals (teaser-safe)
**Filename lookup (e.g., `Image_1006.jpg`):**
- Lowercase key → `image_1006.jpg`
- Ensure `MANUAL.image_index` is loaded (via data-index links)
- Return:
  - **Direct image link**: `MANUAL.site_root + src`
  - **Manual page link**: `MANUAL.site_root + file`
  - Caption/alt if present

**Caption/feature search:**
- Search `images[]` fields in order: **caption → alt → context**
- Rank: caption > alt > context
- Return top 1–3

**Answer format (no inline previews in GPT):**
- Steps (bullets).
- **Visuals** block (for each match):
  - Caption (or alt)
  - Plain clickable **image URL**
  - Plain clickable **manual page URL**
  - (Optionally include a `![alt](url)` line for future compatibility—won’t render today)
- If >3 matches: “More visuals on the page.”
- End with single source line:
  `(Source: https://jason-vaughan.github.io/barcoach-assets/manual_manifest.json)`

---

## 5) Known platform limits (don’t fight these)
- GPT chat **does not render inline images**; links only.
- Large JSON may be truncated in the viewer; prefer wrappers or filtered subsets.

---

## 6) Sanity test prompts (run after any edit)
1. **Manifest parse:**  
   “Report site_root and pages count from the manifest.”
2. **Figures quick search:**  
   “Show 2 visuals that mention adjust or rotate.”
3. **How-to with visuals:**  
   “How do I rotate an input on E2? Include 1–3 relevant visuals.”

---

## 7) Where to edit instructions
- Primary file in repo: `gpt/BarCoach-Gen2-Instructions.md`
- Paste the final version into the GPT Builder **Instructions** field.
- Keep section numbering (##1…##7) to make diffing easy.