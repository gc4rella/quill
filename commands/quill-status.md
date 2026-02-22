---
description: Show the full status of the book — chapters written, word count progress, open threads, and any chapters that may need revision due to earlier changes.
allowed-tools: Read
---

# Quill Status

You are showing the bird's-eye view of a Quill book project. Read `quill.json` and present a comprehensive status report.

If `quill.json` doesn't exist, tell the user to run `/quill:init` first and stop.

---

## Section 1: Book Overview

Display:

- **Title**: from `title`
- **Type**: from `book_type`
- **Format**: from `format` (LaTeX or Markdown)
- **Structure**: from `structure.model`
- **Target word count**: from `structure.target_word_count`
- **Chapters**: written / planned (e.g., "7 / 20 chapters")
- **Words written**: sum of all `chapter_summaries[*].actual_word_count` / `structure.target_word_count` (e.g., "28,400 / 80,000 words (36%)")
- **Estimated completion**: based on current pace — chapters remaining × average words per chapter written so far

---

## Section 2: Chapter Map

Show one line per chapter from the outline. Use status indicators:

- ✅ `written` — chapter is complete
- ✏️ `revised` — chapter has been revised
- ⚠️ `needs-revision` — chapter may need revision due to earlier changes
- 📋 `planned` — not yet written

Format:

```
Ch  1  ✅  "The Opening"           3,800 words
Ch  2  ✅  "Rising Tension"        4,200 words
Ch  3  ✏️  "The Turning Point"     3,950 words (revised)
Ch  4  ⚠️  "Consequences"          4,100 words (needs revision — Ch 3 revised)
Ch  5  📋  "The Descent"           — planned —
...
```

If the book has parts, group chapters under part headings.

---

## Section 3: Open Threads

List all entries from `open_threads`:

```
• [thread-id] "Description" — opened in Ch N
```

**Flag stale threads**: If a thread has been open for 5+ chapters beyond where it was opened (i.e., `last_chapter_written - opened_in_chapter >= 5`), flag it:

```
• [thread-id] "Description" — opened in Ch 2 ⚠️ STALE (open for 8 chapters)
```

If no open threads, say "No open threads."

---

## Section 4: Recent Revision Log

Show the last 3 entries from `revision_log`:

```
• Ch 3 revised after Ch 7 — "Strengthened protagonist motivation" (impact: Ch 4 may need revision)
```

If no revisions, say "No revisions yet."

---

## Section 5: Suggested Next Steps

Based on current state, suggest 1-3 actions:

- If there are `needs-revision` chapters: "Consider revising Chapter N with `/quill:revise N` — it was flagged after changes to Chapter M."
- If the next unwritten chapter exists: "Continue writing with `/quill:write N`."
- If there are stale threads: "Review stale threads with `/quill:threads` — some have been open for a while."
- If all chapters are written: "All chapters complete! Use `/quill:export` to assemble the manuscript."
- If outline is incomplete: "Some chapters don't have outline entries. Use `/quill:outline` to fill them in."
