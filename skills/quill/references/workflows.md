# Quill Workflows

Canonical workflow spec for Quill, used on every platform. In Claude Code the `/quill:*` commands delegate here; in Codex (or anywhere without slash commands) translate the user's intent into the matching workflow directly.

Read [../SKILL.md](../SKILL.md) first for the compression contract, compaction rules, and format constraints. Load only the workflow section you need for the current request.

**Migration check (every workflow):** on the first action in any project, if `quill.json` lacks `schema_version`, run `python3 scripts/quill-validate.py --migrate` — or perform the migration by hand per [schema.md](schema.md) — before proceeding.

**Validation:** after any workflow that changes `quill.json` structurally (init, write, revise, outline edits, format switch), run `python3 scripts/quill-validate.py` when shell execution is available and fix anything it reports.

## Quick Map

- Start a new Quill project -> `Init Workflow`
- Write chapter `N` -> `Write Workflow`
- Revise chapter `N` -> `Revise Workflow`
- Show progress, threads, or revision risk -> `Status Workflow`
- View or edit the outline -> `Outline Workflow`
- View or resolve open threads -> `Threads Workflow`
- Add or update characters or concepts -> `Character / Concept Workflow`
- Switch between LaTeX and Markdown -> `Format Workflow`
- Assemble or convert the manuscript -> `Export Workflow`

## Init Workflow

Use when the user wants to start a new Quill book project.

1. If `quill.json` already exists, warn before overwriting anything and wait for explicit confirmation.
2. Run a structured interview in six phases. Ask all questions for a phase together, then wait. Do not assume the output format; Phase 3 must explicitly ask the author to choose `latex` or `markdown`.

### Phase 1: Foundation

Collect:
- Working title
- Book type: `fiction`, `nonfiction`, or `technical`
- Premise in 1-2 sentences
- Target reader
- Target length: short (~40k / ~10 chapters), standard (~80k / ~20 chapters), long (~120k / ~30 chapters), or custom

### Phase 2: Book-Type-Specific Questions

For fiction, collect:
- Genre
- Central conflict
- Narrative structure
- Protagonist
- Antagonist
- Setting
- POV and tense
- Tone
- Style influences or a writing sample

For nonfiction, collect:
- Thesis
- Reader's problem
- Structure preference
- Tone
- Narrator presence
- Style influences or a writing sample

For technical, collect:
- Technology or domain
- Prerequisites
- Reader goal
- Tutorial style
- Code language(s)
- Tone
- Style influences or a writing sample

### Phase 3: Output Format

Ask whether the project should use `latex` or `markdown`.

If `latex`, also collect:
- Document class (`book` default)
- Paper size (`letter` default)
- Font size (`11pt` default)
- Any special packages

### Phase 4: Style Fingerprint

Derive a one-line style fingerprint from the chosen influences and tone. Present it for approval and refine if needed.

### Phase 5: Create Project Files

Create `quill.json` using the canonical v2 schema from [schema.md](schema.md) — it must include `"schema_version": 2` and must **not** contain `chapter_summaries` or `last_chapter_ending` (per-chapter summaries live in `.quill/summaries/`).

Populate fields from the interview:
- Add protagonist and antagonist to `characters` for fiction when available.
- Leave `outline` empty until Phase 6.
- Use empty `concepts` until concepts are introduced or added explicitly.

Create the directory layout and all supporting files per [init-templates.md](init-templates.md):
- Directories: `.quill/summaries/`, `chapters/`, `export/`, `scripts/`, plus `characters/` (fiction) or `concepts/` (nonfiction/technical)
- Copy all three helper scripts from `../templates/` into `scripts/`: `quill-sync-outline.py`, `quill-validate.py`, `quill-stats.py`
- If format is `latex`, create `book.tex` from the preamble template
- Create the project `README.md` from the matching template

### Phase 6: Auto-Generate Outline

Generate a complete chapter outline based on book type and structure. Each outline entry uses the outline entry shape from [schema.md](schema.md).

Book-type requirements:
- Fiction: map chapters to the narrative structure and protagonist arc.
- Nonfiction: build a clear logical progression and include intro and conclusion chapters.
- Technical: respect prerequisite ordering and progressive code/concept buildup.

Before saving:
- Present the full outline.
- Ask whether the author wants adjustments.
- Apply edits.
- Save the final outline into `quill.json`.

After saving the outline:
- Create or refresh chapter stub files for every outline entry using `scripts/quill-sync-outline.py` or the same logic if shell execution is unavailable
- Markdown stubs must begin with `<!-- quill:chapter-stub -->`
- LaTeX stubs must begin with `% quill:chapter-stub`
- Never overwrite a chapter file that already contains drafted prose
- Report how many stubs were created or refreshed

