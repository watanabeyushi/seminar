# -*- coding: utf-8 -*-
"""Compile 翻訳/N-M/N-M.tex → 翻訳/N-M.pdf (PDF only at 翻訳 top level)."""
from __future__ import annotations

import re
import subprocess
import sys
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


def compile_one(tex: Path) -> tuple[bool, str]:
    sec_dir = tex.parent  # .../翻訳/N-M
    pdf_dir = sec_dir.parent  # .../翻訳
    build_dir = sec_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "latexmk",
        "-lualatex",
        "-interaction=nonstopmode",
        "-f",
        f"-outdir={pdf_dir}",
        f"-auxdir={build_dir}",
        tex.name,
    ]
    try:
        r = subprocess.run(
            cmd,
            cwd=str(sec_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT {tex}"
    pdf = pdf_dir / f"{tex.stem}.pdf"
    ok = pdf.exists() and pdf.stat().st_size > 1000
    tail = (r.stdout or "")[-1200:] + "\n" + (r.stderr or "")[-600:]
    return ok, (f"OK {tex.stem}.pdf" if ok else tail)


def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    results = []
    for folder in CHAPTERS:
        tdir = ROOT / folder / "翻訳"
        if not tdir.exists():
            continue
        for sec in sorted(tdir.iterdir()):
            if not sec.is_dir() or not re.match(r"^\d+-\d+$", sec.name):
                continue
            if only and sec.name not in only:
                continue
            tex = sec / f"{sec.name}.tex"
            if not tex.exists():
                print(f"MISSING tex {tex}")
                results.append((str(tex), False))
                continue
            print(f"== compiling {folder}/翻訳/{sec.name}/{tex.name}")
            ok, msg = compile_one(tex)
            print(msg if ok else msg[-2000:])
            results.append((str(tex.relative_to(ROOT)), ok))
    failed = [p for p, ok in results if not ok]
    print("---")
    print(f"total={len(results)} ok={sum(1 for _, o in results if o)} fail={len(failed)}")
    for p in failed:
        print("FAIL", p)


if __name__ == "__main__":
    main()
