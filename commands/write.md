---
description: Write a specific chapter using compressed context. Automatically self-summarizes into .quill/summaries/ and updates quill.json after writing.
argument-hint: chapter number (e.g. 3)
allowed-tools: Read, Write, Bash
---

Load the `quill` skill and execute the **Write Workflow** from its
`references/workflows.md` for chapter `$ARGUMENTS`. Follow it exactly,
including the compression contract, self-summarization, and auto-compaction
from SKILL.md.

If no argument is provided, offer the next unwritten chapter after
`last_chapter_written`.
