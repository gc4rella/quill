# Quill Schema Reference

Canonical definition of the `quill.json` v2 schema, per-chapter summary files, validation rules, and migration.

---

## quill.json (v2)

```json
{
  "schema_version": 2,
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
  "open_threads": [],
  "resolved_threads": [],
  "last_chapter_written": 0,
  "revision_log": []
}
```

### Field notes

- `schema_version` — must be `2`. Absence indicates a v1 project that needs migration.
- `format` — `"latex"` or `"markdown"`. Controls file extensions and export behavior.
- `outline` — array of chapter entries; see outline entry shape below.
- `open_threads` / `resolved_threads` — each item must have a unique `id` string; the two sets must be disjoint.
- `last_chapter_written` — the highest chapter number written so far (not the most recently touched).
- `world_rules` — deduped; if two entries express the same fact, merge them.
- `continuity_flags` — capped at 20; flags consistent for 10+ chapters can be removed.
- `revision_log` — capped at 10 entries (oldest dropped).
- `resolved_threads` — capped at 10 entries (oldest dropped).

**Removed from v1:** `chapter_summaries`, `last_chapter_ending`. These live in per-chapter summary files instead.

### Outline entry shape

```json
{
  "chapter": 1,
  "part": null,
  "title": "Chapter Title",
  "brief": "2-4 sentence plan.",
  "purpose": "Structural role of the chapter.",
  "target_words": 4000,
  "status": "planned"
}
```

Valid `status` values: `"planned"`, `"written"`, `"revised"`, `"needs-revision"`.

### Character entry shape (fiction)

```json
{
  "role": "protagonist",
  "description": "",
  "arc": "",
  "relationships": {},
  "last_seen": 0
}
```

### Concept entry shape (nonfiction / technical)

```json
{
  "definition": "",
  "dependencies": [],
  "introduced_in_chapter": 1
}
```

### Thread entry shape

```json
{
  "id": "slug",
  "description": "",
  "type": "plot",
  "opened_in_chapter": 1
}
```

Resolved threads additionally carry: `"resolved_in_chapter"` and `"resolution"`.

---

## Per-Chapter Summary File — `.quill/summaries/ch-NN.json`

One file per written chapter. Created or updated by the Write and Revise workflows.

```json
{
  "chapter": 5,
  "what_happened_or_covered": "2-3 sentence summary",
  "emotional_beat_or_takeaway": "key beat",
  "new_characters_or_concepts": [],
  "new_world_facts": [],
  "threads_or_questions_opened": [],
  "threads_or_questions_closed": [],
  "actual_word_count": 3800,
  "ending_excerpt": "final ~150 words verbatim"
}
```

- `ending_excerpt` — the final ~150 words of the chapter's prose, verbatim. Used for prose continuity when writing the successor chapter. Hard cap at 150 words.
- `what_happened_or_covered` — max 3 sentences; condense immediately if longer.
- `.quill/` must be **committed** with the book project (do not gitignore it).

---

## Validation Rules

`quill-validate.py` (and any LLM performing validation by hand) checks:

1. `schema_version` equals `2`. If absent or wrong, run `--migrate`.
2. `format` is `"latex"` or `"markdown"`.
3. Every outline entry with `status` in `{"written", "revised", "needs-revision"}` must have:
   - A chapter file: `chapters/ch-NN.tex` or `chapters/ch-NN.md` (extension from `format`).
   - A summary file: `.quill/summaries/ch-NN.json`.
4. Every summary file `ch-NN.json` must correspond to an outline entry for chapter `N`.
5. `open_threads` IDs are unique (no duplicates within the array).
6. No ID appears in both `open_threads` and `resolved_threads`.

---

## Schema Version & Migration

**v2** (current) introduced per-chapter summary files and removed `chapter_summaries` / `last_chapter_ending` from `quill.json`.

To migrate a v1 project:

```bash
python3 scripts/quill-validate.py --migrate
```

The script:
- Moves each `chapter_summaries[N]` entry to `.quill/summaries/ch-NN.json`.
- Sets `ending_excerpt` from the old `last_chapter_ending` for the last written chapter; other chapters get `ending_excerpt: ""`.
- Sets `schema_version: 2` and removes `chapter_summaries` and `last_chapter_ending`.
- Is idempotent: running it on a v2 project is a no-op.

If shell execution is unavailable, perform the migration by hand following these same steps. On first action in any project that lacks `schema_version`, migrate before proceeding.
