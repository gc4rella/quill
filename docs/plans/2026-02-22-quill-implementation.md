# Quill Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Claude Code plugin for writing books chapter by chapter with minimal context — guided init wizard, context compression, non-linear revision, LaTeX/Markdown dual format.

**Architecture:** Pure markdown plugin — no scripts, no dependencies, no external APIs. All files are `.md` or `.json`. Claude Code's built-in LLM handles writing, summarizing, and analysis via Read/Write tools. Project state lives in `quill.json`, which the commands read and update.

**Tech Stack:** Claude Code plugin system (plugin.json, commands/, agents/, skills/), Markdown, JSON.

---

### Task 1: Plugin Manifest

**Files:**
- Create: `.claude-plugin/plugin.json`

**Step 1: Create the plugin manifest**

```json
{
  "name": "quill",
  "description": "AI-powered book writing assistant for fiction and nonfiction. Guided setup, automatic outline generation, chapter-by-chapter writing with context compression, LaTeX or Markdown output, and non-linear revision support.",
  "version": "0.1.0",
  "author": {
    "name": "Giuseppe",
    "url": "https://github.com/giuseppe/quill"
  },
  "repository": "https://github.com/giuseppe/quill",
  "license": "MIT"
}
```

**Step 2: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: add plugin manifest"
```

---

### Task 2: Init Wizard Command

**Files:**
- Create: `commands/quill-init.md`

**Step 1: Create the init command**

This is the most important file. It runs the 6-phase structured interview and auto-generates a complete chapter outline. Write the full content from the design doc's Step 3 verbatim — all 6 phases, all book-type branches, format selection, style fingerprint derivation, project file creation, and outline generation.

The command frontmatter:

```yaml
---
description: Start a new Quill book project with a guided setup wizard. Collects all context needed to auto-generate a complete chapter outline. Run this once at the start of any new book.
argument-hint: (optional) working title
allowed-tools: Read, Write
---
```

Key sections to include in order:
- Phase 1: Foundation questions (title, type, premise, audience, length)
- Phase 2: Book-type-specific questions (fiction / nonfiction / technical branches)
- Phase 3: Output format (LaTeX vs Markdown with LaTeX follow-ups)
- Phase 4: Style fingerprint derivation
- Phase 5: Project file creation (quill.json, directories, book.tex if LaTeX)
- Phase 6: Auto-generate outline with book-type-specific requirements, present to author for review

Refer to the design doc at `docs/plans/2026-02-22-quill-plugin-design.md` for the complete content of each phase — copy it faithfully into the command file.

**Step 2: Commit**

```bash
git add commands/quill-init.md
git commit -m "feat: add /quill:init wizard command"
```

---

### Task 3: Write Command

**Files:**
- Create: `commands/quill-write.md`

**Step 1: Create the write command**

Frontmatter:

```yaml
---
description: Write a specific chapter using compressed context from quill.json. Automatically self-summarizes and updates quill.json after writing.
argument-hint: chapter number (e.g. 3)
allowed-tools: Read, Write
---
```

Body must cover all 8 steps from the design:
1. Read quill.json
2. Find outline entry (stop if missing)
3. Check for existing chapter file, confirm before overwriting
4. Build briefing under 1500 tokens (title, genre, POV, style_fingerprint, setting, tone, active characters/concepts from last 3 chapters, continuity_flags, open_threads, outline brief, last_chapter_ending, target word count)
5. Write the chapter (format-aware: LaTeX saves to `chapters/ch-NN.tex` with `\chapter{}`, Markdown saves to `chapters/ch-NN.md` without heading)
6. Self-summarize (all summary fields)
7. Update quill.json (summary, characters, concepts, world_rules, threads, last_chapter_written, last_chapter_ending, status)
8. Report (word count vs target, new threads, new characters/concepts)

Copy the complete write command content from the design doc.

**Step 2: Commit**

```bash
git add commands/quill-write.md
git commit -m "feat: add /quill:write command"
```

---

### Task 4: Revise Command

**Files:**
- Create: `commands/quill-revise.md`

**Step 1: Create the revise command**

Frontmatter:

```yaml
---
description: Revisit and revise a chapter that has already been written. Re-summarizes after revision and warns about continuity impact on later chapters.
argument-hint: chapter number (e.g. 3)
allowed-tools: Read, Write
---
```

Body must cover all 10 steps from the design:
1. Read quill.json
2. Load chapter file (format-aware)
3. Load existing chapter_summaries[N]
4. Load last_chapter_ending of ch N-1
5. Show revision options (suggest / rewrite section / full rewrite / metadata-only)
6. Make changes, save file
7. Re-summarize
8. Detect continuity impact (characters, world facts, threads, ending)
9. Update quill.json (summary, last_chapter_ending, status → "revised", revision_log entry)
10. Report (diff vs old summary, downstream chapter warnings, suggest /quill:status)

Copy the complete revise command content from the design doc.

**Step 2: Commit**

```bash
git add commands/quill-revise.md
git commit -m "feat: add /quill:revise command"
```

---

### Task 5: Status Command

**Files:**
- Create: `commands/quill-status.md`

**Step 1: Create the status command**

Frontmatter:

```yaml
---
description: Show the full status of the book — chapters written, word count progress, open threads, and any chapters that may need revision due to earlier changes.
allowed-tools: Read
---
```

Body displays:
- Book Overview (title, type, format, target word count, chapters written/planned, actual/target word count, estimated completion)
- Chapter Map (one line per chapter with status emoji: ✅ ✏️ ⚠️ 📋)
- Open Threads (flag stale ones open 5+ chapters)
- Recent Revision Log (last 3 entries)
- Suggested Next Steps

Copy from design doc.

**Step 2: Commit**

```bash
git add commands/quill-status.md
git commit -m "feat: add /quill:status command"
```

---

### Task 6: Outline Command

**Files:**
- Create: `commands/quill-outline.md`

**Step 1: Create the outline command**

Frontmatter:

```yaml
---
description: View the full chapter outline or add and update individual chapter entries.
argument-hint: (optional) chapter number and title
allowed-tools: Read, Write
---
```

Body:
- No arguments: display full outline (number, part, title, brief, purpose, target words, status)
- With chapter number: show if exists (ask what to update), create if doesn't (ask for details)
- Save all changes to quill.json

Copy from design doc.

**Step 2: Commit**

```bash
git add commands/quill-outline.md
git commit -m "feat: add /quill:outline command"
```

---

### Task 7: Threads Command

**Files:**
- Create: `commands/quill-threads.md`

**Step 1: Create the threads command**

Frontmatter:

```yaml
---
description: View all open plot threads or concept questions. For fiction: unresolved narrative threads. For technical books: concepts introduced but not yet fully resolved or applied.
argument-hint: (optional) thread ID to resolve
allowed-tools: Read, Write
---
```

Body:
- No argument: list all open_threads with ID, description, type, chapter opened, staleness warning
- With thread ID: ask for resolution note and chapter, move to resolved_threads

Copy from design doc.

**Step 2: Commit**

```bash
git add commands/quill-threads.md
git commit -m "feat: add /quill:threads command"
```

---

### Task 8: Character Command

**Files:**
- Create: `commands/quill-character.md`

**Step 1: Create the character command**

Frontmatter:

```yaml
---
description: Add or update a character (fiction) or key concept (technical/nonfiction) in quill.json.
argument-hint: name
allowed-tools: Read, Write
---
```

Body:
- Fiction: add/update character card in quill.json + detailed `characters/name.md`
- Technical/nonfiction: add/update concept in quill.json.concepts + `concepts/name.md`
- Read quill.json first, check existence, show existing entry, ask what to change

Copy from design doc.

**Step 2: Commit**

```bash
git add commands/quill-character.md
git commit -m "feat: add /quill:character command"
```

---

### Task 9: Export Command

**Files:**
- Create: `commands/quill-export.md`

**Step 1: Create the export command**

Frontmatter:

```yaml
---
description: Assemble all written chapters into a final manuscript. Produces PDF (LaTeX) or a single document (Markdown).
argument-hint: (optional) "pdf" to compile LaTeX to PDF, "docx" or "html" for markdown
allowed-tools: Read, Write, Bash
---
```

Body:
- LaTeX path: verify book.tex \input entries, run pdflatex if "pdf" requested, report output
- Markdown path: concatenate chapters with headings, write to export/manuscript.md, run pandoc for docx/html if requested
- Warn if tools not found

Copy from design doc.

**Step 2: Commit**

```bash
git add commands/quill-export.md
git commit -m "feat: add /quill:export command"
```

---

### Task 10: Expert Agent

**Files:**
- Create: `agents/quill-expert.md`

**Step 1: Create the expert agent**

Frontmatter:

```yaml
---
name: quill-expert
description: Book writing expert for Quill projects. Invoke when the user wants to write a book, continue writing chapters, revise earlier work, plan the structure, or discuss their manuscript.
---
```

Body covers:
- Core workflow knowledge (starting, writing, revising, jumping between chapters)
- Book type awareness (fiction, nonfiction, technical)
- Format awareness (LaTeX vs Markdown)
- Tone (thoughtful collaborator, push back gently, celebrate progress)

Copy from design doc.

**Step 2: Commit**

```bash
git add agents/quill-expert.md
git commit -m "feat: add quill-expert agent"
```

---

### Task 11: Context Skill

**Files:**
- Create: `skills/quill-context/SKILL.md`

**Step 1: Create the auto-activating skill**

Frontmatter:

```yaml
---
name: quill-context
description: Automatically activate when a quill.json file is present in the project, when the user mentions writing a book or chapter, or when working inside a Quill book writing project.
allowed-tools: Read, Write
---
```

Body covers:
- Always read quill.json first
- Format awareness (check quill.json.format)
- Compression contract (never load unnecessary chapters, briefings under 1500 tokens, last_chapter_ending is only raw prose carried)
- Non-linear work (check last_chapter_ending, revision_log, warn about downstream impact)
- Self-summarization
- File conventions (chapters, book.tex, character sheets, concept sheets, export, quill.json)

Copy from design doc.

**Step 2: Commit**

```bash
git add skills/quill-context/SKILL.md
git commit -m "feat: add quill-context auto-activating skill"
```

---

### Task 12: README

**Files:**
- Create: `README.md`

**Step 1: Create the README**

Content from design doc Step 10:
- Title and description
- Install instructions
- Start a new book section
- Core commands table
- Output formats section
- Non-linear writing section
- How context compression works section

Copy from design doc.

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

### Task 13: Manual End-to-End Verification (Fiction, LaTeX)

**No files to create.** This is a verification task.

**Step 1: Load plugin and run init**

```bash
claude --plugin-dir ./
```

Run `/quill:init` and walk through a fiction book setup:
- Title: "The Memory Thief"
- Type: fiction
- Premise: "A disgraced archivist discovers her city's collective memory is being harvested by an underground syndicate."
- Target reader: adult fiction readers
- Length: short (10 chapters)
- Genre: sci-fi thriller
- Structure: three-act
- Format: LaTeX

**Step 2: Verify init output**

Check that:
- `quill.json` exists with all fields populated including a 10-chapter outline
- `chapters/` directory exists
- `book.tex` exists with preamble
- `export/` directory exists

**Step 3: Write chapters 1 and 2**

Run `/quill:write 1` then `/quill:write 2`.

Verify after each:
- Chapter file created as `chapters/ch-01.tex` / `chapters/ch-02.tex`
- `chapter_summaries` populated in quill.json
- `last_chapter_written` updated
- `last_chapter_ending` set
- Outline status updated to "written"

**Step 4: Revise chapter 1**

Run `/quill:revise 1`.

Verify:
- Chapter file updated
- `chapter_summaries["1"]` replaced
- `revision_log` has entry
- Continuity warnings displayed if applicable

**Step 5: Check status**

Run `/quill:status`. Verify it shows accurate progress.

**Step 6: Export**

Run `/quill:export`. Verify book.tex has correct \input entries.

---

### Task 14: Manual End-to-End Verification (Technical, Markdown)

**No files to create.** This is a verification task.

**Step 1: Start fresh and run init**

Remove test artifacts from Task 13, then:

```bash
claude --plugin-dir ./
```

Run `/quill:init`:
- Title: "Rust From Scratch"
- Type: technical
- Premise: "A ground-up tutorial on systems programming with Rust for web developers"
- Target reader: JavaScript/Python developers with no systems background
- Length: standard (20 chapters)
- Tutorial style: bottom-up
- Format: Markdown

**Step 2: Verify init output**

Check that:
- `quill.json` exists with all fields, 20-chapter outline, concepts map
- `chapters/` directory exists
- No `book.tex` (Markdown format)
- `export/` directory exists

**Step 3: Write chapters 1 and 2, then export**

Run `/quill:write 1`, `/quill:write 2`, `/quill:export`.

Verify:
- Chapters saved as `chapters/ch-01.md`, `chapters/ch-02.md`
- `export/manuscript.md` generated with chapter headings
- quill.json properly updated after each write
