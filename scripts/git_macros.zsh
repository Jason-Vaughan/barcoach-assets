# ----- Git helper macros (paste-safe; comments allowed) -----

# Show changes + run pre-commit across repo
gwhat() {
  echo "🔧 Changed files:"
  git status -s
  echo
  echo "🧪 Pre-commit (all files)…"
  pre-commit run --all-files || true
}

# Run pre-commit and re-stage any fixes
gfix() {
  echo "🧹 Running pre-commit on all files…"
  pre-commit run --all-files || true
  echo "➕ Re-staging any fixes…"
  git add -A
  echo "✅ Done."
}

# Stage → pre-commit → re-stage → commit → push
# Usage: gpush "your commit message"
gpush() {
  local msg="$*"
  if [ -z "$msg" ]; then
    msg="chore: quick sync $(date -u '+%Y-%m-%d %H:%MZ')"
  fi
  echo "➕ Staging…"
  git add -A
  echo "🧪 Pre-commit (all files)…"
  pre-commit run --all-files || true
  echo "➕ Re-staging any pre-commit fixes…"
  git add -A
  echo "📝 Commit: $msg"
  git commit -m "$msg" || { echo "ℹ️ Nothing to commit."; return 0; }
  echo "🚀 Pushing…"
  git push
}

# Quick HTTP sanity check of key endpoints
gcheck() {
  local urls=(
    "https://jason-vaughan.github.io/barcoach-assets/data-index.html"
    "https://jason-vaughan.github.io/barcoach-assets/manifest.html"
    "https://jason-vaughan.github.io/barcoach-assets/manual_manifest.json"
    "https://jason-vaughan.github.io/barcoach-assets/figures.html"
    "https://jason-vaughan.github.io/barcoach-assets/figures_index.json"
    "https://jason-vaughan.github.io/barcoach-assets/figures_adjust.json"
    "https://jason-vaughan.github.io/barcoach-assets/page_data/content-fixed.json"
  )
  echo "🌐 Endpoint checks:"
  for u in "${urls[@]}"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" -I "$u")
    printf "%-85s %s\n" "$u" "$code"
  done
}
# ----- end -----
