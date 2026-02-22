---
name: quill-context
description: Automatically activate when a quill.json file is present in the project, when the user mentions writing a book or chapter, or when working inside a Quill book writing project.
allowed-tools: Read, Write
---

# Quill Context Skill

This skill auto-activates when working inside a Quill book project. It enforces the compression contract, format awareness, and non-linear writing patterns that make Quill work.

---

## Always Read quill.json First

Before any action on a Quill project, read `quill.json`. It is the single source of truth for:
- Book metadata (title, type, format, structure)
- Chapter outline and status
- Chapter summaries (compressed context)
- Characters and concepts
- Open and resolved threads
- Revision history
- Last chapter written and its ending

---

## Format Awareness

Check `quill.json.format` to determine how to handle files:

| | LaTeX | Markdown |
|---|---|---|
| Chapter files | `chapters/ch-NN.tex` | `chapters/ch-NN.md` |
| Chapter start | `\chapter{Title}` | No heading (added at export) |
| Wrapper file | `book.tex` with `\input{}` | None (assembled at export) |
| Export output | `book.pdf` via pdflatex | `export/manuscript.md` |
| Character sheets | `characters/name.md` | `characters/name.md` |
| Concept sheets | `concepts/name.md` | `concepts/name.md` |

Never mix formats. If the project is LaTeX, all chapter operations use `.tex`. If Markdown, all use `.md`.

---

## Compression Contract

This is the core design principle that allows Quill to handle book-length works within context limits.

### Rules:

1. **Never load full chapters unnecessarily.** Only load a chapter file when actively writing, revising, or when the user explicitly asks to see it.

2. **Briefings under 1500 tokens.** When writing a new chapter, build context from quill.json summaries — never from raw prose of previous chapters.

3. **`last_chapter_ending` is the only raw prose carried forward.** This field (~150 words) provides prose-level continuity. Everything else comes from compressed summaries.

4. **Chapter summaries are the memory.** After writing each chapter, self-summarize and store in `chapter_summaries`. This is how context is preserved without loading everything.

5. **Active characters/concepts from last 3 chapters only.** Don't load all characters into the briefing — only those active in recent chapters.

### What goes in a briefing:
- Title, genre, POV, style_fingerprint, setting, tone
- Active characters/concepts from last 3 chapters
- Continuity flags and relevant open threads
- This chapter's outline brief and purpose
- Last chapter ending (verbatim)
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

1. **Check `last_chapter_ending`** — If writing chapter 5 but `last_chapter_written` is 3, the `last_chapter_ending` refers to chapter 3, not chapter 4 (which doesn't exist yet). Handle gracefully.

2. **Check `revision_log`** — If a chapter was revised, later chapters may have `status: "needs-revision"`. Alert the user to potential continuity issues.

3. **Warn about downstream impact** — When revising an earlier chapter, compare old and new summaries. If characters, world facts, threads, or the ending changed, flag which later chapters may be affected.

4. **Update tracking fields correctly** — `last_chapter_written` should reflect the highest chapter number written, not the most recently touched chapter.

---

## Self-Summarization

After every chapter write or revision, the system must:

1. Extract a summary with all required fields:
   - `what_happened_or_covered`
   - `emotional_beat_or_takeaway`
   - `new_characters_or_concepts`
   - `new_world_facts`
   - `threads_or_questions_opened`
   - `threads_or_questions_closed`
   - `actual_word_count`

2. Update `quill.json` with the summary and all derived data (characters, threads, etc.)

3. Set `last_chapter_ending` to the final ~150 words of the chapter (verbatim prose)

This is not optional. Skipping self-summarization breaks the compression contract and causes context loss for future chapters.

---

## File Conventions

```
project-root/
├── quill.json              ← single source of truth
├── book.tex                ← LaTeX wrapper (LaTeX projects only)
├── chapters/
│   ├── ch-01.tex or .md    ← chapter files (zero-padded)
│   ├── ch-02.tex or .md
│   └── ...
├── characters/             ← fiction projects
│   ├── character-name.md   ← detailed character sheets
│   └── ...
├── concepts/               ← technical/nonfiction projects
│   ├── concept-name.md     ← detailed concept sheets
│   └── ...
└── export/
    ├── manuscript.md       ← assembled markdown (Markdown projects)
    └── ...
```

- Chapter files are zero-padded: `ch-01`, `ch-02`, ..., `ch-10`, `ch-11`
- Character and concept sheet filenames are lowercase with hyphens: `elena-vasquez.md`, `memory-allocation.md`
- The `export/` directory is for assembled output only — never put source files here
