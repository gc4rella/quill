---
description: Start a new Quill book project with a guided setup wizard. Collects all context needed to auto-generate a complete chapter outline. Run this once at the start of any new book.
argument-hint: (optional) working title
allowed-tools: Read, Write
---

# Quill Init Wizard

You are starting a new Quill book project. Run a structured interview in 6 phases, then auto-generate a complete chapter outline. Be conversational but efficient — ask all questions in a phase together, then move on.

**Important:** If a `quill.json` already exists, warn the user and ask for explicit confirmation before overwriting. Never destroy existing work silently.

If an argument was provided, use it as the working title and skip that question in Phase 1.

---

## Phase 1 — Foundation (all book types)

Ask these questions together:

1. **Working title** — What's the working title? (Skip if provided as argument.)
2. **Book type** — Is this fiction, nonfiction, or technical?
3. **Premise** — Summarize the book in 1-2 sentences. What is it about?
4. **Target reader** — Who is this for? Be specific (e.g., "adult literary fiction readers", "junior JavaScript developers", "history buffs interested in WWII Pacific theater").
5. **Target length** — How long should this be?
   - Short: ~40,000 words / ~10 chapters
   - Standard: ~80,000 words / ~20 chapters
   - Long: ~120,000 words / ~30 chapters
   - Custom: specify word count and chapter count

Wait for answers before proceeding.

---

## Phase 2 — Book-Type-Specific Questions

Based on the book type from Phase 1, ask the appropriate branch:

### If Fiction:

Ask these together:

1. **Genre** — What genre? (e.g., literary fiction, sci-fi, fantasy, thriller, romance, horror, mystery, historical fiction, etc.)
2. **Central conflict** — What is the central conflict or dramatic question?
3. **Narrative structure** — Which structure fits best?
   - Three-act (setup → confrontation → resolution)
   - Save the Cat (15 beats)
   - Hero's Journey (12 stages)
   - Five-act (Shakespearean)
   - Nonlinear / experimental
   - Other (describe)
4. **Protagonist** — Who is the protagonist? Name, brief description, what they want, what's in their way.
5. **Antagonist** — Who or what is the antagonist? (Can be a person, institution, nature, internal conflict, etc.)
6. **Setting** — Where and when does this take place?
7. **POV and tense** — What point of view and tense? (e.g., first person past, third person limited present, omniscient, alternating POV)
8. **Tone** — Describe the tone. (e.g., dark and gritty, whimsical, literary and introspective, fast-paced and commercial)
9. **Style influences** — Name 1-3 authors or books whose style is closest to what you want. Or paste a paragraph of your own writing as a sample.

### If Nonfiction:

Ask these together:

1. **Thesis** — What is your central argument or thesis?
2. **Reader's problem** — What problem does the reader have that this book solves?
3. **Structure preference** — How should this be organized?
   - Chronological narrative
   - Thematic (topic-by-topic)
   - Problem → solution
   - Case-study driven
   - Other (describe)
4. **Tone** — Describe the tone. (e.g., conversational, academic, journalistic, personal essay, authoritative)
5. **Narrator presence** — How present is the author? (First person with anecdotes, third person objective, mixed)
6. **Style influences** — Name 1-3 authors or books whose style is closest. Or paste a sample paragraph.

### If Technical:

Ask these together:

1. **Technology/domain** — What technology, language, or domain does this cover?
2. **Prerequisites** — What should the reader already know?
3. **Reader goal** — After reading this book, the reader will be able to _____.
4. **Tutorial style** — How should concepts be introduced?
   - Bottom-up (fundamentals first, build complexity)
   - Top-down (show the big picture, drill into details)
   - Project-based (build something real, explain as you go)
   - Reference (organized for lookup, not linear reading)
5. **Code language(s)** — What programming language(s) for code examples? (If applicable.)
6. **Tone** — Describe the tone. (e.g., friendly and casual, precise and academic, opinionated, dry humor)
7. **Style influences** — Name 1-3 technical books whose style you admire. Or paste a sample paragraph.

Wait for answers before proceeding.

---

## Phase 3 — Output Format

Ask:

**Format** — Do you want LaTeX or Markdown output?

- **LaTeX**: Chapters saved as `.tex` files. Best if you want PDF output with professional typesetting. Requires a LaTeX installation (e.g., TeX Live) for PDF compilation.
- **Markdown**: Chapters saved as `.md` files. Can export to HTML, DOCX, or other formats via pandoc. Simpler toolchain.

### If LaTeX is chosen, follow up with:

1. **Document class** — Which document class? (Default: `book`. Options: `book`, `memoir`, `report`, or custom.)
2. **Paper size** — Letter or A4? (Default: letter.)
3. **Font size** — 10pt, 11pt, or 12pt? (Default: 11pt.)
4. **Any special LaTeX packages** you want in the preamble? (Default: sensible set including `hyperref`, `geometry`, `fontenc`, `inputenc`.)

Wait for answers before proceeding.

---

## Phase 4 — Style Fingerprint Derivation

