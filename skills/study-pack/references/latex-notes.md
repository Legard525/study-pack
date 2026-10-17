# LaTeX notes for study-pack

Read this when a compile fails, when the output language isn't Latin or Cyrillic, or before the final check of a document that uses a decimal comma.

## The decimal-comma trap

In languages that write decimals with a comma (Russian, German, French and many others), the preamble loads `icomma`. Then `1,5` prints as one decimal number. The side effect is that `(1,2)` also prints as the decimal 1,2, so tuples, matrix positions and vectors silently turn into decimals.

**Rule:** in math, type a space after any comma that separates numbers: `(1, 2)`, `(0, -14, 28)`, `a_{1, 4}`.

`scripts/lint_tex.py` checks only inside math. A glued comma next to a letter, or inside brackets like `(1,2)`, counts as a problem. A bare `1,5` is reported as "check", because it may be an intended decimal.

## Other scripts (Greek, CJK, Arabic, Hebrew, …)

pdfLaTeX with `paratype` covers Latin and Cyrillic only. For other scripts:

1. Compile with `latexmk -xelatex` (or `-lualatex`).
2. In the preamble, replace the `fontenc`, `inputenc` and `paratype` lines with `\usepackage{fontspec}` and a font that has the script, e.g. `\setmainfont{Noto Serif}` plus `\newfontfamily\cjkfont{Noto Serif CJK SC}`. For CJK, use the `xeCJK` package.
3. For right-to-left scripts, `polyglossia` handles direction better than `babel`.

If the needed fonts aren't installed, switch to the HTML route: browsers have system fallbacks for every script.

## Common compile errors

| Log line | Cause | Fix |
|---|---|---|
| `! Package babel Error: Unknown option 'xyz'` | Misspelled `\studylang`. | Use babel's language names: `english`, `russian`, `german`, `french`, `spanish`, `italian`, `portuguese`, `polish`, `ukrainian`, … |
| `! LaTeX Error: File 'paratype.sty' not found` | A minimal TeX install. | Run `tlmgr install paratype`, or remove the line (Latin-only text will still work). |
| `! Dimension too large` in pgfplots | A function blows up inside the domain. | Narrow `domain=`, or add `restrict y to domain=…`. |
| `Overfull \hbox` | A long formula. | Fix it only if the PDF visibly overflows. Use `multline`, or break the formula by hand. |
