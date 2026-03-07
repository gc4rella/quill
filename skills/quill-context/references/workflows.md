# Quill Workflows

Use this file when the user asks to operate Quill from Codex. Codex does not expose `/quill:*` slash commands, so translate the user's intent directly into the workflow below.

Read [../SKILL.md](../SKILL.md) first for the compression contract, compaction rules, and format constraints. Use only the section you need for the current request.

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
2. Run a structured interview in six phases. Ask all questions for a phase together, then wait.

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

Create `quill.json` with this baseline shape:

```json
{
  "title": "",
  "subtitle": "",
  "book_type": "fiction",
  "genre": "",
  "target_audience": "",
  "format": "markdown",
  "structure": {
    "model": "",
    "target_word_count": 80000,
    "chapter_count": 20,
    "words_per_chapter": 4000,
    "has_parts": false,
    "parts": []
  },
  "premise": "",
  "central_conflict_or_thesis": "",
  "tone": "",
  "pov": "",
  "style_fingerprint": "",
  "setting": "",
  "world_rules": [],
  "continuity_flags": [],
  "characters": {},
  "concepts": {},
  "outline": [],
  "chapter_summaries": {},
  "open_threads": [],
  "resolved_threads": [],
  "last_chapter_written": 0,
  "last_chapter_ending": "",
  "revision_log": []
}
```

Populate fields from the interview:
- Add protagonist and antagonist to `characters` for fiction when available.
- Leave `outline` empty until Phase 6.
- Use empty `concepts` until concepts are introduced or added explicitly.

Create:
- `chapters/`
- `export/`
- `characters/` for fiction
- `concepts/` for nonfiction and technical

If format is `latex`, create `book.tex` with:
- The chosen document class and options
- Standard packages such as `hyperref`, `geometry`, `fontenc`, and `inputenc`
- `\title{}`, `\author{}`, `\date{}`
- `\begin{document}`, `\maketitle`, `\tableofcontents`
- A placeholder comment for future chapter `\input{}` lines
- `\end{document}`

Create a project `README.md` that explains how to export the manuscript for the chosen format.

### Phase 6: Auto-Generate Outline

Generate a complete chapter outline based on book type and structure.

Each outline entry should include:

```json
{
  "chapter": 1,
  "part": null,
  "title": "Chapter Title",
  "brief": "2-4 sentence chapter plan.",
  "purpose": "Structural role of the chapter.",
  "target_words": 4000,
  "status": "planned"
}
```

Book-type requirements:
- Fiction: map chapters to the narrative structure and protagonist arc.
- Nonfiction: build a clear logical progression and include intro and conclusion chapters.
- Technical: respect prerequisite ordering and progressive code/concept buildup.

Before saving:
- Present the full outline.
- Ask whether the author wants adjustments.
- Apply edits.
- Save the final outline into `quill.json`.

Close by reporting planned chapters, total target word count, and the most natural next action.

## Write Workflow

Use when the user wants a new chapter drafted.

1. Read `quill.json`. If it does not exist, use the `Init Workflow` instead.
2. Determine the chapter number. If none is given, offer the next unwritten chapter after `last_chapter_written`.
3. Find the outline entry. If missing, ask for a brief or direct the user to the `Outline Workflow`.
4. Determine the chapter path from `format`:
   - `latex` -> `chapters/ch-NN.tex`
   - `markdown` -> `chapters/ch-NN.md`
5. If the chapter file already exists, ask before overwriting. If the user intends to modify it, use the `Revise Workflow`.
6. Build a briefing under 1500 tokens from:
   - Title
   - Genre or book type
   - POV and tense
   - Style fingerprint
   - Setting
   - Tone
   - Active characters or concepts from the three nearest prior written chapters by chapter number
   - Relevant continuity flags
   - Relevant open threads
   - This chapter's outline brief and purpose
   - `last_chapter_ending` only when it belongs to the immediate predecessor; otherwise use the previous chapter summary and read only a short closing excerpt from the previous chapter file if prose continuity is necessary
   - Target word count
