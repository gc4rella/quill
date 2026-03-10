---
description: Write a specific chapter using compressed context from quill.json. Automatically self-summarizes and updates quill.json after writing.
argument-hint: chapter number (e.g. 3)
allowed-tools: Read, Write
---

# Quill Write

You are writing a chapter for a Quill book project. Follow these 8 steps exactly.

**The argument is the chapter number to write.** If no argument is provided, check `quill.json` for `last_chapter_written` and offer to write the next chapter.

---

## Step 1: Read quill.json

Read `quill.json` from the project root. If it doesn't exist, tell the user to run `/quill:init` first and stop.

---

## Step 2: Find the outline entry

Look up the requested chapter number in the `outline` array. If no entry exists for this chapter number, tell the user:

> "Chapter N isn't in the outline yet. Use `/quill:outline N` to add it first, or give me a brief and I'll add it now."

Stop if no outline entry and the user doesn't provide one.

---

## Step 3: Check for existing chapter file

Determine the file path based on format:
- LaTeX: `chapters/ch-{NN}.tex` (zero-padded, e.g., `ch-01.tex`)
- Markdown: `chapters/ch-{NN}.md`

If the file already exists, inspect it before warning the user.

If it still matches the Quill stub placeholder, treat it as a placeholder and overwrite it without asking:

- Markdown stub marker: `<!-- quill:chapter-stub -->`
- LaTeX stub marker: `% quill:chapter-stub`

If it contains drafted prose, warn the user:

> "Chapter N already exists at `chapters/ch-NN.{ext}`. Overwrite it? If you want to revise instead, use `/quill:revise N`."

Stop and wait for confirmation before overwriting.

---

## Step 4: Build the briefing

Construct a compressed briefing **under 1500 tokens**. Include only:

1. **Title** — book title
2. **Genre/type** — genre or book type
3. **POV/tense** — point of view and tense
4. **Style fingerprint** — the voice guide (verbatim from quill.json)
5. **Setting** — overall setting
6. **Tone** — tone description
7. **Active characters or concepts** — from `chapter_summaries` of the 3 nearest prior written chapters by chapter number (not all characters, and never from later chapters unless the author asks)
8. **Continuity flags** — from `continuity_flags` array
9. **Open threads** — currently open threads relevant to this chapter
10. **This chapter's outline** — the `brief` and `purpose` from the outline entry
11. **Last chapter ending** — use the `last_chapter_ending` field only when it belongs to the immediate predecessor; otherwise rely on the previous chapter summary and, if needed, read only that chapter's closing passage
12. **Target word count** — from the outline entry's `target_words`

**Do NOT load any full chapter files.** The briefing is your only context. This is the compression contract — it's what makes Quill work for long books.

---

## Step 5: Write the chapter

Using the briefing as your guide, write the full chapter.

**Format-aware writing:**

- **LaTeX**: Start with `\chapter{Chapter Title}` and write in LaTeX. Save to `chapters/ch-{NN}.tex`. Do not include `\documentclass` or `\begin{document}` — this file will be `\input{}` into `book.tex`.
- **Markdown**: Write in plain Markdown. Do NOT start with a heading — the chapter title will be added during export. Save to `chapters/ch-{NN}.md`.

**Writing guidelines:**
- Match the `style_fingerprint` exactly — this is the voice
- Honor the `tone`
- Continue naturally from the strongest available handoff: `last_chapter_ending` when it belongs to the immediate predecessor, otherwise the previous chapter summary plus a short closing excerpt if needed
- Fulfill the outline's `brief` and `purpose`
- Hit the target word count (±10% is fine)
- Introduce any new characters, concepts, or plot threads organically
- End with a hook or natural pause point that makes the reader want to continue

---

## Step 6: Self-summarize

After writing, analyze the chapter and extract:

```json
{
  "what_happened_or_covered": "2-3 sentence summary",
  "emotional_beat_or_takeaway": "the key emotional or intellectual beat",
  "new_characters_or_concepts": ["list of new introductions"],
  "new_world_facts": ["any new world-building facts or rules established"],
  "threads_or_questions_opened": ["new threads or questions raised"],
  "threads_or_questions_closed": ["threads resolved in this chapter"],
  "actual_word_count": 3800
}
```

---

## Step 7: Update quill.json

Update `quill.json` with:

1. **chapter_summaries** — add the summary from Step 6 under the chapter number key
2. **characters** — add or update any characters introduced or developed (update `last_seen`)
3. **concepts** — add any new concepts introduced (technical/nonfiction)
4. **world_rules** — append any new world rules or facts established
5. **open_threads** — add new threads opened; remove threads closed (move to `resolved_threads`)
6. **resolved_threads** — add any threads resolved, with resolution note and chapter
7. **last_chapter_written** — set to this chapter number (only if higher than current value)
8. **last_chapter_ending** — set to the final ~150 words of this chapter (verbatim)
9. **outline status** — update this chapter's outline entry status from `"planned"` to `"written"`

---

## Step 8: Report

Tell the author:

- **Word count**: actual vs. target (e.g., "3,800 words written — target was 4,000 ✓")
- **New threads opened**: list any new plot threads or questions raised
- **Threads closed**: list any resolved
- **New characters/concepts**: list any introduced
- **Suggested next**: `/quill:write {N+1}` to continue, `/quill:status` for overview, or `/quill:revise {N}` to revise this chapter
