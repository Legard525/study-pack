---
name: study-pack
description: Use this skill when a student wants to study from their own course files (lecture notes, slides, textbook chapters, problem sets, seminar sheets, past exams; PDF, Word, scans or photos) and needs typeset study material back as PDF. It makes step-by-step solutions to every problem, a topic walkthrough with intuition and examples, a "what follows from what" formula sheet, a dense cheat sheet, or a compact study guide built around given problems. Use it even if they never say "study pack", in any language: "solve all of these without skipping steps", "make me a cheat sheet", "collect the theory I need for these problems, exam in two weeks", "Spickzettel", "шпора", "разбери задачи". Skip it for editing the student's own thesis or essay, summarising research papers, translating documents, making slide decks, or quick conceptual questions that need no course files.
---

# study-pack

Someone has an exam coming and hands over their course files with a short, often informal request. Your job is to give back material they can actually study from: correct, complete where it needs to be, short where it can be, and nicely typeset. They are usually stressed and short on time, so every page should earn its place.

## 1. Find and read the sources

- **Where the files are:** a path the user gives. Otherwise look at the newest course-like files in the working directory and then in `~/Downloads`, and say which ones you used. If nothing plausible turns up, ask.
- **Read every file completely before planning.** Skimming misses the one problem that needs extra theory.
  - **PDF:** use `pdftotext -layout`, or `pypdf`/`pymupdf` if poppler is missing. If the text comes out empty, the file is a scan (`pdfinfo` often shows `img2pdf` or a scanner as Producer). In that case, and wherever formulas, graphs, tables or handwriting come out mangled, render the pages (`pdftoppm -r 110 -png`) and read them as images. Skip blank scratch pages.
  - **DOCX:** use `python-docx` or `textutil -convert txt` (macOS). Run `unzip -l` to find embedded images or equations, and look at those too.
  - **Photos:** read them directly.
- **Write down what you're working from:** the course, the chapter or seminar numbers, and every problem with its source number. Everything you produce cites these numbers, so the student can find their way back to the original.

## 2. Match the request to a deliverable

One request can ask for several deliverables. Build each one as its own PDF, with a number prefix in the output language: `1_Solutions_….pdf`, `2_Cheat_sheet_….pdf`.

| Request sounds like | Deliverable | What it must contain |
|---|---|---|
| "solve all of these", "don't skip steps", "as simply as possible" | **Solutions** | For multiple choice, an answer table first. Then every problem in order, with the statement restated briefly. Show every algebraic and arithmetic step and substitute the numbers explicitly. Use the simplest method that works. Put each final answer in an answer box. Computational problems get the most detail. For each "MUST be true" item, give a counterexample or a one-line proof, and name the trap option (the one you get from the typical mistake). |
| "full walkthrough of the chapter with intuition and examples" | **Walkthrough** | Go section by section through the source, with definition, intuition, example and trap boxes. Draw graphs to scale. Solve every in-text exercise. End with exam-style practice problems with answers and a True/False block. |
| "all the formulas", "what follows from what", "derivations" | **Formula sheet** | Start with a dependency diagram showing which formula leads to which. Then a numbered formula table with a column for which earlier formula each comes from and how (derivative, division, substitution). Mark one- or two-line consequences missing from the source as *bonus*. End with ready-made standard cases and a step-by-step method for typical problems. |
| "cheat sheet", "crib sheet", "one page of theory" | **Cheat sheet** | 1–2 pages, A4 landscape, three columns. Definitions, key results, traps, mini-graphs, and a glossary when the source and output languages differ. Dense but readable. |
| "study guide", "the theory I need for these problems", "no fluff" | **Study guide** | Open with a table mapping each problem to the guide sections it needs. Each topic gets only the definitions and theorems actually needed, a method box, a trap box, and a short worked example from their own sheets, cited by number. End with a checklist of exam traps. If the problems need theory the materials don't cover, add it as its own section and say so. |
| One question about one problem, often a photo | **Chat answer, no PDF** | The verdict first, in bold. Then the reasoning in short bullets, then an optional quick check. Write math in Unicode (p + s, MC = 2q + 2, n·s²/4), because raw TeX doesn't render in most chat surfaces. |

If the request fits none of these, pick the closest one and say how you read it. Ask only when the reading would change which files you produce.

## 3. Language

1. **Default:** write in the language of the course materials. That's the language of the exam and of the terms the student has to recognise.
2. **No usable materials** (a bare question or a photo of one line): write in the language of the request.
3. **Explicit request for another language:** if the user asks for, say, Russian while the notes are in English, write in that language. Keep each key source-language term in parentheses at first use (`\term{deadweight loss}` in LaTeX), and use the source-language notation inside formulas and graph labels.

Follow the output language's typographic conventions: quotation marks, the decimal separator, and non-breaking spaces where the language needs them. If a typography skill for that language is available, for example `ru-text` for Russian, apply it.

Write no filler: no paragraph on why the topic matters, no motivational closing. The student asked for material, not encouragement.

## 4. Correctness

A study pack with a wrong answer is worse than none, because the student will learn the mistake. So:

