# study-pack

An agent skill that turns course materials into exam-ready study PDFs. It reads lecture notes, slides, problem sets, past papers, scans and phone photos, in PDF, DOCX or image form, and produces one of:

- **Solutions:** every problem worked step by step, with an answer table first and the trap options named.
- **Walkthrough:** the chapter section by section, with intuition, examples and graphs drawn to scale.
- **Formula sheet:** a dependency diagram plus numbered formulas, each saying where it comes from and how.
- **Cheat sheet:** 1–2 pages, A4 landscape, three columns.
- **Study guide:** only the theory a given problem set needs, mapped problem by problem.

Every answer is checked with a computer algebra system, and errors in the source are flagged where they occur. Each page is checked visually before delivery. The output is written in the language of the materials by default, with box titles built in for English, Russian, German, French and Spanish.

## Install

```bash
npx skills add Legard525/study-pack
```

Or copy `skills/study-pack/` into your agent's skills folder, e.g. `~/.claude/skills/`. If you'd rather call it only explicitly (`/study-pack`), add `disable-model-invocation: true` to the frontmatter of your copy.

## Requirements

- **LaTeX (best output):** `latexmk` with pdfLaTeX, plus the packages `paratype`, `tcolorbox` and `pgfplots`.
- **No LaTeX:** the skill falls back to HTML with KaTeX, printed to PDF by headless Chrome, Chromium or Edge.
- **Reading and checking:** poppler (`pdftotext`, `pdftoppm`), Python 3 with Pillow, and sympy.

## Repository layout

- `skills/study-pack/`: the skill.
  - `SKILL.md`: the workflow.
  - `assets/`: the LaTeX preamble, one skeleton per deliverable, and the HTML template.
  - `scripts/`: the lint, page-preview and HTML-to-PDF helpers.
  - `references/`: notes on LaTeX edge cases.
- `evals/`: test prompts with synthetic inputs, each containing planted errors. `evals.json` holds the tuning set and `heldout.json` the held-out set; `evals/README.md` describes how to run them.

## How it was tested

Development used [skill-creator](https://github.com/anthropics/skills): every test ran with the skill and without it. On the 3 tuning evals, iteration 2 passed 20/20 checks, against 17/20 without the skill. It was also 13–58% faster than iteration 1.

On 4 held-out evals the skill was never tuned on, all versions passed every check. Iteration 2 was 21% faster than iteration 1 on average.

## Licence

MIT, see `LICENSE`.
