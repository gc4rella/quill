# Quill Init Templates

Templates and layout specifications used by the Init Workflow. Load this file only when initializing a new project.

---

## Directory Layout

Create these directories at init:

```
project-root/
├── .quill/
│   └── summaries/          ← per-chapter summary files (commit this)
├── chapters/               ← chapter source files
├── export/                 ← assembled output and conversion intermediates
├── scripts/                ← helper utilities
├── characters/             ← fiction projects only
└── concepts/               ← nonfiction / technical projects only
```

`.quill/` must be **committed** with the book project. Note this in the project README.

---

## Helper Scripts

Copy all three scripts from `../templates/` into `scripts/` at init:

- `quill-sync-outline.py` — reads `quill.json` and creates or refreshes chapter stub files without overwriting drafted chapters.
- `quill-validate.py` — validates the project and migrates v1 → v2. Run after any structural change or to check integrity.
- `quill-stats.py` — computes accurate word counts from chapter files (strips markup). Used by Write/Revise/Status workflows.

If the templates directory is not accessible, create stubs that print a "not available" message rather than leaving the scripts directory empty.

---

## book.tex Preamble (LaTeX projects only)

```latex
\documentclass[{font_size},{paper_size}]{book}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[{paper_size}]{geometry}
\usepackage{hyperref}

\title{{Title}}
\author{{Author}}
\date{}

\begin{document}

\maketitle
\tableofcontents

% Chapter \input{} lines will be added by /quill:export

\end{document}
```

Defaults: document class `book`, font size `11pt`, paper size `letterpaper`. Substitute values from Phase 3 of the interview. Add any additional packages the author requested.

---

## README Template — LaTeX Projects

```markdown
# {Title}

A book project powered by [Quill](https://github.com/gc4rella/quill).

## Building the PDF

This project uses LaTeX. To compile the manuscript to PDF:

```bash
pdflatex book.tex
pdflatex book.tex   # run twice for table of contents
```

### Requirements

- A LaTeX distribution (e.g., [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), or [MiKTeX](https://miktex.org/))
- Packages used: `hyperref`, `geometry`, `fontenc`, `inputenc` (included in most distributions)

### Project Structure

- `quill.json` — project metadata and outline (single source of truth)
- `.quill/summaries/` — per-chapter summary files; commit this directory
- `book.tex` — LaTeX wrapper with preamble and chapter includes
- `chapters/` — individual chapter files (`.tex`)
- `scripts/quill-sync-outline.py` — refreshes placeholder chapter files from the outline
- `scripts/quill-validate.py` — validates the project; run with `--migrate` to upgrade schema
- `scripts/quill-stats.py` — accurate word counts and progress stats
- `export/` — compiled output

## Create or Refresh Chapter Stubs

When you add or change planned chapters in `quill.json`, regenerate placeholder chapter files with:

```bash
python3 scripts/quill-sync-outline.py
```

This only updates Quill stub files. Drafted chapters are left untouched.

## Validate the Project

```bash
python3 scripts/quill-validate.py
```

## Quill Commands

| Command | Description |
|---------|-------------|
| `/quill:write N` | Write chapter N |
| `/quill:revise N` | Revise chapter N |
| `/quill:status` | Progress overview |
| `/quill:outline` | View or edit the outline |
| `/quill:export` | Assemble and compile the manuscript |
| `/quill:format` | Switch between LaTeX and Markdown |
```

---

## README Template — Markdown Projects

```markdown
# {Title}

A book project powered by [Quill](https://github.com/gc4rella/quill).

## Assembling the Manuscript

Use the Quill export command to assemble all chapters into a single file:

```
/quill:export
```

This creates `export/manuscript.md`.

### Converting to Other Formats

With [pandoc](https://pandoc.org/) installed, you can convert the assembled manuscript:

```bash
# To DOCX
pandoc export/manuscript.md -o export/manuscript.docx

# To HTML
pandoc export/manuscript.md -o export/manuscript.html --standalone

# To PDF (requires LaTeX)
pandoc export/manuscript.md -o export/manuscript.pdf
```

### Project Structure

- `quill.json` — project metadata and outline (single source of truth)
- `.quill/summaries/` — per-chapter summary files; commit this directory
- `chapters/` — individual chapter files (`.md`)
- `scripts/quill-sync-outline.py` — refreshes placeholder chapter files from the outline
- `scripts/quill-validate.py` — validates the project; run with `--migrate` to upgrade schema
- `scripts/quill-stats.py` — accurate word counts and progress stats
- `export/` — assembled manuscript output

## Create or Refresh Chapter Stubs

When you add or change planned chapters in `quill.json`, regenerate placeholder chapter files with:

```bash
python3 scripts/quill-sync-outline.py
```

This only updates Quill stub files. Drafted chapters are left untouched.

## Validate the Project

```bash
python3 scripts/quill-validate.py
```

## Quill Commands

| Command | Description |
|---------|-------------|
| `/quill:write N` | Write chapter N |
| `/quill:revise N` | Revise chapter N |
| `/quill:status` | Progress overview |
| `/quill:outline` | View or edit the outline |
| `/quill:export` | Assemble the manuscript |
| `/quill:format` | Switch between LaTeX and Markdown |
```

Replace `{Title}` with the actual book title from Phase 1.
