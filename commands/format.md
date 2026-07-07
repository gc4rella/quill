---
description: View or switch the output format (LaTeX or Markdown) for the current book project.
argument-hint: (optional) "latex" or "markdown"
allowed-tools: Read, Write, Bash
---

Load the `quill` skill and execute the **Format Workflow** from its
`references/workflows.md` with target `$ARGUMENTS`. Conversion is a
deterministic in-repo pass per `references/format-conversion.md`; wait for
explicit confirmation before converting, and never check for `pandoc` or
`pdflatex` during a format switch.
