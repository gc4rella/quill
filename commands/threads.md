---
description: View all open plot threads or concept questions. For fiction: unresolved narrative threads. For technical books: concepts introduced but not yet fully resolved or applied.
argument-hint: (optional) thread ID to resolve
allowed-tools: Read, Write
---

# Quill Threads

You are managing open threads for a Quill book project. Threads track unresolved narrative questions (fiction), open concepts or unanswered questions (nonfiction/technical), and anything the author wants to remember to address later.

Read `quill.json` first. If it doesn't exist, tell the user to run `/quill:init` first and stop.

---

## No argument: List all open threads

Display all entries from `open_threads`:

```
Open Threads (N total)

  [thread-id]  "Description"
               Type: plot | character | concept | question
               Opened in: Ch N

  [thread-id]  "Description"
               Type: plot
               Opened in: Ch 2  ⚠️ STALE — open for 8 chapters
...
```

**Staleness warning**: If `last_chapter_written - opened_in_chapter >= 5`, flag it as stale. Stale threads may be forgotten plot holes or concepts that need resolution.

After listing, show options:

> "To resolve a thread, run `/quill:threads thread-id`. To add a new thread manually, say 'add' and describe it."

### If user says "add":

Ask for:
1. **ID** — a short slug (e.g., `missing-letter`, `ownership-model`)
2. **Description** — what the thread is about
3. **Type** — plot, character, concept, or question
4. **Opened in chapter** — which chapter introduced it (default: `last_chapter_written`)

Add to `open_threads` in `quill.json` and confirm.

---

## With thread ID argument: Resolve a thread

Look up the thread ID in `open_threads`. If not found, tell the user and list available thread IDs.

If found, show the thread details and ask:

> "How was this resolved? Which chapter resolves it?"

Then:

1. Remove the thread from `open_threads`
2. Add it to `resolved_threads` with additional fields:

```json
{
  "id": "thread-id",
  "description": "original description",
  "opened_in_chapter": 2,
  "type": "plot",
  "resolved_in_chapter": 8,
  "resolution": "Brief note on how it was resolved"
}
```

3. Save `quill.json`
4. Confirm:

> "Thread [thread-id] resolved in Chapter N. Use `/quill:threads` to see remaining open threads."

---

## Also show resolved threads summary

At the bottom of the thread list (no-argument mode), show a count:

> "N threads resolved so far. To see resolved threads, say 'show resolved'."

If the user asks to see resolved threads, display them:

```
Resolved Threads (N total)

  [thread-id]  "Description"
               Opened in Ch 2 → Resolved in Ch 8
               Resolution: "Brief note"
...
```
