# -*- coding: utf-8 -*-
"""Extract figures/tables from seminar PDF into chapter 翻訳/images/."""
from pathlib import Path
import re
import fitz  # pymupdf

root = Path(".")
pdf_path = root / "ゼミ資料" / "ゼミ資料.pdf"
doc = fitz.open(pdf_path)

chapters = {
    1: "ch01-dgm",
    2: "ch02-vae-ddpm",
    3: "ch03-score-ncsn",
    4: "ch04-score-sde",
    5: "ch05-flow-matching",
    6: "ch06-unified",
    7: "ch07-ot",
    8: "ch08-guidance",
}

# Paper page numbers from TOC (printed) -> need PDF page index.
# Heuristic: find "Figure X.Y" / "Table X.Y" text and clip nearby drawings/images.
pat_fig = re.compile(r"Figure\s+([1-8])\.(\d+)")
pat_tab = re.compile(r"Table\s+([1-8])\.(\d+)")

found = {}
for page_index in range(len(doc)):
    page = doc[page_index]
    text = page.get_text("text")
    for kind, pat in (("fig", pat_fig), ("table", pat_tab)):
        for m in pat.finditer(text):
            c, n = int(m.group(1)), int(m.group(2))
            key = (kind, c, n)
            # keep first occurrence (caption page)
            if key not in found:
                found[key] = page_index

print("found captions", len(found))
for key in sorted(found):
    print(key, "pdf_page", found[key] + 1)


def save_page_region(page, out_path, clip=None, zoom=2.0):
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))


saved = []
for (kind, c, n), page_index in sorted(found.items()):
    dest_dir = root / chapters[c] / "翻訳" / "images"
    dest = dest_dir / f"{kind}-{c}-{n}.jpg"
    # Prefer existing slide-extracted fig if present and larger
    alt = dest_dir / f"fig-{c}-{n}.jpg"
    if kind == "fig" and alt.exists() and alt.stat().st_size > 20_000:
        print("skip existing", alt.name)
        continue
    if dest.exists() and dest.stat().st_size > 20_000:
        print("skip existing", dest.name)
        continue

    page = doc[page_index]
    # Try to capture upper/middle figure: from top to caption y
    blocks = page.get_text("dict")["blocks"]
    caption_y = None
    for b in blocks:
        if b.get("type") != 0:
            continue
        for line in b.get("lines", []):
            s = "".join(span.get("text", "") for span in line.get("spans", []))
            if kind == "fig" and re.search(rf"Figure\s+{c}\.{n}\b", s):
                caption_y = line["bbox"][1]
            if kind == "table" and re.search(rf"Table\s+{c}\.{n}\b", s):
                caption_y = line["bbox"][1]
    rect = page.rect
    if caption_y is None:
        clip = fitz.Rect(rect.x0 + 36, rect.y0 + 60, rect.x1 - 36, rect.y1 - 60)
    else:
        # figure usually above caption; take a band above caption
        top = max(rect.y0 + 40, caption_y - 320)
        bottom = min(rect.y1 - 40, caption_y + 40)
        clip = fitz.Rect(rect.x0 + 36, top, rect.x1 - 36, bottom)
        if clip.height < 80:
            clip = fitz.Rect(rect.x0 + 36, max(rect.y0 + 40, caption_y - 200), rect.x1 - 36, min(rect.y1 - 40, caption_y + 60))

    out = dest if kind == "table" else (alt if True else dest)
    # standardize: figures -> fig-c-n.jpg, tables -> table-c-n.jpg
    if kind == "fig":
        out = dest_dir / f"fig-{c}-{n}.jpg"
    else:
        out = dest_dir / f"table-{c}-{n}.jpg"
    save_page_region(page, out, clip=clip, zoom=2.0)
    saved.append(str(out.relative_to(root)))
    print("saved", out, "clip_h", round(clip.height, 1))

print("saved_count", len(saved))
doc.close()
