---
description: Assemble all written chapters into a final manuscript. Produces PDF (LaTeX) or a single document (Markdown).
argument-hint: (optional) "pdf" to compile LaTeX to PDF, "docx" or "html" for markdown
allowed-tools: Read, Write, Bash
---

Load the `quill` skill and execute the **Export Workflow** from its
`references/workflows.md` with target `$ARGUMENTS`. External tool checks
(`pdflatex`, `pandoc`) belong here, not in format switching.