- **Solve everything yourself.** Treat answers printed in the source as claims to check.
- **Verify every numerical or symbolic result** with a short sympy script (or another CAS). Determinants, inverses, ranks and solution sets are cheap to check and easy to get wrong by hand. If the script disagrees with you, find out why before you write the answer.
- **Errors in the source:** wrong sign, max instead of min, mislabelled variables, an answer to a different question. Mark each one where it occurs (the `srcerr` box) and list them all in your reply, so the student isn't thrown by them.
- **Loose wording that still has a standard reading:** use the same box, add "imprecise wording", and state the reading you used.
- **Problems that are genuinely ambiguous:** state the interpretation and solve under it. If no reading is defensible, leave the problem out and say why. Never guess silently.

The pack is for the requester's own study. Restate problems briefly rather than reproducing whole pages of the source.

## 5. Build

**Output folder.** If the user or the project has a convention for scratch or throwaway output (check CLAUDE.md or similar), use it. Otherwise create `study-pack-<short-topic>/` next to the source files, or in the working directory. Put the PDFs at the top level and the sources in `src/`.

**Engine.** Use LaTeX if `latexmk` is available: math, tables and pgfplots graphs come out best there. Otherwise use the HTML route. If neither LaTeX nor a Chromium-family browser is available, deliver the HTML file and say that printing it to PDF is one click in any browser.

### LaTeX route

- **Start from a skeleton.** Copy `assets/preamble.tex` and the matching file from `assets/skeletons/` into `src/`. The skeletons are `solutions.tex`, `walkthrough.tex`, `formula-sheet.tex`, `cheatsheet.tex` and `study-guide.tex`. Their layout is already settled (margins, columns, box styles, graph style), so your job is content, not layout.
- **Language:** set `\def\studylang{…}` and `\def\sourcelang{…}` at the top. Box titles come built in for `english`, `russian`, `ngerman`, `french` and `spanish`. For another language, `\renewcommand` the `\ttl…` macros. pdfLaTeX covers Latin and Cyrillic; for other scripts see `references/latex-notes.md`.
- **No need to read the preamble.** Everything it offers is listed here:
  - boxes `defn`, `idea`, `trap`, `method`, `task`, `exmpl`, `keyres` and `srcerr`, written as `\begin{trap}[: title suffix]`;
  - `\sol` and `\ans{…}` for solutions;
  - `\term{…}` for a source-language term;
  - the `econ` pgfplots axis style;
  - `\studyheader{…}{…}` for the running header.
- **Defaults that prevent fix-up rounds:**
  - Boxes don't split across pages. Pass `[breakable]` as the second option (`\begin{exmpl}[: name][breakable]`) only for a box longer than about half a page.
  - Text lines can't overflow, headings never sit stranded at the bottom of a page, there are no paragraph indents, and long `align` blocks may break across pages.
  - Label graph curves at their ends, with `node[pos=1,anchor=west]`.
- **Write each document in one go.** Draft the whole `.tex` in a single write instead of growing it through many small edits. Each extra round trip costs far more time than the compile itself. Put subject macros (`\MC`, `\rk`, …) in the document.
- **Typing rules that the lint can't fix for you:**
  - With a decimal-comma language, put a space after every comma that separates items in math: `(1, 2)`, `(x, y)`, `a_{1, 4}`.
  - Break any display formula wider than the text with `\\` inside `aligned` or `multline`.
- **Compile and lint:** run `latexmk -pdf -interaction=nonstopmode -halt-on-error <file>.tex`, then `python3 scripts/lint_tex.py <file>.tex`. The lint reports errors, overfull lines, boxes too tall for a page, undefined references and glued commas, each with its `.tex` line number. Fix everything it reports before looking at any page image. Text-level fixes are cheap; rendering and inspecting pages is the expensive part.

### HTML route

- **Template:** copy `assets/template.html`. It has KaTeX math, the same box styles and an A4 print layout. Add `class="landscape cols3"` to `<body>` for a cheat sheet.
- **Graphs:** draw them as inline SVG.
- **Print:** run `bash scripts/html_to_pdf.sh <file>.html <out>.pdf`. It finds Chrome, Chromium or Edge and prints headlessly, waiting for KaTeX to finish rendering.

### Visual check: two rounds, then stop

Students print these, so the layout matters. Each look at page images is slow, though, so keep to this budget:

1. **Round 1.** Once the lint is clean, run `python3 scripts/contact_sheet.py <file>.pdf <scratch-dir>`, which tiles four pages per image, and look at every sheet.
   - Write down **every** problem you see across all pages before changing anything: clipped or overlapping graph labels, a box with a big gap before it, a lone line on the last page, unrendered math.
   - Zoom in (`pdftoppm -r 160 -f N -l N` plus a crop) only where a sheet looks wrong.
   - Then fix them all in one edit and recompile.
2. **Round 2.** Lint again, render the contact sheet again and confirm the fixes. If something small remains, fix it, recompile, lint, and stop. Don't render a third time.

With several deliverables, compile and render them together (one command, `&` and `wait`) rather than one at a time.

Finally, remove the build artefacts (`latexmk -c`) and copy the PDFs out of `src/`.

## 6. Deliver

Send or link the PDFs. Keep the reply short and cover:

- the source files used;
- what each PDF contains and its page count;
- the final answers, when the deliverable is solutions;
- the errors found in the source;
- how you verified the content (CAS, visual check);
- anything you left out, and why.

Offer at most one natural extra, for example an answer key to the remaining problems or the next chapter in the same style.

When feedback comes back, edit the sources in `src/` and rebuild. Don't start over.
