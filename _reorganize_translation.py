# -*- coding: utf-8 -*-
"""Reorganize 翻訳/: only N-M.pdf + section dirs N-M/ at top level."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
    "ch01-dgm",
    "ch02-vae-ddpm",
    "ch03-score-ncsn",
    "ch04-score-sde",
    "ch05-flow-matching",
    "ch06-unified",
    "ch07-ot",
    "ch08-guidance",
]


def section_image_names(md_text: str) -> set[str]:
    names = set()
    for m in re.finditer(r"!\[[^\]]*\]\((?:images/)?([^)]+)\)", md_text):
        names.add(Path(m.group(1)).name)
    return names


def guess_section_for_image(name: str, section_stems: list[str]) -> str | None:
    # fig-3-4.jpg / table-5-1.jpg -> prefer section 3-4 / 5-1 if exists, else chapter-first
    m = re.match(r"(?:fig|table)-(\d+)-(\d+)", name, re.I)
    if not m:
        return section_stems[0] if section_stems else None
    cand = f"{m.group(1)}-{m.group(2)}"
    if cand in section_stems:
        return cand
    # same chapter prefix
    pref = f"{m.group(1)}-"
    same = [s for s in section_stems if s.startswith(pref)]
    return same[0] if same else (section_stems[0] if section_stems else None)


def reorganize_chapter(folder: str) -> None:
    tdir = ROOT / folder / "翻訳"
    if not tdir.exists():
        return

    old_images = tdir / "images"
    old_tex = tdir / "tex"
    old_src = tdir / "_src"
    old_pdf = tdir / "pdf"
    old_build = tdir / "build"

    mds = sorted(
        p for p in tdir.glob("*.md") if p.name.lower() != "readme.md"
    )
    stems = [md.stem for md in mds]

    # Move README out of 翻訳/ into chapter root if present
    readme = tdir / "README.md"
    if readme.exists():
        chapter_readme = ROOT / folder / "README_翻訳.md"
        shutil.move(str(readme), str(chapter_readme))

    for md in mds:
        stem = md.stem
        sec = tdir / stem
        sec.mkdir(parents=True, exist_ok=True)
        (sec / "images").mkdir(exist_ok=True)
        (sec / "build").mkdir(exist_ok=True)

        dest_md = sec / f"{stem}.md"
        if md.resolve() != dest_md.resolve():
            shutil.move(str(md), str(dest_md))

        src_tex = old_tex / f"{stem}.tex"
        if src_tex.exists():
            shutil.move(str(src_tex), str(sec / f"{stem}.tex"))

        src_en = old_src / f"{stem}.en.txt"
        if src_en.exists():
            shutil.move(str(src_en), str(sec / f"{stem}.en.txt"))

        text = dest_md.read_text(encoding="utf-8", errors="replace")
        for name in section_image_names(text):
            src_img = old_images / name
            if src_img.exists():
                dest_img = sec / "images" / name
                if not dest_img.exists():
                    shutil.copy2(src_img, dest_img)

        for cand in (old_pdf / f"{stem}.pdf", tdir / f"{stem}.pdf"):
            if cand.exists():
                dest_pdf = tdir / f"{stem}.pdf"
                if cand.resolve() != dest_pdf.resolve():
                    if dest_pdf.exists():
                        dest_pdf.unlink()
                    shutil.move(str(cand), str(dest_pdf))
                break

        print(f"  {folder}/翻訳/{stem}/ + {stem}.pdf")

    # Place leftover images into guessed section folders
    if old_images.exists():
        for p in list(old_images.iterdir()):
            if not p.is_file():
                continue
            stem = guess_section_for_image(p.name, stems)
            if stem is None:
                continue
            dest = tdir / stem / "images" / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.move(str(p), str(dest))
            else:
                p.unlink()

    for d in (old_tex, old_src, old_pdf, old_build, old_images):
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)

    for preview in (tdir / "_preview",):
        if preview.exists():
            shutil.rmtree(preview, ignore_errors=True)

    # Fix preamble path in moved tex if needed (same depth as before)
    for stem in stems:
        tex = tdir / stem / f"{stem}.tex"
        if tex.exists():
            t = tex.read_text(encoding="utf-8")
            t2 = t.replace(
                r"\input{../../../common/translation-preamble}",
                r"\input{../../../common/translation-preamble}",
            )
            # ensure graphicspath works via preamble images/
            if t2 != t:
                tex.write_text(t2, encoding="utf-8")

    print(f"done {folder}")


def main():
    for folder in CHAPTERS:
        print("==", folder)
        reorganize_chapter(folder)


if __name__ == "__main__":
    main()
