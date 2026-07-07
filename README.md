# Quill

AI-powered book writing assistant for Claude Code and Codex. Write fiction, nonfiction, or technical books chapter by chapter with automatic context compression, non-linear revision support, and LaTeX or Markdown output.

Quill is distributed as:

- a Claude Code plugin with `/quill:*` slash commands
- a Codex skill named `quill`

## Install

### Requirements

- Git, if installing from a checkout
- Node.js/npm, if installing the Codex skill with `npx skills`
- Claude Code or Codex, depending on the assistant you use

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

Install the `quill` skill globally with `npx skills`:

```bash
npx skills add gc4rella/quill --skill quill -g -a codex -y
```

To install from a local checkout instead:

```bash
git clone https://github.com/gc4rella/quill.git
cd quill
npx skills add . --skill quill -g -a codex -y
```

Restart Codex after installation so it discovers the new skill.

Manual install is also supported: copy `skills/quill/` into `$CODEX_HOME/skills/quill/` (usually `~/.codex/skills/quill/`).

Then use the skill explicitly with `$quill`, or rely on auto-activation when you are inside a Quill project with a `quill.json` file.

## Quick Start

### Claude Code

Create a project directory and run:

```bash
/quill:init
```

After the wizard creates the outline and chapter stubs, write the first chapter:

```bash
/quill:write 1
```

### Codex

Create a project directory, open it in Codex, and ask:

```text
Use $quill to initialize a new fiction book in this folder.
```

Then continue with chapter work:

```text
Use $quill to write chapter 1 from the current outline.
```

Codex uses the same Quill rules and file layout, but it does not expose `/quill:*` slash commands. The skill maps those intents onto bundled workflow references.

## Guided Setup

### Claude Code

The initialization wizard walks you through 6 phases:

1. **Foundation** - title, type (fiction/nonfiction/technical), premise, audience, length
2. **Book-type questions** - genre, structure, characters (fiction) or thesis, prerequisites (technical)
3. **Output format** - LaTeX or Markdown
4. **Style fingerprint** - derives a one-line voice guide from your influences
5. **Project setup** - creates `quill.json`, directories, format files, and a reusable chapter scaffold helper
6. **Auto-generated outline** - complete chapter-by-chapter plan you can review and adjust, then materializes chapter stubs

Then start writing with `/quill:write 1`.

### Codex

Ask for the same workflow directly:

- `Use $quill to initialize a new fiction book in this folder.`
- `Use $quill to write chapter 1 from the current outline.`
- `Use $quill to revise chapter 3 and flag any downstream continuity impact.`
- `Use $quill to export this manuscript to Markdown.`

## Commands / Intents

In Claude Code these are slash commands. In Codex they are the corresponding requests you make to the `quill` skill.

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
2. **Each summary is stored in its own file** under `.quill/summaries/ch-NN.json`, not raw prose. Every summary keeps an `ending_excerpt` — the chapter's final ~150 words verbatim — for prose continuity.
3. **When writing the next chapter**, Quill builds a briefing under 1500 tokens from `quill.json` plus only the 3 nearest prior chapter summaries, the style fingerprint, active characters, open threads, and the chapter's outline brief.
4. **No full chapter is ever loaded** unless you're actively revising it.

This means chapter 20 writes with the same quality of context as chapter 2 — the compression scales to any book length.

Existing projects created before schema v2 migrate automatically on first use, or manually via `python3 scripts/quill-validate.py --migrate`.

## Project Structure

```
your-book/
├── quill.json              ← single source of truth (schema v2)
├── .quill/
│   └── summaries/          ← per-chapter summaries + ending excerpts (commit this)
├── book.tex                ← LaTeX wrapper (LaTeX projects only)
├── chapters/
│   ├── ch-01.tex or .md
│   ├── ch-02.tex or .md
│   └── ...
├── scripts/
│   ├── quill-sync-outline.py   ← refresh chapter stubs from the outline
│   ├── quill-validate.py       ← validate the project / migrate v1 → v2
│   └── quill-stats.py          ← accurate word counts and progress
├── characters/             ← fiction: detailed character sheets
├── concepts/               ← technical: detailed concept sheets
└── export/
    └── manuscript.md       ← assembled output (Markdown projects)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
