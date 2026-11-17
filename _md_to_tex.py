# -*- coding: utf-8 -*-
"""Convert 翻訳/N-M/N-M.md Japanese translations to N-M.tex in the same section folder."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS = {
    1: "ch01-dgm",
    2: "ch02-vae-ddpm",
    3: "ch03-score-ncsn",
    4: "ch04-score-sde",
    5: "ch05-flow-matching",
    6: "ch06-unified",
    7: "ch07-ot",
    8: "ch08-guidance",
}


def escape_text(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in s)


def convert_inline(s: str) -> str:
    parts: list[str] = []
    pattern = re.compile(r"(\$\$.*?\$\$|\$[^$]+\$)")
    idx = 0
    for m in pattern.finditer(s):
        if m.start() > idx:
            parts.append(_inline_text(s[idx : m.start()]))
        math = m.group(1)
        if math.startswith("$$"):
            inner = math[2:-2].strip()
            tag_m = re.search(r"\\(?:quad|qquad)\s*\(([0-9.]+)\)\s*$", inner)
            if tag_m:
                num = tag_m.group(1)
                inner = inner[: tag_m.start()].rstrip()
                parts.append(f"\\[\n{inner}\\quad ({num})\n\\]")
            else:
                tag_m2 = re.search(r"\(([0-9]+\.[0-9]+(?:\.[0-9]+)?)\)\s*$", inner)
                if tag_m2:
                    num = tag_m2.group(1)
                    inner2 = inner[: tag_m2.start()].rstrip()
                    parts.append(f"\\[\n{inner2}\\quad ({num})\n\\]")
                else:
                    parts.append(f"\\[\n{inner}\n\\]")
        else:
            parts.append(math)
        idx = m.end()
    if idx < len(s):
        parts.append(_inline_text(s[idx:]))
    return "".join(parts)


def _inline_text(s: str) -> str:
    s = re.sub(r"\[\^([^\]]+)\]", r"\\footnote{REF:\1}", s)
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: "\\textbf{" + escape_text(m.group(1)) + "}", s)
    s = re.sub(
        r"(?<!\*)\*([^*]+?)\*(?!\*)",
        lambda m: "\\emph{" + escape_text(m.group(1)) + "}",
        s,
    )
    s = re.sub(r"`([^`]+)`", lambda m: "\\texttt{" + escape_text(m.group(1)) + "}", s)
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append(s[i])
            i += 1
            while i < len(s) and s[i].isalpha():
                out.append(s[i])
                i += 1
            if i < len(s) and s[i] == "{":
                depth = 0
                while i < len(s):
                    if s[i] == "{":
                        depth += 1
                    elif s[i] == "}":
                        depth -= 1
                    out.append(s[i])
                    i += 1
                    if depth == 0:
                        break
            continue
        ch = s[i]
        if ch in "&%#_~^":
            out.append(
                {
                    "&": r"\&",
                    "%": r"\%",
                    "#": r"\#",
                    "_": r"\_",
                    "~": r"\textasciitilde{}",
                    "^": r"\textasciicircum{}",
                }[ch]
            )
        elif ch == "{":
            out.append(r"\{")
        elif ch == "}":
            out.append(r"\}")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def parse_meta(lines: list[str]) -> tuple[dict, list[str]]:
    meta = {}
    body = lines
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            if ":" in lines[i]:
                k, v = lines[i].split(":", 1)
                meta[k.strip()] = v.strip()
            i += 1
        body = lines[i + 1 :] if i < len(lines) else []
    cleaned = []
    for ln in body:
        m = re.match(
            r"^-\s*\*\*(原題|日本語タイトル|出典[^:]*)\*\*\s*[:：]\s*(.+)$",
            ln.strip(),
        )
        if m:
            key = "出典" if "出典" in m.group(1) else m.group(1)
            meta[key] = m.group(2).strip()
            continue
        cleaned.append(ln)
    return meta, cleaned


def md_to_body(md: str) -> tuple[dict, str]:
    lines = md.splitlines()
    meta, lines = parse_meta(lines)
    footnotes = {}
    body_lines = []
    for ln in lines:
        fm = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", ln.strip())
        if fm:
            footnotes[fm.group(1)] = fm.group(2)
            continue
        body_lines.append(ln)

    out: list[str] = []
    i = 0
    in_quote = False
    quote_buf: list[str] = []
    in_list = False
    list_type = None

    def flush_quote():
        nonlocal in_quote, quote_buf
        if not quote_buf:
            in_quote = False
            return
        text = "\n".join(quote_buf)
        title_m = re.search(r"\*\*(.+?)\*\*", text)
        title = title_m.group(1).strip() if title_m else "注意"
        content = re.sub(r"^\s*>\s?", "", text, flags=re.M)
        cleaned_lines = []
        skipped_title = False
        for qln in content.split("\n"):
            plain = re.sub(r"\*\*(.+?)\*\*", r"\1", qln).strip()
            if (not skipped_title) and plain and plain == title:
                skipped_title = True
                continue
            cleaned_lines.append(qln)
        content = "\n".join(cleaned_lines).strip()
        content = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", content)
        content = convert_block_math(content)
        out.append(
            f"\\begin{{propositionbox}}[{_inline_text(title)}]\n{content}\n\\end{{propositionbox}}\n"
        )
        quote_buf = []
        in_quote = False

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            out.append(f"\\end{{{list_type}}}\n")
            in_list = False
            list_type = None

    while i < len(body_lines):
        ln = body_lines[i]
        raw = ln.rstrip()

        if not raw.strip():
            if in_quote:
                flush_quote()
            flush_list()
            out.append("")
            i += 1
            continue

        im = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", raw.strip())
        if im:
            flush_list()
            if in_quote:
                flush_quote()
            alt, path = im.group(1), im.group(2)
            path = path.replace("\\", "/").replace("images/", "").lstrip("/")
            cap = convert_inline(alt)
            out.append(f"\\translationfigure{{{path}}}{{{cap}}}\n")
            i += 1
            continue

        if raw.strip().startswith("$$"):
            flush_list()
            if in_quote:
                flush_quote()
            block = [raw.strip()]
            if not raw.strip().endswith("$$") or raw.strip() == "$$":
                i += 1
                while i < len(body_lines):
                    block.append(body_lines[i].rstrip())
                    if body_lines[i].strip().endswith("$$"):
                        break
                    i += 1
            math = "\n".join(block).strip()
            if math.startswith("$$"):
                math = math[2:]
            if math.endswith("$$"):
                math = math[:-2]
            math = math.strip()
            tag_m = re.search(r"\\(?:quad|qquad)\s*\(([0-9.]+)\)\s*$", math)
            if not tag_m:
                tag_m = re.search(r"\(([0-9]+\.[0-9]+(?:\.[0-9]+)?)\)\s*$", math)
            if tag_m:
                num = re.search(r"([0-9]+\.[0-9]+(?:\.[0-9]+)?)", tag_m.group(0)).group(1)
                inner = math[: tag_m.start()].rstrip()
                if "&=" in inner or "\\\\" in inner:
                    out.append(f"\\begin{{align*}}\n{inner}\\quad ({num})\n\\end{{align*}}\n")
                else:
                    out.append(f"\\[\n{inner}\\quad ({num})\n\\]\n")
            else:
                if "&=" in math or (r"\\" in math and "\n" in math):
                    out.append(f"\\begin{{align*}}\n{math}\n\\end{{align*}}\n")
                else:
                    out.append(f"\\[\n{math}\n\\]\n")
            i += 1
            continue

        hm = re.match(r"^(#{1,3})\s+(.*)$", raw)
        if hm:
            flush_list()
            if in_quote:
                flush_quote()
            level = len(hm.group(1))
            title = convert_inline(hm.group(2).strip())
            cmd = {1: "section*", 2: "subsection*", 3: "subsubsection*"}[level]
            out.append(f"\\{cmd}{{{title}}}\n")
            i += 1
            continue

        if raw.lstrip().startswith(">"):
            flush_list()
            in_quote = True
            quote_buf.append(re.sub(r"^\s*>\s?", "", raw))
            i += 1
            continue
        elif in_quote:
            flush_quote()

        um = re.match(r"^(\s*)[-*]\s+(.*)$", raw)
        om = re.match(r"^(\s*)\d+\.\s+(.*)$", raw)
        if um or om:
            kind = "itemize" if um else "enumerate"
            content = um.group(2) if um else om.group(2)
            if not in_list or list_type != kind:
                flush_list()
                out.append(f"\\begin{{{kind}}}")
                in_list = True
                list_type = kind
            out.append(f"\\item {convert_inline(content)}")
            i += 1
            continue
        else:
            flush_list()

        out.append(convert_inline(raw))
        i += 1

    flush_list()
    if in_quote:
        flush_quote()

    body = "\n".join(out)
    for fid, ftext in footnotes.items():
        body = body.replace(
            f"\\footnote{{REF:{fid}}}",
            f"\\footnote{{{convert_inline(ftext)}}}",
        )
    body = re.sub(r"\\footnote\{REF:([^}]+)\}", r"\\footnote{\1}", body)
    return meta, body


def convert_block_math(text: str) -> str:
    def repl(m):
        inner = m.group(1).strip()
        return f"\\[\n{inner}\n\\]"

    return re.sub(r"\$\$(.+?)\$\$", repl, text, flags=re.S)


def wrap_tex(meta: dict, body: str, section_id: str) -> str:
    source = meta.get("出典") or meta.get("出典§") or f"§{section_id.replace('-', '.')}"
    # 翻訳/N-M/N-M.tex → ../../../common
    preamble = r"\input{../../../common/translation-preamble}"
    parts = [
        preamble,
        "\\begin{document}",
        f"{{\\color{{gray}}\\footnotesize 出典: {convert_inline(source)}\\par}}",
        "\\vspace{0.2em}",
        body,
        "\\end{document}\n",
    ]
    return "\n".join(parts)


def convert_file(md_path: Path, tex_path: Path) -> None:
    md = md_path.read_text(encoding="utf-8")
    section_id = md_path.stem
    meta, body = md_to_body(md)
    tex = wrap_tex(meta, body, section_id)
    tex = re.sub(r"\\tag\{([^}]+)\}", r"\\quad (\1)", tex).replace("\u2003", " ")
    tex_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path.write_text(tex, encoding="utf-8")


def main():
    converted = []
    for _, folder in CHAPTERS.items():
        tdir = ROOT / folder / "翻訳"
        if not tdir.exists():
            continue
        # new layout: 翻訳/N-M/N-M.md
        for sec in sorted(tdir.iterdir()):
            if not sec.is_dir() or not re.match(r"^\d+-\d+$", sec.name):
                continue
            md = sec / f"{sec.name}.md"
            if not md.exists():
                continue
            tex = sec / f"{sec.name}.tex"
            convert_file(md, tex)
            converted.append(str(tex.relative_to(ROOT)))
    print(f"converted {len(converted)}")
    for p in converted:
        print(p)


if __name__ == "__main__":
    main()
