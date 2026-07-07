---
description: Start a new Quill book project with a guided setup wizard. Collects all context needed to auto-generate a complete chapter outline. Run this once at the start of any new book.
argument-hint: (optional) working title
allowed-tools: Read, Write, Bash
---

Load the `quill` skill and execute the **Init Workflow** from its
`references/workflows.md`. Follow it exactly, including the six-phase
interview, the v2 `quill.json` schema, and the init templates.

If `$ARGUMENTS` is provided, use it as the working title and skip that
question in Phase 1. If a `quill.json` already exists, warn and wait for
explicit confirmation before overwriting anything.
