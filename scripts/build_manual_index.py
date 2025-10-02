#!/usr/bin/env python3
import os, re, json, glob
from html.parser import HTMLParser

DOCS_DIR = "docs"
PAGE_DATA_DIR = os.path.join(DOCS_DIR, "page_data")
MANIFEST = os.path.join(DOCS_DIR, "manual_manifest.json")
IMAGE_INDEX = os.path.join(DOCS_DIR, "image_index.json")

CAPTION_HINT = re.compile(r'\b(Image\s*\d+[-–]\d+|Figure|Fig\.)\b', re.I)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.images = []          # [{src, alt, caption}]
        self._textbuf = []
        self._last_img = None

    def handle_starttag(self, tag, attrs):
        d = {k:v for k,v in attrs}
        if tag == "title":
            self.in_title = True
        if tag in ("p","div","li","td","th","section","article","figcaption"):
            self._textbuf = []
        if tag == "img":
            src = (d.get("src") or "").strip()
            alt = (d.get("alt") or "").strip()
            self._last_img = {"src": src, "alt": alt, "caption": ""}
            self.images.append(self._last_img)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in ("p","div","li","td","th","section","article","figcaption"):
            txt = " ".join(t.strip() for t in self._textbuf if t.strip())
            if txt and self._last_img and not self._last_img.get("caption"):
                if tag in ("figcaption","li") or CAPTION_HINT.search(txt):
                    self._last_img["caption"] = txt
            self._textbuf = []

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        self._textbuf.append(data)

def norm_src(src: str) -> str:
    if not src: return ""
    if src.startswith(("http://","https://","data:")): return src
    s = re.sub(r'^(?:\./|\.\./|/)+', '', src)
    if not s.lower().startswith("images/"):
        s = "images/" + s
    return s

def parse_page(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    p = Parser()
    p.feed(html)
    title = (p.title or os.path.basename(path)).strip()
    imgs = []
    for im in p.images:
        src = norm_src(im.get("src",""))
        if src:
            imgs.append({
                "src": src,
                "alt": (im.get("alt") or "").strip(),
                "caption": (im.get("caption") or "").strip()
            })
    return title, imgs

def main():
    os.makedirs(PAGE_DATA_DIR, exist_ok=True)
    pages = []
    image_index = {}

    html_files = sorted(glob.glob(os.path.join(DOCS_DIR, "*.htm")) +
                        sorted(glob.glob(os.path.join(DOCS_DIR, "*.html"))))

    # Build per-page data and compact image index
    for file in html_files:
        rel = os.path.relpath(file, DOCS_DIR)
        base = os.path.splitext(os.path.basename(file))[0]
        title, imgs = parse_page(file)

        # write per-page json
        out_page_json = os.path.join(PAGE_DATA_DIR, f"{base}.json")
        with open(out_page_json, "w", encoding="utf-8") as f:
            json.dump({"file": rel, "title": title, "images": imgs}, f, indent=2, ensure_ascii=False)

        pages.append({"file": rel, "title": title, "data_json": f"page_data/{base}.json"})

        for im in imgs:
            key = im["src"].split("/")[-1].lower()
            image_index.setdefault(key, []).append({
                "page": rel,
                "title": title,
                "src": im["src"],
                "caption": im["caption"]
            })

    # Write manifest (tiny)
    site_root = "https://jason-vaughan.github.io/barcoach-assets/"
    manifest = {
        "site_root": site_root,
        "pages": pages,
        "assets": {
            "image_index": "image_index.json"
        },
        "version": {"generated": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z"}
    }
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Write compact image index
    with open(IMAGE_INDEX, "w", encoding="utf-8") as f:
        json.dump(image_index, f, indent=2, ensure_ascii=False)

    print(f"Manifest: {MANIFEST}")
    print(f"Pages: {len(pages)}  Image files indexed: {len(image_index)}")
    print(f"Per-page JSONs in: {PAGE_DATA_DIR}")

if __name__ == "__main__":
    main()
