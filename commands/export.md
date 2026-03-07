---
description: Assemble all written chapters into a final manuscript. Produces PDF (LaTeX) or a single document (Markdown).
argument-hint: (optional) "pdf" to compile LaTeX to PDF, "docx" or "html" for markdown
allowed-tools: Read, Write, Bash
---

# Quill Export

You are assembling the final manuscript for a Quill book project.

Read `quill.json` first. If it doesn't exist, tell the user to run `/quill:init` first and stop.

Check the `format` field to determine which export path to follow.

---

## LaTeX Export Path (format = "latex")

### Step 1: Verify chapter files

Scan the `outline` array. For each chapter with `status` of `"written"` or `"revised"`, verify the file exists at `chapters/ch-{NN}.tex`.

Report any missing files:
> "Warning: Chapter N is marked as written but `chapters/ch-03.tex` is missing."

### Step 2: Update book.tex

Read `book.tex`. Update the `\input{}` lines to include all written chapters in order:

```latex
\input{chapters/ch-01.tex}
\input{chapters/ch-02.tex}
\input{chapters/ch-03.tex}
% ... etc
```

Only include chapters that exist as files. Preserve the existing preamble, title page, and table of contents. Save `book.tex`.

### Step 3: Compile (if "pdf" argument)

If the user passed "pdf" as argument:

1. Check if `pdflatex` is available:
   ```bash
   which pdflatex
   ```
2. If available, compile:
   ```bash
   cd <project root> && pdflatex -interaction=nonstopmode book.tex && pdflatex -interaction=nonstopmode book.tex
   ```
   (Run twice for table of contents and references.)
3. If successful, report: "PDF generated at `book.pdf`."
4. If `pdflatex` not found, tell the user:
   > "pdflatex is not installed. Install TeX Live (`brew install --cask mactex` on macOS) or compile manually with `pdflatex book.tex`."

If no "pdf" argument, just update `book.tex` and report:
> "book.tex updated with all chapter inputs. Run `pdflatex book.tex` to compile, or `/quill:export pdf` to compile now."

### Step 4: Report

- Number of chapters included
- Any chapters skipped (not yet written)
- Total word count across all chapters
- Output file location

---

## Markdown Export Path (format = "markdown")

### Step 1: Verify chapter files

Same as LaTeX path — check all written chapters exist at `chapters/ch-{NN}.md`.

### Step 2: Assemble manuscript

Concatenate all written chapters into a single file at `export/manuscript.md`:

```markdown
# Book Title

## Chapter 1: Chapter Title

[contents of ch-01.md]

## Chapter 2: Chapter Title

[contents of ch-02.md]

...
```

Use chapter titles from the `outline` array. Add a blank line between the heading and the chapter text, and two blank lines between chapters.

If the book has parts (`structure.has_parts`), add part headings:

```markdown
# Part 1: Part Title

## Chapter 1: Chapter Title
...
```

Save to `export/manuscript.md`.

### Step 3: Convert (if "docx" or "html" argument)

If the user passed "docx" or "html":

1. Check if `pandoc` is available:
   ```bash
   which pandoc
   ```
2. If available, convert:
   ```bash
   pandoc export/manuscript.md -o export/manuscript.docx
   ```
   or
   ```bash
   pandoc export/manuscript.md -o export/manuscript.html --standalone
   ```
3. If successful, report the output location.
4. If `pandoc` not found, tell the user:
   > "pandoc is not installed. Install it (`brew install pandoc` on macOS) or convert manually. The assembled Markdown is at `export/manuscript.md`."

If no conversion argument, just assemble and report:
> "Manuscript assembled at `export/manuscript.md`. Run `/quill:export docx` or `/quill:export html` to convert."

### Step 4: Report

- Number of chapters included
- Any chapters skipped (not yet written)
- Total word count
- Output file location(s)
- If chapters are marked `needs-revision`, warn:
  > "Note: Chapters N, M are flagged as needing revision. The export includes their current versions."
