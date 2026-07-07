---
name: quill
description: Activate when a quill.json file is present, when the user mentions Quill, or when the user wants to plan, draft, write, revise, or outline a book, novel, manuscript, or technical book — including managing chapters, threads, characters, or concepts, switching between LaTeX and Markdown, checking progress, or exporting the manuscript.
allowed-tools: Read, Write, Bash
---

# Quill Skill

This skill works in both Claude Code and Codex. It enforces the compression contract, format awareness, and non-linear writing patterns that make Quill work.

---

## Workflow Routing

In Claude Code, prefer the `/quill:*` slash commands when the user invokes them. Codex does not expose those commands. When no command was invoked, translate the user's intent directly into the matching workflow from [`references/workflows.md`](references/workflows.md):

- Start a new project or initialize Quill -> `Init Workflow`
- Write a chapter -> `Write Workflow`
- Revise a chapter -> `Revise Workflow`
- Inspect progress -> `Status Workflow`
- Edit or extend the outline -> `Outline Workflow`
- Manage threads -> `Threads Workflow`
- Manage characters or concepts -> `Character / Concept Workflow`
- Switch between LaTeX and Markdown -> `Format Workflow`
- Assemble or convert the manuscript -> `Export Workflow`

Load only the workflow section needed for the current request. `references/workflows.md` is the canonical spec on every platform.

---

## Project State: quill.json + Summary Files

Before any action on an existing Quill project, read `quill.json`. If it does not exist and the user wants to start a new book, use the `Init Workflow`.

The canonical schema (v2) lives in [`references/schema.md`](references/schema.md). Two-part state model:

- **`quill.json`** — book metadata, outline and chapter status, characters and concepts, open/resolved threads, continuity flags, world rules, revision log, `last_chapter_written`. Small fields only; never store prose or summaries here.
- **`.quill/summaries/ch-NN.json`** — one file per written chapter: the chapter summary plus `ending_excerpt` (final ~150 words, verbatim). These files are the project's memory.

**Migration:** if `quill.json` lacks `schema_version`, the project is v1. Run `python3 scripts/quill-validate.py --migrate` (or migrate by hand per `schema.md`) before doing anything else.

---

## Initialization Contract

When starting a new Quill project, always run the six-phase questionnaire from the `Init Workflow`. Do not infer the output format from context or taste; explicitly ask whether the project should use `latex` or `markdown`, then apply the format-specific setup.

Every newly initialized project gets all three bundled helper scripts copied from [`templates/`](templates/) into the project's `scripts/` directory: `quill-sync-outline.py`, `quill-validate.py`, `quill-stats.py`. Directory layout, `book.tex` preamble, and project README templates live in [`references/init-templates.md`](references/init-templates.md).

Chapter stubs created by Quill must begin with a format-specific marker so later workflows can treat them as placeholders:
- Markdown: `<!-- quill:chapter-stub -->`
- LaTeX: `% quill:chapter-stub`

If a chapter file still matches the Quill stub placeholder, the write workflow may replace it without asking for overwrite confirmation.

---

## Format Awareness

Check `quill.json.format` to determine how to handle files:

| | LaTeX | Markdown |
|---|---|---|
| Chapter files | `chapters/ch-NN.tex` | `chapters/ch-NN.md` |
| Chapter start | `\chapter{Title}` | No heading (added at export) |
| Assembled source output | `book.tex` with `\input{}` | `export/manuscript.md` |
| Optional compiled output | `book.pdf` via `pdflatex` if available | `export/manuscript.docx` / `.html` via `pandoc` if available |
| Character sheets | `characters/name.md` | `characters/name.md` |
| Concept sheets | `concepts/name.md` | `concepts/name.md` |

Never mix formats. If the project is LaTeX, all chapter operations use `.tex`. If Markdown, all use `.md`.

## Toolchain Boundary

Treat format conversion and export as separate operations:

