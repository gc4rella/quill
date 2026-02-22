# QUILL — Claude Code Plugin Design

## What We Are Building

Quill is a **Claude Code plugin** for writing books chapter by chapter with minimal context.
It is entirely markdown files — no scripts, no dependencies, no external API calls, no build step.
Claude Code's built-in LLM does all writing, summarizing, and analysis.

### Key Design Principles

- **Deep initialization**: a guided wizard that understands the book well enough to auto-generate a first-pass outline before a single word of prose is written
- **Format choice**: the user picks LaTeX or Markdown at init time; all chapter files, export, and structure follow that choice throughout
- **Non-linear writing**: chapters can be revisited, revised, and reordered at any time; quill.json tracks the impact and warns of continuity ripple effects
- **Fiction and nonfiction/technical**: the wizard branches based on book type and asks the right questions for each

---

## Plugin Structure

```
quill/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── quill-expert.md          ← main conversational agent
├── commands/
│   ├── quill-init.md            ← /quill:init  (the deep wizard)
│   ├── quill-write.md           ← /quill:write [N]
│   ├── quill-revise.md          ← /quill:revise [N]
│   ├── quill-outline.md         ← /quill:outline
│   ├── quill-status.md          ← /quill:status  (bird's eye view)
│   ├── quill-threads.md         ← /quill:threads  (fiction) / concepts (technical)
│   ├── quill-character.md       ← /quill:character [name]
│   └── quill-export.md          ← /quill:export
├── skills/
│   └── quill-context/
│       └── SKILL.md
└── README.md
```

---

## quill.json Schema

The complete schema. Claude reads and writes this with native Read/Write tools.

```json
{
  "title": "string",
  "subtitle": "string or empty",
  "book_type": "fiction | nonfiction | technical",
  "genre": "string",
  "target_audience": "string",
  "format": "latex | markdown",

  "structure": {
    "model": "string — e.g. three-act, save-the-cat, hero-journey, part-chapter, tutorial-progression",
    "target_word_count": 80000,
    "chapter_count": 20,
    "words_per_chapter": 4000,
    "has_parts": false,
    "parts": [
      { "number": 1, "title": "string", "chapter_range": "1-7" }
    ]
  },

  "premise": "string — 2-3 sentences",
  "central_conflict_or_thesis": "string",
  "tone": "string",
  "pov": "string",
  "style_fingerprint": "string — dense one-line voice description",
  "setting": "string",

  "world_rules": ["canonical facts that must stay consistent"],
  "continuity_flags": ["must-remember details across chapters"],

  "characters": {
    "Name": {
      "role": "protagonist | antagonist | supporting | mentor",
      "description": "one line",
      "arc": "where they start and where they end",
      "relationships": ["relationship strings"],
      "last_seen": "ch-N, brief note"
    }
  },

  "concepts": {
    "ConceptName": {
      "definition": "one-line definition",
      "introduced_in_chapter": 3,
      "depends_on": ["other concept names"]
    }
  },

  "outline": [
    {
      "chapter": 1,
      "part": 1,
      "title": "string",
      "brief": "2-4 sentence plan",
      "purpose": "string — structural role",
      "target_words": 4000,
      "status": "planned | written | revised | needs-revision"
    }
  ],

  "chapter_summaries": {
    "1": {
      "what_happened_or_covered": "2-3 sentences",
      "emotional_beat_or_takeaway": "string",
      "new_characters_or_concepts": [],
      "new_world_facts": [],
      "threads_or_questions_opened": [],
      "threads_or_questions_closed": [],
      "actual_word_count": 3800
    }
  },

  "open_threads": [
    {
      "id": "short-slug",
      "description": "string",
      "opened_in_chapter": 2,
      "type": "plot | character | concept | question"
    }
  ],
  "resolved_threads": [],

  "last_chapter_written": 0,
  "last_chapter_ending": "Final ~150 words of last chapter verbatim",

  "revision_log": [
    {
      "chapter": 3,
      "revised_at": "after chapter 7",
      "reason": "string",
      "continuity_impact": "string"
    }
  ]
}
```

