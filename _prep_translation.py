# -*- coding: utf-8 -*-
from pathlib import Path
import re, shutil, json

root = Path(".")
txt = (root / "ゼミ資料" / "ゼミ資料.txt").read_text(encoding="utf-8", errors="replace")
lines = txt.splitlines()

starts = []
for i, line in enumerate(lines):
    m = re.match(r"^([1-8])\.([0-9]+)\s{2,}(\S.*)$", line)
    if m and i > 800 and "...." not in m.group(3):
        starts.append((i, int(m.group(1)), int(m.group(2)), m.group(3).strip()))

end = 12852
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

ch_intro = {}
for c in range(1, 9):
    first = next(s for s in starts if s[1] == c)
    for j in range(first[0] - 1, max(800, first[0] - 150), -1):
        s = lines[j].strip()
        if re.match(rf"^{c}\s+\S", s) and len(s) < 110 and not s.startswith(f"{c}."):
            ch_intro[c] = j
            break
    if c not in ch_intro:
        ch_intro[c] = first[0]

meta = {}
for idx, (i, c, s, title) in enumerate(starts):
    nxt = starts[idx + 1][0] if idx + 1 < len(starts) else end
    body = "\n".join(lines[i:nxt]).rstrip() + "\n"
    outdir = root / chapters[c] / "翻訳" / "_src"
    outdir.mkdir(parents=True, exist_ok=True)
    name = f"{c}-{s}.en.txt"
    (outdir / name).write_text(body, encoding="utf-8")
    meta.setdefault(c, []).append(
        {
            "file": name,
            "section": f"{c}.{s}",
            "title": title,
            "lines": f"{i}-{nxt - 1}",
            "chars": len(body),
        }
    )

for c, start in ch_intro.items():
    first = next(s for s in starts if s[1] == c)[0]
    if start < first:
        body = "\n".join(lines[start:first]).rstrip() + "\n"
        outdir = root / chapters[c] / "翻訳" / "_src"
        (outdir / f"{c}-0.en.txt").write_text(body, encoding="utf-8")
        meta[c].insert(
            0,
            {
                "file": f"{c}-0.en.txt",
                "section": f"{c}.0",
                "title": "Chapter intro",
                "lines": f"{start}-{first - 1}",
                "chars": len(body),
            },
        )

copied = []
for fig in root.rglob("fig-*.jpg"):
    if "翻訳" in fig.parts:
        continue
    m = re.search(r"fig-([1-8])-(\d+)", fig.name)
    if not m:
        continue
    c = int(m.group(1))
    dest_name = fig.name.replace("-nocaption", "")
    dest = root / chapters[c] / "翻訳" / "images" / dest_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if (not dest.exists()) or dest.stat().st_size < fig.stat().st_size:
        shutil.copy2(fig, dest)
        copied.append(str(dest.relative_to(root)))

(root / "翻訳_meta.json").write_text(
    json.dumps(
        {"sections": meta, "copied_figs": copied, "ch_intro": ch_intro},
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
print("sections", sum(len(v) for v in meta.values()))
print("copied", len(copied))
for c, items in meta.items():
    print(c, [x["file"] for x in items])