1. **Format switching (`markdown` <-> `latex`) is an in-repo source conversion.** It does not require `pandoc`, `pdflatex`, or any other external converter. The per-construct conversion rules live in [`references/format-conversion.md`](references/format-conversion.md).
2. **Export and compilation happen after the sources are in the right format.**
   - LaTeX projects always maintain `book.tex`; PDF compilation is optional and depends on a LaTeX engine being installed.
   - Markdown projects always maintain `export/manuscript.md`; DOCX/HTML conversion is optional and depends on `pandoc`.

When external tools are missing, do not frame the format switch as blocked or degraded. Proceed with the deterministic in-repo conversion, handle supported markup explicitly, and call out only the constructs that may need manual cleanup.

Keep generated artifacts separate from source files:

- Source chapters live only in `chapters/` and must all share the active extension from `quill.json.format`.
- Assembled manuscripts, temporary snapshots, and conversion intermediates belong under `export/`, never in `chapters/`.
- After a successful switch, do not leave both `.md` and `.tex` versions of the same chapter in place.

---

## Compression Contract

This is the core design principle that allows Quill to handle book-length works within context limits.

### Rules:

1. **Never load full chapters unnecessarily.** Only load a chapter file when actively writing, revising, or when the user explicitly asks to see it.

2. **Briefings under 1500 tokens.** When writing a new chapter, build context from `quill.json` plus per-chapter summary files — never from raw prose of previous chapters.

3. **`ending_excerpt` is the only raw prose carried forward.** Each summary file keeps the final ~150 words of its chapter verbatim. Prose handoff uses the `ending_excerpt` of the nearest prior *written* chapter. Everything else comes from compressed summaries.

4. **Summary files are the memory.** After writing each chapter, self-summarize into `.quill/summaries/ch-NN.json`. This is how context is preserved without loading everything.

5. **Active characters/concepts from the 3 nearest prior written chapters only.** Don't load all characters into the briefing, and don't pull continuity from later chapters unless the user explicitly asks. Exception: characters or concepts named in the current chapter's outline brief are always included, even if last seen outside that window.

6. **Targeted verification reads are allowed; wholesale rereads are not.** If the user flags a specific chapter as a continuity risk, read that chapter, extract the hard facts into the briefing, and discard the prose. Cap: at most 2 full-chapter verification reads per task, and only for individually named chapters — if the user names more than 2, ask which matter most for this chapter. Blanket phrasing ("all previous chapters", "everything so far", "be careful about continuity") names nothing and licenses zero rereads — summaries, threads, and continuity flags are the continuity mechanism. If that feels insufficient, say so and invite the author to name the 1–2 chapters they actually worry about.

7. **Summaries are trusted unless suspect.** If there is concrete reason to doubt a chapter summary (e.g., a reported contradiction), verify it against the chapter file and repair the summary before relying on it.

### What goes in a briefing:
- Title, genre, POV, style_fingerprint, setting, tone
- Active characters/concepts from the 3 nearest prior written chapters (quill.json entries; read a `characters/` or `concepts/` sheet only when that entry is central to this chapter)
- Continuity flags and relevant open threads — if more threads are relevant than the budget allows (e.g., a convergence chapter), include in full only the threads explicitly named in this chapter's outline brief and compress the rest to one line each
- This chapter's outline brief and purpose
- `ending_excerpt` of the nearest prior written chapter (verbatim)
- Target word count

### What does NOT go in a briefing:
- Full text of any chapter
- All characters (only recently active ones)
- All threads (only relevant ones)
- Historical revision log entries
- Resolved threads

---

## Non-Linear Work Patterns

Quill supports writing and revising chapters in any order. When working non-linearly:

1. **Pick the right prose handoff** — Use the `ending_excerpt` from the summary file of the nearest prior *written* chapter. If writing chapter 5 and chapter 4 is unwritten but chapter 3 is written, hand off from chapter 3's `ending_excerpt`.

2. **Check `revision_log`** — If a chapter was revised, later chapters may have `status: "needs-revision"`. Alert the user to potential continuity issues.

3. **Warn about downstream impact** — When revising an earlier chapter, compare old and new summaries. If characters, world facts, threads, or the ending changed, flag which later chapters may be affected.

4. **Update tracking fields correctly** — `last_chapter_written` should reflect the highest chapter number written, not the most recently touched chapter.

