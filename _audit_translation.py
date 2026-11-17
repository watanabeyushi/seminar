# -*- coding: utf-8 -*-
"""Audit Japanese translation completeness for ch01-ch08."""
from pathlib import Path
import re

root = Path(".")
chapters = {
    1: ("ch01-dgm", list(range(1, 5))),
    2: ("ch02-vae-ddpm", list(range(1, 4))),
    3: ("ch03-score-ncsn", list(range(1, 7))),
    4: ("ch04-score-sde", list(range(1, 8))),
    5: ("ch05-flow-matching", list(range(1, 6))),
    6: ("ch06-unified", list(range(1, 6))),
    7: ("ch07-ot", list(range(1, 7))),
    8: ("ch08-guidance", list(range(1, 7))),
}
expected_figs = {
    1: [1, 2, 3, 4],
    2: [1, 2, 3, 4, 5, 6, 7],
    3: [1, 2, 3, 4, 5, 6, 7],
    4: [1, 2, 3, 4, 5, 6, 7, 8],
    5: list(range(1, 12)),
    6: [1, 2],
    7: [1, 2, 3, 4, 5, 6],
    8: [1, 2],
}
expected_tabs = {1: [1], 3: [1], 4: [1], 5: [1, 2, 3], 6: [1]}

issues = []
ok_files = []
for c, (folder, secs) in chapters.items():
    tdir = root / folder / "翻訳"
    for s in secs:
        md = tdir / f"{c}-{s}.md"
        en = tdir / "_src" / f"{c}-{s}.en.txt"
        if not md.exists():
            issues.append(f"MISSING_MD {md}")
            continue
        jp = md.read_text(encoding="utf-8", errors="replace")
        en_text = en.read_text(encoding="utf-8", errors="replace") if en.exists() else ""
        if len(jp) < max(800, int(0.35 * len(en_text))):
            issues.append(f"SHORT {md} jp={len(jp)} en={len(en_text)}")
        # figure refs in english
        for n in expected_figs.get(c, []):
            if re.search(rf"Figure\s+{c}\.{n}\b", en_text) and not re.search(
                rf"images/fig-{c}-{n}\.", jp
            ):
                issues.append(f"NO_FIG_EMBED {md} fig-{c}-{n}")
        for n in expected_tabs.get(c, []):
            if en.exists() and re.search(rf"Table\s+{c}\.{n}\b", en_text) and not re.search(
                rf"images/table-{c}-{n}\.", jp
            ):
                issues.append(f"NO_TAB_EMBED {md} table-{c}-{n}")
        ok_files.append((str(md.relative_to(root)), len(jp)))

print("OK_FILES", len(ok_files))
for p, n in ok_files:
    print(f"  {p}\t{n}")
print("ISSUES", len(issues))
for i in issues:
    print(i)
