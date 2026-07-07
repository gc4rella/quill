# Format Conversion Reference

Detailed Markdown ↔ LaTeX conversion rules for the Format Workflow. Load this file only when switching a project between formats.

Format switching is a **deterministic in-repo source conversion**. It never requires `pandoc`, `pdflatex`, or any external converter — those matter only for export targets (PDF/DOCX/HTML).

---

## Markdown → LaTeX (`.md` → `.tex`)

For each chapter file:

1. Add `\chapter{Title}` as the first line, using the chapter title from `outline` in `quill.json`. If no outline entry matches, derive a placeholder title from the filename.
2. Convert markup:

| Markdown | LaTeX |
|---|---|
| `**bold**` | `\textbf{bold}` |
| `*italic*` | `\textit{italic}` |
| `` `code` `` | `\texttt{code}` |
| ` ``` ` code fence | `\begin{verbatim}...\end{verbatim}` |
| `# H1` / `## H2` / `### H3` | `\section{}` / `\subsection{}` / `\subsubsection{}` |
| `---` horizontal rule | `\bigskip` |
| Ordered / unordered lists | `enumerate` / `itemize` |
| Blockquote | `quote` environment |
| `[text](url)` | `\href{url}{text}` |
| Footnotes | `\footnote{...}` when straightforward |
| Pipe tables | Convert only when the structure is unambiguous; otherwise preserve the content and flag manual review |

3. Escape LaTeX special characters in prose: `&`, `%`, `$`, `#`, `_`, `{`, `}` — but **not** inside already-converted commands or verbatim blocks.
4. Preserve meaning for unsupported Markdown features (HTML blocks, complex tables) instead of dropping content; flag them for manual review.

## LaTeX → Markdown (`.tex` → `.md`)

For each chapter file:

1. Remove the `\chapter{...}` line — chapter headings are added during export in Markdown mode.
2. Convert markup:

| LaTeX | Markdown |
|---|---|
| `\textbf{text}` | `**text**` |
| `\textit{text}` / `\emph{text}` | `*text*` |
| `\texttt{code}` | `` `code` `` |
| `\begin{verbatim}...\end{verbatim}` | Triple-backtick code block |
| `\section{}` / `\subsection{}` / `\subsubsection{}` | `#` / `##` / `###` |
| `\bigskip` | `---` |
| `itemize` / `enumerate` | Markdown lists |
| `quote` environment | Blockquote |
| `\href{url}{text}` | `[text](url)` |
| `\footnote{...}` | Markdown footnote when straightforward |

3. Flatten custom macros and unsupported environments conservatively, then flag them for manual review.
4. Unescape LaTeX special characters: `\&` → `&`, `\%` → `%`, `\$` → `$`, `\#` → `#`, `\_` → `_`.

---

## File-handling rules

- **Write all new target-format files first.** Remove old source-format files only after the complete new set exists. Never leave both `.md` and `.tex` versions of the same chapter after a successful switch.
- Any assembled snapshot or conversion scratch file belongs under `export/`, never in `chapters/`.

## Edge cases

- **No chapter files yet** — skip conversion; just update `quill.json.format` and handle `book.tex`. Report "No chapters to convert."
- **Mixed extensions** — if both `.md` and `.tex` exist for the same chapter *before* switching, warn and stop; ask the user to resolve manually.
- **Best-effort caveat** — automated conversion handles the constructs above; complex LaTeX (custom macros, math environments, intricate tables) or complex Markdown (HTML blocks) may need manual review. Always list flagged constructs in the report.