---

## Auto-Compaction

Project state grows as chapters are written. To keep it manageable, enforce these compaction rules automatically:

### When to compact

Run compaction **after every chapter write or revision** and whenever `quill.json` is updated.

### Compaction rules

1. **Chapter summaries** — `what_happened_or_covered` must stay under 3 sentences. If a summary is longer after self-summarization, condense it immediately in the summary file.

2. **Resolved threads** — Keep only the last 10 resolved threads. When `resolved_threads` exceeds 10 entries, remove the oldest (lowest `resolved_in_chapter`). They've served their purpose.

3. **Revision log** — Keep only the last 10 entries. Older revision history is not needed for active writing decisions.

4. **Character `last_seen`** — Only store the most recent `last_seen` value. Don't accumulate history.

5. **`ending_excerpt`** — Hard cap at 150 words per summary file. If longer, trim from the beginning to keep the final 150 words.

6. **World rules** — Deduplicate. If two `world_rules` entries express the same fact, merge them into one.

7. **Open threads** — If an open thread was both opened and closed in the same chapter, skip adding it to `open_threads` entirely — record it only in `resolved_threads`.

8. **Continuity flags** — Cap at 20 entries. Flags are objects with `added_in_chapter` (see `schema.md`); always append new flags at the end, and treat legacy string entries as `added_in_chapter: 0`. When over the cap, auto-remove flags where `last_chapter_written - added_in_chapter >= 10` (oldest first) until the count reaches 20, then stop. List the removed flags in your end-of-task report. Only if still over 20 after that, ask the author which to keep.

### Compaction is silent

Don't announce compaction to the user and never block on a question for it (the rule-8 fallback is the one exception). Just do it as part of the quill.json update. When compaction dropped data the user might care about (e.g., removed continuity flags), note it briefly in your report after the fact.

---

## Self-Summarization

After every chapter write or revision, the system must:

1. Write `.quill/summaries/ch-NN.json` with all required fields (canonical shape in [`references/schema.md`](references/schema.md)):
   - `chapter`
   - `what_happened_or_covered`
   - `emotional_beat_or_takeaway`
   - `new_characters_or_concepts`
   - `new_world_facts`
   - `threads_or_questions_opened`
   - `threads_or_questions_closed`
   - `actual_word_count` — via `python3 scripts/quill-stats.py` when shell execution is available, otherwise estimated
   - `ending_excerpt` — the final ~150 words of the chapter, verbatim

2. Update `quill.json` with the derived small fields (characters, threads, world rules, outline status, `last_chapter_written`).

This is not optional. Skipping self-summarization breaks the compression contract and causes context loss for future chapters.

---

## File Conventions

```
project-root/
├── quill.json              ← single source of truth (v2, small fields only)
├── .quill/
│   └── summaries/
│       ├── ch-01.json      ← per-chapter summaries + ending excerpts (commit this)
│       └── ...
├── book.tex                ← LaTeX wrapper (LaTeX projects only)
├── chapters/
│   ├── ch-01.tex or .md    ← chapter files (zero-padded)
│   ├── ch-02.tex or .md
│   └── ...
├── scripts/
│   ├── quill-sync-outline.py
│   ├── quill-validate.py
│   └── quill-stats.py
├── characters/             ← fiction projects
│   ├── character-name.md   ← detailed character sheets
│   └── ...
├── concepts/               ← technical/nonfiction projects
│   ├── concept-name.md     ← detailed concept sheets
│   └── ...
└── export/
    ├── manuscript.md       ← assembled markdown (Markdown projects)
    └── ...                 ← optional conversion intermediates
```

- Chapter files are zero-padded: `ch-01`, `ch-02`, ..., `ch-10`, `ch-11`
- Character and concept sheet filenames are lowercase with hyphens: `elena-vasquez.md`, `memory-allocation.md`
- `scripts/quill-sync-outline.py` is safe to rerun after outline edits; it updates only stub chapter files
- `.quill/` must be committed with the book project — it is project memory, not a cache
- The `export/` directory is for assembled output and conversion intermediates — never put source files here