---

## Commands

### /quill:init — The Deep Wizard (Most Important Command)

Runs a structured interview in 6 phases and ends by auto-generating a complete chapter outline.

**Phase 1 — Foundation** (all book types):
1. Working title
2. Book type: fiction / nonfiction / technical
3. One-sentence premise
4. Target reader
5. Target length (short/standard/long/custom)

**Phase 2 — Book-type-specific questions**:

- **Fiction**: genre, central conflict, narrative structure (three-act / save-the-cat / hero's journey / five-act / nonlinear), protagonist, antagonist, setting, POV/tense, tone, style
- **Nonfiction**: thesis, reader's problem, structure preference, tone, narrator presence, style
- **Technical**: technology/domain, prerequisites, reader goal, tutorial style, code language(s), tone, style

**Phase 3 — Output format**: LaTeX or Markdown (with LaTeX-specific follow-ups)

**Phase 4 — Style fingerprint derivation**: Derive from sample/references, show to author for approval

**Phase 5 — Project file creation**: Create quill.json, directories, and book.tex (if LaTeX)

**Phase 6 — Auto-generate outline**: Complete chapter-by-chapter outline mapped to chosen structure. Author reviews and adjusts before finalizing.

### /quill:write N

1. Read quill.json, build a briefing under 1500 tokens
2. Write the chapter matching style_fingerprint and tone
3. Save to `chapters/ch-NN.tex` or `chapters/ch-NN.md`
4. Self-summarize: extract all summary fields
5. Update quill.json with summary, threads, characters, concepts
6. Report word count vs target

### /quill:revise N

1. Load chapter and existing summary
2. Offer options: suggest revisions / rewrite section / full rewrite / metadata-only update
3. Make changes, re-summarize
4. Detect continuity impact vs old summary
5. Update quill.json, add to revision_log
6. Warn about downstream chapter impact

### /quill:status

Bird's-eye view: chapters written vs planned, word count progress, open threads, revision log, suggested next steps.

### /quill:outline

View full outline or add/update individual chapter entries.

### /quill:threads

View open threads with staleness warnings. Resolve threads by ID.

### /quill:character [name]

Add or update character cards (fiction) or concept entries (technical/nonfiction).

### /quill:export

Assemble manuscript: PDF via pdflatex (LaTeX) or concatenated MD/DOCX/HTML via pandoc (Markdown).

---

## Agent: quill-expert

Conversational book writing collaborator. Activates when user wants to write, continue, revise, plan, or discuss their manuscript. Understands all three book types and both formats. Follows the compression contract (briefings under 1500 tokens, summaries not raw prose).

## Skill: quill-context

Auto-activates when quill.json is present. Enforces format awareness, compression contract, non-linear work patterns, and self-summarization.

---

## Key Constraints

1. No external API calls — Claude is the LLM
2. No build step — zero code, zero dependencies
3. Format set at init, never changes
4. Briefings under 1500 tokens
5. Non-linear writing is first-class
6. Init must produce a complete outline
7. Idempotent init — never overwrite without confirmation

---

## Build Order

1. `.claude-plugin/plugin.json`
2. `commands/quill-init.md`
3. `commands/quill-write.md`
4. `commands/quill-revise.md`
5. `commands/quill-status.md`
6. `commands/quill-outline.md`
7. `commands/quill-threads.md`
8. `commands/quill-character.md`
9. `commands/quill-export.md`
10. `agents/quill-expert.md`
11. `skills/quill-context/SKILL.md`
12. `README.md`

## Definition of Done

- `/quill:init` wizard works for fiction, nonfiction, and technical book types
- `/quill:init` produces a complete auto-generated outline
- LaTeX and Markdown paths both work correctly
- `/quill:write N` writes chapter, self-summarizes, updates quill.json
- `/quill:write N+1` uses only compressed context (not raw prose)
- `/quill:revise N` updates chapter, re-summarizes, logs revision, warns of impact
- `/quill:status` shows accurate progress and flags issues
- `/quill:export` produces correct output for both format choices
- Quill context skill auto-activates when quill.json is present
- README complete
