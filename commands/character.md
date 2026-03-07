---
description: Add or update a character (fiction) or key concept (technical/nonfiction) in quill.json.
argument-hint: name
allowed-tools: Read, Write
---

# Quill Character / Concept

You are managing characters (fiction) or key concepts (technical/nonfiction) for a Quill book project.

Read `quill.json` first. If it doesn't exist, tell the user to run `/quill:init` first and stop.

Check `book_type` to determine which mode to operate in.

---

## Fiction mode (book_type = "fiction")

### If no argument: List all characters

Display all entries from `characters`:

```
Characters (N total)

  Name — role
    "One-line description"
    Arc: where they start → where they end
    Last seen: Ch N, brief note
    Relationships: list
```

After listing:
> "To add or update a character, run `/quill:character Name`."

### With name argument: Add or update character

**If the character exists in `quill.json.characters`:**

Show the current entry and ask:
> "What would you like to update? You can change the description, arc, role, relationships, or any other field."

Apply changes to `quill.json`.

Also check if a detailed character sheet exists at `characters/{name}.md` (lowercase, hyphens for spaces). If it exists, offer to update it. If not, offer to create one.

**If the character does NOT exist:**

Ask for:
1. **Role** — protagonist, antagonist, supporting, mentor, or other
2. **Description** — one-line description
3. **Arc** — where they start and where they end (can be brief or "TBD")
4. **Relationships** — key relationships to other characters (can be empty)

Add to `quill.json.characters`:

```json
{
  "role": "supporting",
  "description": "one-line description",
  "arc": "starts as X, ends as Y",
  "relationships": ["relationship strings"],
  "last_seen": ""
}
```

Then create a detailed character sheet at `characters/{name}.md`:

```markdown
# Character Name

**Role:** supporting
**First appearance:** TBD

## Description
Detailed physical and personality description.

## Background
Key backstory relevant to the narrative.

## Arc
Where they start → where they end.

## Relationships
- Character A: relationship description

## Notes
Any other relevant details for maintaining consistency.
```

Ask the author to fill in or approve the details. Save both `quill.json` and the character sheet.

---

## Nonfiction / Technical mode (book_type = "nonfiction" or "technical")

### If no argument: List all concepts

Display all entries from `concepts`:

```
Key Concepts (N total)

  ConceptName
    "One-line definition"
    Introduced in: Ch N
    Depends on: [list of prerequisites]
```

After listing:
> "To add or update a concept, run `/quill:character ConceptName`."

### With name argument: Add or update concept

**If the concept exists in `quill.json.concepts`:**

Show the current entry and ask:
> "What would you like to update? You can change the definition, dependencies, or introduction chapter."

Apply changes to `quill.json`.

Also check if a detailed concept sheet exists at `concepts/{name}.md` (lowercase, hyphens for spaces). If it exists, offer to update it. If not, offer to create one.

**If the concept does NOT exist:**

Ask for:
1. **Definition** — one-line definition
2. **Introduced in chapter** — which chapter introduces this concept (can be "TBD")
3. **Depends on** — what concepts must the reader understand first (can be empty)

Add to `quill.json.concepts`:

```json
{
  "definition": "one-line definition",
  "introduced_in_chapter": 3,
  "depends_on": ["other concept names"]
}
```

Then create a detailed concept sheet at `concepts/{name}.md`:

```markdown
# Concept Name

**Definition:** One-line definition.
**Introduced in:** Chapter N
**Prerequisites:** list of concepts

## Explanation
Fuller explanation of the concept for reference while writing.

## Key Points
- Point 1
- Point 2

## Common Misconceptions
Things readers often get wrong about this concept.

## Related Concepts
- Related concept: how it connects

## Notes
Any other relevant details for maintaining consistency across chapters.
```

Ask the author to fill in or approve the details. Save both `quill.json` and the concept sheet.