Run `python3 scripts/quill-validate.py` when shell execution is available; expect `ok`.

Close by reporting planned chapters, total target word count, and the most natural next action.

## Write Workflow

Use when the user wants a new chapter drafted.

1. Read `quill.json`. If it does not exist, use the `Init Workflow` instead.
2. Determine the chapter number. If none is given, offer the next unwritten chapter after `last_chapter_written`.
3. Find the outline entry. If missing, ask for a brief or direct the user to the `Outline Workflow`.
4. Determine the chapter path from `format`:
   - `latex` -> `chapters/ch-NN.tex`
   - `markdown` -> `chapters/ch-NN.md`
5. If the chapter file already exists, inspect it before stopping:
   - If it still matches the Quill stub placeholder (`<!-- quill:chapter-stub -->` for Markdown or `% quill:chapter-stub` for LaTeX), treat it as a placeholder and overwrite it without asking
   - Otherwise ask before overwriting. If the user intends to modify it, use the `Revise Workflow`.
6. Build a briefing under 1500 tokens following the compression contract in `SKILL.md` ("What goes in a briefing"). Sources:
   - Book-level fields from `quill.json`
   - The 3 nearest prior *written* chapters' summary files from `.quill/summaries/`
   - For prose handoff, the `ending_excerpt` of the nearest prior written chapter (the immediate predecessor when it is written; otherwise the closest earlier written chapter)
7. Do not load full prior chapters unless the user explicitly asks. The briefing is the default context source. Targeted verification reads follow the caps in the compression contract.
8. Write the chapter:
   - `latex`: start with `\chapter{Title}` and write valid chapter-level LaTeX only.
   - `markdown`: write plain Markdown without a top-level chapter heading.
9. Self-summarize into `.quill/summaries/ch-NN.json` using the summary schema from [schema.md](schema.md), including `chapter` and `ending_excerpt` (the final ~150 words, verbatim). For `actual_word_count`, run `python3 scripts/quill-stats.py` when shell execution is available; otherwise estimate from the drafted text.
10. Update `quill.json` (small fields only — no prose, no summaries):
    - Update characters or concepts and `last_seen`
    - Update `world_rules`
    - Move opened and closed threads between `open_threads` and `resolved_threads`
    - Append any new continuity flags (flag objects with `added_in_chapter`)
    - Update `last_chapter_written` only if this chapter number is higher
    - Mark the outline entry as `written`
11. Apply compaction rules from `SKILL.md`, then validate.
12. Report actual word count, new threads, closed threads, new characters or concepts, and the best next action.

## Revise Workflow

Use when the user wants to improve an existing chapter or refresh metadata after manual edits.

1. Read `quill.json`.
2. Resolve the chapter path from the current format and read the full chapter.
3. Read the existing summary file `.quill/summaries/ch-NN.json`. Keep the old values for the continuity diff in step 8.
4. If this is not chapter 1, load the lightest continuity context that works: the previous written chapter's summary file, and its `ending_excerpt` if prose-level handoff matters.
5. Offer one of these modes:
   - Suggest revisions only
   - Rewrite a section
   - Full rewrite
   - Metadata-only refresh
6. Make the requested changes and save the chapter unless the user asked for suggestions only.
7. Re-summarize the revised chapter into `.quill/summaries/ch-NN.json`, refreshing every field including `ending_excerpt` and `actual_word_count` (via `quill-stats.py` when available).
8. Compare old and new summaries to detect continuity impact:
   - Characters added, removed, or materially changed
   - World facts changed
   - Threads opened or closed differently
   - `ending_excerpt` changed
9. Update `quill.json`:
   - Update characters, concepts, world rules, and thread state
   - Set the outline status to `revised`
   - Append a `revision_log` entry with the reason and continuity impact
   - Mark downstream written chapters as `needs-revision` when continuity was affected
10. Apply compaction rules, then validate.
11. Report what changed, the summary diff, downstream revision risk, and the best next action.

## Status Workflow

Use when the user wants the overall project state.

1. Read `quill.json`.
2. Run `python3 scripts/quill-stats.py` when shell execution is available for accurate word counts and progress; otherwise sum `actual_word_count` from the summary files in `.quill/summaries/`.
3. Report:
   - Book overview: title, type, format, structure, target words, written chapters, words written, estimated completion
   - Chapter map: one line per chapter with status (`written`, `revised`, `needs-revision`, `planned`)
   - Open threads, including stale-thread warnings when `last_chapter_written - opened_in_chapter >= 5`
   - The last three revision log entries
   - One to three suggested next actions based on the current state

