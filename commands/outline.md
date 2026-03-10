---
description: View the full chapter outline or add and update individual chapter entries.
argument-hint: (optional) chapter number and title
allowed-tools: Read, Write
---

# Quill Outline

You are viewing or editing the chapter outline for a Quill book project.

Read `quill.json` first. If it doesn't exist, tell the user to run `/quill:init` first and stop.

---

## No argument: Display full outline

Show the complete outline in a readable table format:

```
# Outline: "Book Title"
Structure: three-act | 20 chapters | 80,000 words target

Part 1: "Part Title" (if has_parts)

  Ch  1  📋  "Chapter Title"
             Brief: 2-4 sentence plan...
             Purpose: structural role
             Target: 4,000 words

  Ch  2  ✅  "Chapter Title"
             Brief: 2-4 sentence plan...
             Purpose: structural role
             Target: 4,000 words | Actual: 3,800 words
...
```

Use the same status indicators as `/quill:status`:
- ✅ written
- ✏️ revised
- ⚠️ needs-revision
- 📋 planned

After displaying, remind the user:
> "To edit a chapter entry, run `/quill:outline N`. To add a new chapter, run `/quill:outline N New Title`."

---

## With chapter number argument: View or edit a single chapter

### If the chapter exists in the outline:

Show the full entry, then ask:

> "What would you like to update? You can change the title, brief, purpose, target word count, or part assignment. Or say 'delete' to remove this chapter from the outline."

Apply the requested changes and save to `quill.json`.

If the matching chapter file is still a Quill stub, refresh it after saving. If `scripts/quill-sync-outline.py` exists, use it when shell execution is available; otherwise recreate the same stub content directly. Never overwrite a non-stub chapter file.

If the chapter has already been written (`status: "written"` or `"revised"`), warn:

> "This chapter has already been written. Changing the outline entry won't change the chapter text — use `/quill:revise N` to revise the actual chapter."

### If the chapter does NOT exist in the outline:

Ask for the details:

1. **Title** — What's the chapter title?
2. **Brief** — 2-4 sentence plan for this chapter.
3. **Purpose** — What structural role does this chapter serve?
4. **Target words** — Target word count (default: `structure.words_per_chapter`)
5. **Part** — Which part does it belong to? (Only ask if `structure.has_parts` is true.)

Create the new outline entry with `status: "planned"` and save to `quill.json`.

If the new chapter number is beyond the current `structure.chapter_count`, update `chapter_count` and recalculate `target_word_count` accordingly.

After saving, create or refresh the matching chapter stub file. If `scripts/quill-sync-outline.py` exists, use it when shell execution is available; otherwise recreate the same stub content directly. Never overwrite a non-stub chapter file.

After saving, confirm:

> "Chapter N added to the outline and the chapter stub is ready. Use `/quill:write N` when you're ready to write it."
