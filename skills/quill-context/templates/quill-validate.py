#!/usr/bin/env python3
"""Validate a Quill project and migrate v1 quill.json to the v2 layout."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = 2

SUMMARY_FIELDS = (
    "what_happened_or_covered",
    "emotional_beat_or_takeaway",
    "new_characters_or_concepts",
    "new_world_facts",
    "threads_or_questions_opened",
    "threads_or_questions_closed",
    "actual_word_count",
)


def load_quill(project_root: Path) -> dict:
    path = project_root / "quill.json"
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_quill(project_root: Path, quill: dict) -> None:
    (project_root / "quill.json").write_text(
        json.dumps(quill, indent=2) + "\n", encoding="utf-8"
    )


def summaries_dir(project_root: Path) -> Path:
    return project_root / ".quill" / "summaries"


def migrate(project_root: Path) -> bool:
    """Return True if a migration was performed, False if already v2."""
    quill = load_quill(project_root)
    if quill.get("schema_version") == SCHEMA_VERSION:
        return False

    sdir = summaries_dir(project_root)
    sdir.mkdir(parents=True, exist_ok=True)

    last_written = int(quill.get("last_chapter_written") or 0)
    last_ending = quill.get("last_chapter_ending", "")
    summaries = quill.get("chapter_summaries") or {}

    for key, summary in summaries.items():
        n = int(key)
        out = {"chapter": n}
        for field in SUMMARY_FIELDS:
            if field in summary:
                out[field] = summary[field]
        out["ending_excerpt"] = last_ending if n == last_written else ""
        (sdir / f"ch-{n:02d}.json").write_text(
            json.dumps(out, indent=2) + "\n", encoding="utf-8"
        )

    quill.pop("chapter_summaries", None)
    quill.pop("last_chapter_ending", None)
    quill["schema_version"] = SCHEMA_VERSION
    write_quill(project_root, quill)
    return True


def validate(project_root: Path) -> list[str]:
    """Return a list of error strings. Empty list means valid."""
    errors: list[str] = []
    quill = load_quill(project_root)

    if quill.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version is {quill.get('schema_version')!r}, expected {SCHEMA_VERSION}; run --migrate"
        )

    fmt = quill.get("format")
    if fmt not in {"latex", "markdown"}:
        errors.append(f"format must be 'latex' or 'markdown', got {fmt!r}")
    ext = "tex" if fmt == "latex" else "md"

    outline = quill.get("outline") or []
    sdir = summaries_dir(project_root)
    for entry in outline:
        n = int(entry["chapter"])
        status = entry.get("status", "planned")
        if status in {"written", "revised", "needs-revision"}:
            chap = project_root / "chapters" / f"ch-{n:02d}.{ext}"
            if not chap.exists():
                errors.append(f"chapter {n} is '{status}' but {chap} is missing")
            summ = sdir / f"ch-{n:02d}.json"
            if not summ.exists():
                errors.append(f"chapter {n} is '{status}' but {summ} is missing")

    outline_numbers = {int(e["chapter"]) for e in outline}
    if sdir.exists():
        for summ in sdir.glob("ch-*.json"):
            n = int(summ.stem.split("-")[1])
            if n not in outline_numbers:
                errors.append(f"{summ} has no matching outline entry")

    open_ids = [t.get("id") for t in (quill.get("open_threads") or [])]
    if len(open_ids) != len(set(open_ids)):
        errors.append("duplicate ids found in open_threads")
    resolved_ids = {t.get("id") for t in (quill.get("resolved_threads") or [])}
    overlap = resolved_ids.intersection(open_ids)
    if overlap:
        errors.append(f"thread ids appear in both open and resolved: {sorted(overlap)}")

    return errors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate or migrate a Quill project.")
    p.add_argument("--project-root", default=".")
    p.add_argument("--migrate", action="store_true", help="Migrate v1 quill.json to v2.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    if args.migrate:
        changed = migrate(root)
        print("migrated to schema v2" if changed else "already schema v2")
        return 0
    errors = validate(root)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
