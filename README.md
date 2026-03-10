# Quill

AI-powered book writing assistant for Claude Code and Codex. Write fiction, nonfiction, or technical books chapter by chapter with automatic context compression, non-linear revision support, and LaTeX or Markdown output.

## Install

### Claude Code

Clone or download this plugin, then point Claude Code at it:

```bash
git clone https://github.com/gc4rella/quill.git
claude --plugin-dir /path/to/quill
```

Or install directly from GitHub:

```bash
claude plugin install gc4rella/quill
```

### Codex

Install the bundled skill directory `skills/quill-context/` into `$CODEX_HOME/skills/quill-context/` (usually `~/.codex/skills/quill-context/`), or ask Codex to install the GitHub path `gc4rella/quill/skills/quill-context`.

Then use the skill explicitly with `$quill-context`, or rely on auto-activation when you are inside a Quill project with a `quill.json` file.

## Start a New Book

### Claude Code

Run the guided setup wizard:

```
/quill:init
```

The wizard walks you through 6 phases:

1. **Foundation** — title, type (fiction/nonfiction/technical), premise, audience, length
2. **Book-type questions** — genre, structure, characters (fiction) or thesis, prerequisites (technical)
3. **Output format** — LaTeX or Markdown
4. **Style fingerprint** — derives a one-line voice guide from your influences
5. **Project setup** — creates `quill.json`, directories, format files, and a reusable chapter scaffold helper
6. **Auto-generated outline** — complete chapter-by-chapter plan you can review and adjust, then materializes chapter stubs

Then start writing with `/quill:write 1`.

### Codex

Ask for the same workflow directly. Examples:

- `Use $quill-context to initialize a new fiction book in this folder.`
- `Use $quill-context to write chapter 1 from the current outline.`
- `Use $quill-context to revise chapter 3 and flag any downstream continuity impact.`
- `Use $quill-context to export this manuscript to Markdown.`

Codex uses the same Quill rules and file layout, but it does not expose `/quill:*` slash commands. The skill maps those intents onto bundled workflow references.

## Commands / Intents

In Claude Code these are slash commands. In Codex they are the corresponding requests you make to the `quill-context` skill.

| Claude command | Codex intent | Description |
|---------|-------------|-------------|
| `/quill:init` | "Initialize a new Quill project" | Guided setup wizard — run once to start a new book |
| `/quill:write N` | "Write chapter N" | Write chapter N using compressed context |
| `/quill:revise N` | "Revise chapter N" | Revise an existing chapter with continuity tracking |
| `/quill:status` | "Show Quill status" | Bird's-eye view: progress, threads, revision log |
| `/quill:outline` | "Show or edit the outline" | View or edit the chapter outline |
| `/quill:threads` | "Show or resolve open threads" | Manage open plot threads or concept questions |
| `/quill:character Name` | "Update character/concept Name" | Add or update characters (fiction) or concepts (technical) |
| `/quill:export` | "Export the manuscript" | Assemble manuscript — PDF, Markdown, DOCX, or HTML |
| `/quill:format` | "Switch format to latex/markdown" | View or switch output format (LaTeX/Markdown) |

## Output Formats

### LaTeX
- Chapters saved as `chapters/ch-NN.tex`
- Wrapper file `book.tex` with preamble and `\input{}` entries
- `scripts/quill-sync-outline.py` keeps placeholder chapter files aligned with the outline
- Switching into LaTeX uses in-repo chapter conversion
- Export can compile to PDF with `pdflatex` (requires TeX Live)

### Markdown
- Chapters saved as `chapters/ch-NN.md`
- `scripts/quill-sync-outline.py` keeps placeholder chapter files aligned with the outline
- Export assembles `export/manuscript.md`
- Optional conversion to DOCX or HTML via `pandoc`

Choose your format during project initialization. Switch later with `/quill:format` in Claude Code or by asking Codex to change the Quill format.

## Non-Linear Writing

Quill is designed for non-linear work. You can:

- **Write chapters out of order** — the briefing system handles context from summaries
- **Revise any chapter at any time** — Quill detects continuity impact and flags downstream chapters that may need updating
- **Track open threads** — plot threads and concept questions are tracked automatically, with staleness warnings for threads open 5+ chapters

After revising an earlier chapter, check Quill status to see which later chapters may need attention.

## How Context Compression Works

Writing a full book exceeds any LLM's context window. Quill solves this with a compression contract:

1. **After writing each chapter**, Quill self-summarizes: what happened, new characters/concepts, threads opened/closed, emotional beats, word count.
2. **Summaries are stored in `quill.json`**, not raw prose. Only the last ~150 words of the most recent chapter are kept verbatim (for prose continuity).
3. **When writing the next chapter**, Quill builds a briefing under 1500 tokens from summaries, style fingerprint, active characters, open threads, and the chapter's outline brief.
4. **No full chapter is ever loaded** unless you're actively revising it.

This means chapter 20 writes with the same quality of context as chapter 2 — the compression scales to any book length.

## Project Structure

```
your-book/
├── quill.json              ← single source of truth
├── book.tex                ← LaTeX wrapper (LaTeX projects only)
├── chapters/
│   ├── ch-01.tex or .md
│   ├── ch-02.tex or .md
│   └── ...
├── scripts/
│   └── quill-sync-outline.py
├── characters/             ← fiction: detailed character sheets
├── concepts/               ← technical: detailed concept sheets
└── export/
    └── manuscript.md       ← assembled output (Markdown projects)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
