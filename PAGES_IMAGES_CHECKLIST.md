# GitHub Pages Images Checklist

This checklist helps ensure images resolve correctly on GitHub Pages.

---

## 1. Ignore macOS junk
```bash
echo ".DS_Store" >> .gitignore
git rm --cached .DS_Store || true
git add .gitignore
git commit -m "chore: ignore .DS_Store"
git push
```

---

## 2. Verify `<base>` tag
All `.htm/.html` files should point to the absolute GitHub Pages URL:

```html
<base href="https://YOUR-USERNAME.github.io/REPO-NAME/images/">
```

Search for bad relative bases:

```bash
grep -RIn '<base href="../images/">' docs || echo "No bad base tags ✅"
```

---

## 3. Double-check image paths
Extract some image references:

```bash
grep -oE '<img[^>]*src="([^"]+)"' docs/content-fixed.htm | head -3
```

Test URLs with curl:

```bash
curl -I https://YOUR-USERNAME.github.io/REPO-NAME/images/Image_1006.jpg
```

(Replace `Image_1006.jpg` with actual file names.)

---

## 4. Commit & push all changes
```bash
git add -A
git commit -m "fix: update base href / images"
git push
```

---

## 5. Confirm GitHub sync
```bash
git log -1 --oneline
git ls-remote origin HEAD
```

Short hash (local) must match the long hash (remote).

---

## 6. Global base-href fix (when adding new HTML/HTM files)

If new `.htm/.html` files are added and images don’t load, run this once to insert/replace `<base>` everywhere:

```bash
bash -c '
find docs -type f $begin:math:text$ -name "*.htm" -o -name "*.html" $end:math:text$ -print0 |
while IFS= read -r -d "" f; do
  if grep -q "<base href=" "$f"; then
    sed -i "" "s#<base href=\"[^\"]*\"#<base href=\"https://jason-vaughan.github.io/barcoach-assets/images/\"#g" "$f"
  else
    sed -i "" "s#<head>#<head>\
  <base href=\"https://jason-vaughan.github.io/barcoach-assets/images/\">#" "$f"
  fi
done
'

---

✅ Done — GitHub Pages should now serve all images correctly.