Based on the style influences and tone from Phase 2, derive a **style fingerprint** — a dense, one-line voice description that will guide all chapter writing.

**How to derive it:**

1. If the user named author influences, synthesize their key stylistic traits (sentence length, vocabulary level, rhythm, use of metaphor, dialogue style, paragraph structure).
2. If the user pasted a writing sample, analyze it for the same traits.
3. Combine with the stated tone to produce a single line like:

   > "Terse declarative sentences, Anglo-Saxon vocabulary, minimal adjectives, Hemingway-meets-McCarthy with dry wit in dialogue"

   or

   > "Flowing literary prose, rich sensory metaphor, complex nested sentences, Donna Tartt pacing with Zadie Smith humor"

   or (technical)

   > "Clear and direct, short paragraphs, code-first explanations, conversational asides, Rust Book meets Pragmatic Programmer"

**Present the fingerprint to the author and ask for approval.** Adjust if they want changes. This fingerprint will be stored in `quill.json` and used as the voice guide for every chapter.

---

## Phase 5 — Project File Creation

Now create the project structure:

### 1. Create `quill.json`

Build the complete quill.json from all collected answers. Use this schema:

```json
{
  "title": "<from Phase 1>",
  "subtitle": "",
  "book_type": "<fiction | nonfiction | technical>",
  "genre": "<from Phase 2>",
  "target_audience": "<from Phase 1>",
  "format": "<latex | markdown>",
  "structure": {
    "model": "<from Phase 2 structure choice>",
    "target_word_count": "<calculated>",
    "chapter_count": "<calculated>",
    "words_per_chapter": "<calculated>",
    "has_parts": false,
    "parts": []
  },
  "premise": "<from Phase 1>",
  "central_conflict_or_thesis": "<from Phase 2>",
  "tone": "<from Phase 2>",
  "pov": "<from Phase 2, or empty for nonfiction>",
  "style_fingerprint": "<from Phase 4>",
  "setting": "<from Phase 2, or empty for nonfiction/technical>",
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

Fill in all fields from the collected answers. Leave `outline` empty for now — Phase 6 will populate it. Set `characters` with any protagonist/antagonist from Phase 2 fiction answers. Set `concepts` empty for now.

### 2. Create directories

- `chapters/` — where chapter files will be saved
- `export/` — where assembled manuscripts will go

For fiction: also create `characters/` directory.
For technical/nonfiction: also create `concepts/` directory.

### 3. If LaTeX format: create `book.tex`

Create a `book.tex` file with:
- Document class and options from Phase 3
- Standard preamble packages
- `\title{}`, `\author{}`, `\date{}`
- `\begin{document}`, `\maketitle`, `\tableofcontents`
- Comment placeholder: `% Chapter \input{} lines will be added by /quill:export`
- `\end{document}`

### 4. If Markdown format: create no additional files

Markdown projects don't need a wrapper file — `/quill:export` will concatenate chapters directly.

---

## Phase 6 — Auto-Generate Outline

Generate a complete chapter-by-chapter outline based on everything collected. This is the payoff of the deep init.

### Requirements by book type:

**Fiction:**
- Map chapters to the chosen narrative structure (e.g., three-act: which chapters are Act 1, inciting incident, midpoint, climax, resolution)
- Ensure protagonist arc progresses across chapters
- Place major plot turns at structurally appropriate points
- Distribute subplots and supporting character arcs
- Each chapter entry needs: number, part (if applicable), title, 2-4 sentence brief, structural purpose, target word count

**Nonfiction:**
- Follow the chosen organizational structure
- Ensure logical progression from foundational to complex ideas
- Each chapter builds on previous knowledge
- Include introduction and conclusion chapters
- Each chapter entry needs: number, part (if applicable), title, 2-4 sentence brief, purpose, target word count

**Technical:**
- Follow the tutorial style (bottom-up, top-down, project-based, reference)
- Map prerequisite concepts → dependent concepts across chapters
- Ensure code examples build progressively
- Include setup/intro chapter and wrap-up/next-steps chapter
- Each chapter entry needs: number, part (if applicable), title, 2-4 sentence brief, purpose, target word count, key concepts introduced

### Outline entry format:

```json
{
  "chapter": 1,
  "part": null,
  "title": "Chapter Title",
  "brief": "2-4 sentence plan for this chapter.",
  "purpose": "Structural role (e.g., 'Inciting incident', 'Introduce core concept', 'Rising action')",
  "target_words": 4000,
  "status": "planned"
}
```

### After generating:

1. Present the full outline to the author in a readable format (numbered list with titles and briefs).
2. Ask: "Does this outline work? You can adjust any chapter, add chapters, remove chapters, or restructure before we lock it in. You can also change the outline later with `/quill:outline`."
3. Apply any requested changes.
4. Save the final outline to `quill.json`.

### Final message:

After saving, tell the author:
- How many chapters are planned
- Total target word count
- Suggested first command: `/quill:write 1` to start writing Chapter 1
- Mention `/quill:outline` to view or adjust the outline later
- Mention `/quill:status` for a bird's-eye view at any time
