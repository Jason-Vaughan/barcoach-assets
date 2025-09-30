#!/usr/bin/env python3
import os, re, json, glob
from html.parser import HTMLParser

DOCS_DIR = "docs"
OUT_FILE = os.path.join(DOCS_DIR, "manual_index.json")

# Heuristics for captions:
# - <img alt="..."> wins if present
# - text immediately following the image within the same block element
# - text containing "Image", e.g., "Image 7-4: Adjust menu"
CAPTION_PATTERN = re.compile(r'\bImage\s*\d+[-–]\d+\b|\bFigure\b|\bFig\.\b', re.I)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.images = []          # list of dicts: {src, alt, caption, context}
        self._current_text = []   # collect text nodes per block
        self._blocks = []         # list of (tag, text)
        self._last_img = None     # remember last seen image to bind nearby text

    def handle_starttag(self, tag, attrs):
        if tag == "title": self.in_title = True
        if tag in ("p","div","li","td","th","section","article","figcaption"): 
            self._current_text = []
        if tag == "img":
            d = {k:v for k,v in attrs}
            src = d.get("src","").strip()
            alt = d.get("alt","") or ""
            self._last_img = {"src": src, "alt": alt, "caption": "", "context": ""}
            self.images.append(self._last_img)

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag in ("p","div","li","td","th","section","article","figcaption"):
            txt = " ".join(t.strip() for t in self._current_text if t.strip())
            if txt:
                self._blocks.append((tag, txt))
                # Bind to most recent image if no caption yet and text is likely a caption
                if self._last_img and not self._last_img.get("caption"):
                    if CAPTION_PATTERN.search(txt) or tag in ("figcaption","li"):
                        self._last_img["caption"] = txt
                # Give some surrounding context too
                if self._last_img and not self._last_img.get("context"):
                    self._last_img["context"] = txt[:280]
            self._current_text = []

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        self._current_text.append(data)

def normalize_src(src: str) -> str:
    # We publish at site root; HTML uses images/… relative to root (thanks to <base>).
    # Ensure we only emit paths the site actually serves.
    if src.startswith(("http://","https://","data:")):
        return src
    # Strip any leading ./ or ../ and normalize to images/… when it looks like an image
    if re.search(r'\.(png|jpe?g|gif|svg|webp)$', src, re.I):
        # collapse any leading slashes or dots
        s = re.sub(r'^(?:\./|\.\./|/)+', '', src)
        if not s.lower().startswith("images/"):
            s = "images/" + s
        return s
    return src

def parse_page(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    p = PageParser()
    p.feed(html)
    # Clean + normalize images
    imgs = []
    for im in p.images:
        src = normalize_src(im.get("src",""))
        if not src: 
            continue
        obj = {
            "src": src,
            "alt": (im.get("alt") or "").strip(),
            "caption": (im.get("caption") or "").strip(),
            "context": (im.get("context") or "").strip()
        }
        imgs.append(obj)
    title = p.title.strip() or os.path.basename(path)
    return title, imgs

def main():
    pages = []
    image_map = {}   # key: filename (lower), value: list of occurrences

    for file in sorted(glob.glob(os.path.join(DOCS_DIR, "*.htm")) + 
                       glob.glob(os.path.join(DOCS_DIR, "*.html"))):
        rel = os.path.relpath(file, DOCS_DIR)
        title, imgs = parse_page(file)
        page_entry = {
            "file": rel,
            "title": title,
            "images": imgs
        }
        pages.append(page_entry)
        for im in imgs:
            # reduce key to the filename for easy lookup
            fname = im["src"].split("/")[-1].lower()
            entry = {
                "page": rel,
                "title": title,
                "src": im["src"],
                "alt": im["alt"],
                "caption": im["caption"]
            }
            image_map.setdefault(fname, []).append(entry)

    out = {
        "site_root": "https://jason-vaughan.github.io/barcoach-assets/",
        "generated_from": "docs/*.htm(l)",
        "pages": pages,
        "image_index": image_map
    }

    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_FILE} with {len(pages)} pages and {sum(len(p['images']) for p in pages)} images.")

if __name__ == "__main__":
    main()