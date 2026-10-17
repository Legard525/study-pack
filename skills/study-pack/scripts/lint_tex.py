#!/usr/bin/env python3
"""Lint a compiled study-pack .tex: LaTeX errors, layout warnings, decimal-comma trap.

Usage: lint_tex.py <file.tex> [<file2.tex> ...]
Run after compiling. Prints one line per problem with the .tex line number; exits 1 if any
problem needs fixing. Catching these in text is much cheaper than finding them in page renders.
"""
import re
import sys
from pathlib import Path

MATH = re.compile(r"\$\$.+?\$\$|\$.+?\$|\\\[.+?\\\]|\\\(.+?\\\)|"
                  r"\\begin\{(equation|align|gather|multline|pmatrix|bmatrix|vmatrix|array|cases)\*?\}.+?\\end\{\1\*?\}",
                  re.S)
GLUED = re.compile(r"(?<=[0-9A-Za-z}]),(?=-?[0-9A-Za-z\\])")


def lang_of(src: str) -> str:
    m = re.search(r"\\def\\studylang\{([a-z]+)\}", src)
    return m.group(1) if m else "english"


def line_of(src: str, pos: int) -> int:
    return src.count("\n", 0, pos) + 1


def lint(tex: Path) -> int:
    problems = 0
    src = tex.read_text(encoding="utf-8")
    code = re.sub(r"(?<!\\)%.*", lambda m: " " * len(m.group(0)), src)  # blank out comments, keep offsets
    log = tex.with_suffix(".log")

    if not log.exists():
        print(f"{tex.name}: no .log, compile first"); return 1
    lg = log.read_text(encoding="latin-1")
    for m in re.finditer(r"^! (.+)$(?:.|\n)*?^l\.(\d+)", lg, re.M):
        print(f"{tex.name}:{m.group(2)}: ERROR {m.group(1)}"); problems += 1
    for m in re.finditer(r"Overfull \\hbox \((\d+\.?\d*)pt too wide\)[^\n]*lines? (\d+)", lg):
        if float(m.group(1)) > 3:
            print(f"{tex.name}:{m.group(2)}: overfull line by {m.group(1)}pt (break the formula or reword)"); problems += 1
    for m in re.finditer(r"Overfull \\vbox \((\d+\.?\d*)pt too high\)", lg):
        if float(m.group(1)) > 3:
            print(f"{tex.name}: a box is {m.group(1)}pt taller than the page: give it [breakable] or split it"); problems += 1
    if re.search(r"There were undefined references|Reference `[^']+' on page", lg):
        print(f"{tex.name}: undefined references (rerun latexmk, or fix the \\label)"); problems += 1

    if lang_of(src) != "english":
        for mm in MATH.finditer(code):
            seg = mm.group(0)
            for g in GLUED.finditer(seg):
                a, b = seg[g.start() - 1], seg[g.end()]
                pos = mm.start() + g.start()
                ctx = seg[max(0, g.start() - 12):g.end() + 12].replace("\n", " ")
                left = re.search(r"[(\[{]\s*-?\d*$", seg[:g.start()])
                right = re.match(r"-?\d*\s*[,)\]]", seg[g.end():])
                if a.isdigit() and b.isdigit() and not (left and right):
                    # a bare n,m outside brackets may be an intended decimal like 1,5
                    print(f"{tex.name}:{line_of(src, pos)}: check '{ctx}': decimal is fine; a tuple needs ', '")
                else:
                    print(f"{tex.name}:{line_of(src, pos)}: glued comma in '{ctx}': write ', ' or it renders as a decimal")
                    problems += 1
    if problems == 0:
        print(f"{tex.name}: clean")
    return problems


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(1 if sum(lint(Path(p)) for p in sys.argv[1:]) else 0)
