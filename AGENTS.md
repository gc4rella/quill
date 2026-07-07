# AGENTS.md

Quill is a book-writing assistant distributed as a Claude Code plugin and a Codex skill. Keep both surfaces behaviorally aligned; see `README.md` for user-facing usage.

## Working style

- Make the smallest change that satisfies the request.
- Preserve existing slash-command names, skill activation behavior, project schema, and generated file layout unless the task explicitly changes them.
- Treat changes to the generated `quill.json` schema, chapter-summary storage, command names, or generated project layout as public contract changes; update every affected surface together.

## Repository map

- `commands/` — thin Claude Code slash-command adapters.
- `agents/` — Claude Code agent definitions.
- `skills/quill/` — canonical cross-platform behavior and Codex skill metadata.
- `skills/quill/references/workflows.md` — authoritative workflow implementations.
- `skills/quill/references/schema.md` — canonical `quill.json` and chapter-summary schemas.
- `skills/quill/templates/` — Python helpers copied into initialized book projects.
- `tests/` — pytest coverage for the bundled Python helpers.
- `.claude-plugin/plugin.json` — Claude Code plugin metadata.

## Setup and commands

- Install the test dependency: `pip install pytest`
- Run the full test suite: `python -m pytest -q`
- Run one test module: `python -m pytest -q tests/test_validate.py`

There is no repository build step or local development server.

## Implementation rules

- Keep `commands/*.md` as thin adapters that load the `quill` skill and route to the matching canonical workflow; do not duplicate workflow logic there.
- Put shared operational behavior in `skills/quill/references/workflows.md`, and keep `skills/quill/SKILL.md` focused on routing and cross-workflow contracts.
- When changing schema fields, update `schema.md`, migration and validation behavior in `quill-validate.py`, affected workflows, README examples, and tests in the same change.
- Keep Claude Code command frontmatter and skill frontmatter valid Markdown/YAML.
- Preserve the compression contract: do not introduce workflows that load full chapters without the explicit exceptions documented by the skill.
- Keep format switching independent from optional export tools such as Pandoc or LaTeX engines.
- Add or update regression tests for changes to scripts under `skills/quill/templates/`.

## Safety and repository hygiene

- NEVER commit credentials, tokens, private keys, `.env` files, generated book manuscripts, or local assistant state.
- Do not edit files under `.worktrees/`; they are separate working trees and are ignored by this repository.
- Do not reintroduce stale planning documents as behavioral authority. Current code, tests, skill references, and CI take precedence.

## Verification and definition of done

Before marking work complete, `python -m pytest -q` must pass.

Work is done only when:

- Claude Code and Codex behavior remain aligned for the changed workflow.
- Public behavior changes are reflected in `README.md` and relevant command or skill references.
- Script behavior changes have regression coverage.
