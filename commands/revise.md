---
description: Revisit and revise a chapter that has already been written. Re-summarizes after revision and warns about continuity impact on later chapters.
argument-hint: chapter number (e.g. 3)
allowed-tools: Read, Write
---

# Quill Revise

You are revising an existing chapter in a Quill book project. Follow these 10 steps exactly.

**The argument is the chapter number to revise.** If no argument is provided, ask which chapter to revise.

---

## Step 1: Read quill.json

Read `quill.json` from the project root. If it doesn't exist, tell the user to run `/quill:init` first and stop.

---

## Step 2: Load the chapter file

Determine the file path based on format:
- LaTeX: `chapters/ch-{NN}.tex` (zero-padded)
- Markdown: `chapters/ch-{NN}.md`

Read the full chapter file. If it doesn't exist, tell the user:

> "Chapter N hasn't been written yet. Use `/quill:write N` to write it first."

Stop if the file doesn't exist.

---

## Step 3: Load existing chapter summary

Read `chapter_summaries[N]` from quill.json. This is the current summary of the chapter as it stands. You'll compare against this after revision to detect continuity impact.

---

## Step 4: Load previous chapter ending

If this is not chapter 1, read `last_chapter_ending` of chapter N-1 from the chapter summaries or, if N-1 is the most recently written chapter, from the `last_chapter_ending` field. This ensures the revised chapter still flows from the previous one.

---

## Step 5: Show revision options

Present these options to the author:

1. **Suggest revisions** — Read the chapter and suggest specific improvements without making changes. Let the author pick which suggestions to apply.
2. **Rewrite a section** — The author identifies a section (by quoting or describing it), and you rewrite just that part while preserving the rest.
3. **Full rewrite** — Rewrite the entire chapter from scratch using the same outline brief. The old version is replaced.
4. **Metadata-only update** — Don't change the chapter text. Just re-read it and update the summary, characters, threads, etc. in quill.json. Useful if you manually edited the chapter file.

Wait for the author's choice before proceeding.

---

## Step 6: Make changes and save

Based on the chosen option:

- **Suggest**: Present suggestions as a numbered list. For each, show the original text and proposed replacement. Ask which to apply. Apply selected changes and save.
- **Rewrite section**: Ask the author to identify the section. Rewrite it in the same style (match `style_fingerprint`). Show the rewrite for approval. Save when approved.
- **Full rewrite**: Rebuild the briefing (same as `/quill:write` Step 4), rewrite the full chapter. Show to author for approval. Save when approved.
- **Metadata-only**: Skip to Step 7.

Save the updated chapter to the same file path.

---

## Step 7: Re-summarize

Analyze the revised chapter and produce a new summary with all fields:

```json
{
  "what_happened_or_covered": "2-3 sentence summary",
  "emotional_beat_or_takeaway": "the key emotional or intellectual beat",
  "new_characters_or_concepts": ["list"],
  "new_world_facts": ["list"],
  "threads_or_questions_opened": ["list"],
  "threads_or_questions_closed": ["list"],
  "actual_word_count": 3800
}
```

---

## Step 8: Detect continuity impact

Compare the OLD summary (from Step 3) with the NEW summary (from Step 7). Flag changes in:

- **Characters**: Any characters added, removed, or significantly changed?
- **World facts**: Any world rules or facts altered?
- **Threads**: Any threads opened or closed differently than before?
- **Chapter ending**: Did the ending change? If so, the next chapter's opening may no longer flow correctly.

For each detected impact, determine which later chapters (those with `status: "written"` and chapter number > N) might be affected.

---

## Step 9: Update quill.json

1. **chapter_summaries[N]** — replace with new summary
2. **last_chapter_ending** — if this is the last written chapter, update the ending. If not, only update if the ending changed and note it in continuity impact.
3. **characters** — update any changed character entries
4. **concepts** — update any changed concept entries
5. **world_rules** — update if world facts changed
6. **open_threads** — update if threads changed
7. **resolved_threads** — update if thread resolutions changed
8. **outline status** — set this chapter's status to `"revised"`
9. **revision_log** — append a new entry:

```json
{
  "chapter": N,
  "revised_at": "after chapter M",
  "reason": "<brief reason for revision>",
  "continuity_impact": "<summary of what changed that affects later chapters, or 'none'>"
}
```

Where M = `last_chapter_written` at the time of revision.

If continuity impact was detected, set affected later chapters' outline status to `"needs-revision"`.

---

## Step 10: Report

Tell the author:

- **What changed**: Brief description of the revision
- **Summary diff**: Key differences between old and new summary (what was added, removed, or changed)
- **Continuity warnings**: If later chapters are affected, list them with specific concerns:
  > "⚠️ Chapter 5 may need revision: the ending of Chapter 3 changed significantly, and Chapter 5's opening references events that were altered."
- **Word count**: new word count vs. target
- **Suggested next**: If chapters were flagged as `needs-revision`, suggest `/quill:revise` for those. Otherwise suggest `/quill:status` for overview.