7. Do not load full prior chapters unless the user explicitly asks. The briefing is the default context source.
8. Write the chapter:
   - `latex`: start with `\chapter{Title}` and write valid chapter-level LaTeX only.
   - `markdown`: write plain Markdown without a top-level chapter heading.
9. Self-summarize the chapter into:

```json
{
  "what_happened_or_covered": "2-3 sentence summary",
  "emotional_beat_or_takeaway": "key beat",
  "new_characters_or_concepts": [],
  "new_world_facts": [],
  "threads_or_questions_opened": [],
  "threads_or_questions_closed": [],
  "actual_word_count": 0
}
```

10. Update `quill.json`:
- Add the chapter summary
- Update characters or concepts and `last_seen`
- Update `world_rules`
- Move opened and closed threads between `open_threads` and `resolved_threads`
- Update `last_chapter_written` only if this chapter number is higher
- Set `last_chapter_ending` to the final ~150 words of the new chapter
- Mark the outline entry as `written`

11. Apply compaction rules from `SKILL.md`.
12. Report actual word count, new threads, closed threads, new characters or concepts, and the best next action.

## Revise Workflow

Use when the user wants to improve an existing chapter or refresh metadata after manual edits.

1. Read `quill.json`.
2. Resolve the chapter path from the current format and read the full chapter.
3. Read the existing chapter summary from `chapter_summaries[N]`.
4. If this is not chapter 1, load the lightest continuity context that works: prefer the previous chapter summary, use `last_chapter_ending` only when it belongs to chapter `N-1`, and read only the closing passage of the previous chapter file if prose-level handoff matters.
5. Offer one of these modes:
- Suggest revisions only
- Rewrite a section
- Full rewrite
- Metadata-only refresh
6. Make the requested changes and save the chapter unless the user asked for suggestions only.
7. Re-summarize the revised chapter using the same schema as the `Write Workflow`.
8. Compare old and new summaries to detect continuity impact:
- Characters added, removed, or materially changed
- World facts changed
- Threads opened or closed differently
- Chapter ending changed
9. Update `quill.json`:
- Replace `chapter_summaries[N]`
- Update `last_chapter_ending` if this is the last written chapter, or note ending changes in continuity impact
- Update characters, concepts, world rules, and thread state
- Set the outline status to `revised`
- Append a `revision_log` entry with the reason and continuity impact
- Mark downstream written chapters as `needs-revision` when continuity was affected
10. Apply compaction rules.
11. Report what changed, the summary diff, downstream revision risk, and the best next action.

## Status Workflow

Use when the user wants the overall project state.

Read `quill.json` and report:
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
4. Convert each chapter file with a deterministic in-repo pass. Do not check for `pandoc` or `pdflatex` as part of format switching.
- Markdown -> LaTeX:
  - add `\chapter{Title}`
  - convert headings, bold, italics, inline code, code fences, horizontal rules, lists, blockquotes, links, and footnotes when straightforward
  - convert simple tables only when the structure is unambiguous; otherwise preserve the content and flag manual review
  - escape LaTeX special characters in prose, but not inside commands or verbatim blocks
  - preserve meaning for unsupported Markdown features instead of dropping content
- LaTeX -> Markdown:
  - remove `\chapter{...}`
  - convert headings, emphasis, inline code, verbatim blocks, `\bigskip`, lists, quote environments, links, and footnotes when straightforward
  - flatten custom macros and unsupported environments conservatively, then flag manual review
  - unescape LaTeX special characters
- Write all new target-format files first. Remove old source files only after the new set is complete.
- If you need an assembled snapshot or scratch output during conversion, keep it under `export/`.
5. If switching to `latex`, create `book.tex` with the standard wrapper and chapter `\input{}` lines.
6. If switching to `markdown`, remove `book.tex` if present.
7. Update `quill.json.format`.
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
- Total word count
- Output locations
- A warning when `needs-revision` chapters are included in the export
