# BarCoach – Gen2 TODO (Internal Only)

⚠️ This file is **local only** and should remain ignored by git.
It’s a mutable working checklist for development and testing.

---

## ✅ Status Markers Legend
- ✅ = Done / verified
- 🚧 = In progress
- ⏭ = Next action
- ❓ = Open question / needs decision
- 💤 = Deferred / maybe later

---

## Tasks

### Answer Format & Visuals
- 🚧 Auto-suggest training videos (integrate into answers by default)
- ⏭ Refine captions + links for readability
- ⏭ Add dimmed/italicized note under visuals:
  *“⚠️ Inline images not supported yet — click links to view (future-proofed).”*
- ❓ Confirm whether GPT can display *web-fetched inline images* (vs hosted assets)

### Loader & Diagnostics
- ⏭ Streamline diagnostics (short, user-friendly)
- ✅ Figures subset (`figures_adjust.json`) in place
- 🚧 Test fallback reliability across wrappers + raw JSON

### Repo Hygiene
- ⏭ Audit repo for dead files / confirm archive folder contents
- ✅ PR template added
- ⏭ Double-check `.gitignore` for local-only files (e.g. `TODO_GEN2.md`)

### Cross-Version Flow
- ⏭ Add Gen1 → Gen2 link/upgrade hint
- ❓ Plan Gen2 → Gen3 teaser copy
- 💤 Keep Gen1 around for “manual upload” users


---

## ✅ Completed
- Figures index (`figures_index.json`) + filtered subset (`figures_adjust.json`)
- Loader: wrappers first, raw fallback, caching
- PR template + repo hygiene
- Public roadmap + builder guide committed

---

## 🚧 In Progress
- [ ] Verify filtered figures (`figures_adjust.json`) used correctly by GPT
- [ ] Streamline loader diagnostics (short, clear, only helpful info)
- [ ] Repo hygiene check (dead files, dupes, naming consistency)

---

## ⏭ Next Actions
- [ ] Update **Answer Format**:
  - Caption + link readability
  - Add dimmed italic note: *“Inline images not supported yet; click to view image”*
- [ ] Auto-suggest training videos when relevant
- [ ] Enable web search for related images/videos (use inline previews if platform allows)
- [ ] Add Gen1 → Gen2 cross-link (for users upgrading)
- [ ] Add Gen1/Gen2 → Gen3 teaser message (future-ready)

---

## ❓ Open Questions
- Should we keep Gen1 live permanently, or redirect later?
- Do we eventually merge TODOs into roadmap, or keep split?

---