## Outline Workflow

Use when the user wants to inspect, add, remove, or change outline entries.

1. Read `quill.json`.
2. If no chapter number is specified, show the full outline with chapter status, brief, purpose, and target words.
3. If a chapter number is specified and the entry exists:
   - Show the entry
   - Offer edits to title, brief, purpose, target word count, or part assignment
   - Warn that changing the outline does not rewrite existing chapter prose
4. If a chapter number is specified and the entry does not exist:
   - Ask for title
   - Ask for a 2-4 sentence brief
   - Ask for the chapter purpose
   - Ask for target words, defaulting to `structure.words_per_chapter`
   - Ask for the part if the project uses parts
5. Save the updated outline.
6. If the new chapter exceeds `structure.chapter_count`, update chapter count and target word count accordingly.
7. Keep the chapter scaffold in sync:
   - If `scripts/quill-sync-outline.py` is present, run it when shell execution is available
   - Otherwise create or refresh only the affected stub chapter files directly
   - Never overwrite non-stub chapter files
8. Validate.

## Threads Workflow

Use when the user wants to inspect or resolve open narrative or conceptual threads.

1. Read `quill.json`.
2. If no thread ID is given, list all `open_threads` with type, opening chapter, and stale warnings.
3. If the user wants to add a thread, collect:
   - ID slug
   - Description
   - Type: `plot`, `character`, `concept`, or `question`
   - Opening chapter, defaulting to `last_chapter_written`
4. If a thread ID is given, find it in `open_threads`, ask how it resolves and in which chapter, then:
   - Remove it from `open_threads`
   - Add it to `resolved_threads` with `resolved_in_chapter` and `resolution`
5. Save `quill.json`.
6. When showing threads, also include a short resolved-thread count and show resolved entries if the user asks.

## Character / Concept Workflow

Use when the user wants to maintain reference entries outside chapter prose.

1. Read `quill.json`.
2. Branch on `book_type`.

For fiction:
- No name -> list characters from `characters`
- With a name:
  - If the character exists, offer to update role, description, arc, relationships, and the detailed sheet
  - If not, collect role, description, arc, and relationships
  - Save the entry to `quill.json.characters`
  - Create or update `characters/<slug>.md`

For nonfiction or technical:
- No name -> list concepts from `concepts`
- With a name:
  - If the concept exists, offer to update definition, dependencies, and introduction chapter
  - If not, collect those fields
  - Save the entry to `quill.json.concepts`
  - Create or update `concepts/<slug>.md`

Keep sheet filenames lowercase with hyphens.

## Format Workflow

Use when the user wants to inspect or switch between LaTeX and Markdown.

1. Read `quill.json`.
2. If no target format is given, report the current format and how files are laid out.
3. If a target format is given:
   - Validate it is `latex` or `markdown`
   - If unchanged, say so and stop
   - Warn that chapter files will be renamed and converted, `book.tex` may be created or removed, and `quill.json` will change
   - Wait for explicit confirmation
4. Convert each chapter file with a deterministic in-repo pass following [format-conversion.md](format-conversion.md) — the per-construct rules, escaping, file-handling order, and edge cases live there. Do not check for `pandoc` or `pdflatex` as part of format switching.
5. If switching to `latex`, create `book.tex` with the standard wrapper and chapter `\input{}` lines.
6. If switching to `markdown`, remove `book.tex` if present.
7. Update `quill.json.format` and validate.
8. Report converted files and warn that complex markup may need manual review. Only mention missing `pandoc` or `pdflatex` if the user also asked for an export target that needs them.

## Export Workflow

Use when the user wants the manuscript assembled or converted.

1. Read `quill.json`.
2. Verify every written or revised chapter in `outline` has a matching file.
3. Branch on `format`. External tool checks belong here, not in the format-switch workflow.

For `latex`:
- Update `book.tex` to include `\input{chapters/ch-NN.tex}` for each existing written chapter
- If the user asked for PDF output, check for `pdflatex` and run it twice
- Otherwise stop after updating `book.tex`

For `markdown`:
- Assemble `export/manuscript.md` with the book title, optional part headings, chapter headings from `outline`, and chapter contents in order
- If the user asked for `docx` or `html`, check for `pandoc` and convert from the assembled Markdown

Always report:
- Number of chapters included
- Any chapters skipped or missing
- Total word count (via `python3 scripts/quill-stats.py` when shell execution is available)
- Output locations
- A warning when `needs-revision` chapters are included in the export
