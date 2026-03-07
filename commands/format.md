---
description: View or switch the output format (LaTeX or Markdown) for the current book project.
argument-hint: (optional) "latex" or "markdown"
allowed-tools: Read, Write, Bash
---

# Quill Format

You are managing the output format for a Quill book project.

---

## Step 1 — Load Project State

Read `quill.json` from the current directory. If it doesn't exist, tell the user to run `/quill:init` first and stop.

Note the current `format` field (`latex` or `markdown`).

---

## Step 2 — No Argument: Show Current Format

If no argument was provided, report the current format and exit:

- **LaTeX**: "This project uses **LaTeX** format. Chapters are `.tex` files in `chapters/`. Use `/quill:format markdown` to switch."
- **Markdown**: "This project uses **Markdown** format. Chapters are `.md` files in `chapters/`. Use `/quill:format latex` to switch."

Stop here if no argument was given.

---

## Step 3 — Validate Argument

The argument must be `latex` or `markdown` (case-insensitive). If it's anything else, show usage and stop.

If the requested format is already the current format, say so and stop.

---

## Step 4 — Confirm with User

Warn the user about what will change:

> Switching from **{current}** to **{target}** will:
> - Rename all chapter files in `chapters/` (`.md` to `.tex` or vice versa)
> - Convert chapter content to the new format
> - {If switching to LaTeX: "Create `book.tex` wrapper file"}
> - {If switching to Markdown: "Remove `book.tex` if it exists"}
> - Update `quill.json`
>
> Proceed?

Wait for explicit confirmation before continuing.

---

## Step 5 — Convert Chapter Files

List all chapter files in `chapters/`. For each file:

### Markdown to LaTeX (`.md` -> `.tex`)

1. Read the file content.
2. Convert markup:
   - Add `\chapter{Title}` as the first line, using the chapter title from the `outline` in `quill.json`. If no outline entry matches, use the filename to derive a placeholder title.
   - Convert `**bold**` to `\textbf{bold}`
   - Convert `*italic*` to `\textit{italic}`
   - Convert `# Heading` to `\section{Heading}`, `## Heading` to `\subsection{Heading}`, etc.
   - Convert `` `code` `` to `\texttt{code}`
   - Convert code blocks (triple backtick) to `\begin{verbatim}...\end{verbatim}`
   - Convert `---` horizontal rules to `\bigskip`
   - Escape special LaTeX characters in prose: `&`, `%`, `$`, `#`, `_`, `{`, `}` (but not inside already-converted commands)
3. Write the converted content to the new `.tex` filename.
4. Delete the old `.md` file.

### LaTeX to Markdown (`.tex` -> `.md`)

1. Read the file content.
2. Convert markup:
   - Remove the `\chapter{...}` line (chapter headings are added during export in Markdown mode)
   - Convert `\textbf{text}` to `**text**`
   - Convert `\textit{text}` to `*text*`
   - Convert `\emph{text}` to `*text*`
   - Convert `\section{Heading}` to `# Heading`, `\subsection{Heading}` to `## Heading`, etc.
   - Convert `\texttt{code}` to `` `code` ``
   - Convert `\begin{verbatim}...\end{verbatim}` to triple-backtick code blocks
   - Convert `\bigskip` to `---`
   - Unescape LaTeX special characters: `\&` to `&`, `\%` to `%`, `\$` to `$`, `\#` to `#`, `\_` to `_`
3. Write the converted content to the new `.md` filename.
4. Delete the old `.tex` file.

---

## Step 6 — Handle Wrapper File

### Switching to LaTeX

Create `book.tex` with:
- Document class from `quill.json` (default to `book` with `11pt,letterpaper`)
- Standard preamble packages (`hyperref`, `geometry`, `fontenc`, `inputenc`)
- `\title{}`, `\author{}`, `\date{}`
- `\begin{document}`, `\maketitle`, `\tableofcontents`
- `\input{}` lines for each chapter file that exists
- `\end{document}`

### Switching to Markdown

If `book.tex` exists, delete it.

---

## Step 7 — Update quill.json

Update the `format` field to the new value. Write the updated `quill.json`.

---

## Step 8 — Report

Summarize what was done:

- Number of chapter files converted
- Format switched from X to Y
- Any files created or removed (`book.tex`)
- Remind the user: "Use `/quill:export` to assemble the manuscript in the new format."

---

## Edge Cases

- **No chapter files yet**: Skip file conversion, just update `quill.json` and handle `book.tex`. Report "No chapters to convert."
- **Mixed file extensions**: If both `.md` and `.tex` files exist for the same chapter, warn the user and stop without converting. Ask them to resolve manually.
- **Conversion imperfections**: After converting, note that automated format conversion is best-effort. Complex LaTeX (custom macros, math environments, tables) or complex Markdown (HTML blocks, footnotes) may need manual review.
