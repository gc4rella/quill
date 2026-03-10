#!/usr/bin/env python3
"""Create or refresh Quill chapter stub files from quill.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MARKDOWN_STUB = "<!-- quill:chapter-stub -->"
LATEX_STUB = "% quill:chapter-stub"
MARKDOWN_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or refresh chapter stub files from quill.json.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to the Quill project root (defaults to current directory).",
    )
    return parser.parse_args()


def load_project(project_root: Path) -> dict:
    quill_path = project_root / "quill.json"
    if not quill_path.exists():
        raise SystemExit(f"Missing {quill_path}")
    try:
        return json.loads(quill_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {quill_path}: {exc}") from exc


def get_format(project: dict) -> str:
    fmt = project.get("format")
    if fmt not in {"latex", "markdown"}:
        raise SystemExit("quill.json must set format to 'latex' or 'markdown'.")
    return fmt


def chapter_path(project_root: Path, chapter_number: int, fmt: str) -> Path:
    extension = "tex" if fmt == "latex" else "md"
    return project_root / "chapters" / f"ch-{chapter_number:02d}.{extension}"


def is_stub(content: str, fmt: str) -> bool:
    stripped = content.lstrip()
    if not stripped:
        return True
    marker = LATEX_STUB if fmt == "latex" else MARKDOWN_STUB
    if not stripped.startswith(marker):
        return False

    if fmt == "markdown":
        without_comments = MARKDOWN_COMMENT_RE.sub("", content)
        return without_comments.strip() == ""

    meaningful_lines = []
    for line in content.splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("%"):
            continue
        meaningful_lines.append(stripped_line)
    return (
        len(meaningful_lines) == 1
        and meaningful_lines[0].startswith(r"\chapter{")
        and meaningful_lines[0].endswith("}")
    )


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    escaped = value
    for old, new in replacements.items():
        escaped = escaped.replace(old, new)
    return escaped


def one_line(value: object, default: str) -> str:
    text = str(value or "").strip()
    text = " ".join(text.split())
    return text or default


def render_stub(entry: dict, fmt: str) -> str:
    chapter_number = int(entry["chapter"])
    title = one_line(entry.get("title"), f"Chapter {chapter_number}")
    brief = one_line(entry.get("brief"), "Outline brief pending.")
    purpose = one_line(entry.get("purpose"), "Purpose pending.")
    target_words = entry.get("target_words")

    if fmt == "latex":
        lines = [
            LATEX_STUB,
            f"\\chapter{{{latex_escape(title)}}}",
            "%",
            f"% brief: {brief}",
            f"% purpose: {purpose}",
        ]
        if target_words not in {None, ""}:
            lines.append(f"% target_words: {target_words}")
        lines.extend(
            [
                "%",
                "% Replace this stub with drafted chapter prose.",
                "% Keep only chapter-level LaTeX in this file.",
                "",
            ]
        )
        return "\n".join(lines)

    lines = [
        MARKDOWN_STUB,
        f"<!-- title: {title} -->",
        f"<!-- brief: {brief} -->",
        f"<!-- purpose: {purpose} -->",
    ]
    if target_words not in {None, ""}:
        lines.append(f"<!-- target_words: {target_words} -->")
    lines.extend(
        [
            "",
            "<!-- Replace this stub with drafted chapter prose. -->",
            "<!-- Keep this file free of a top-level heading. -->",
            "",
        ]
    )
    return "\n".join(lines)


def sync_outline(project_root: Path) -> int:
    project = load_project(project_root)
    fmt = get_format(project)
    outline = project.get("outline") or []
    chapters_dir = project_root / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    updated = 0
    preserved = 0

    for entry in sorted(outline, key=lambda item: int(item["chapter"])):
        chapter_number = int(entry["chapter"])
        path = chapter_path(project_root, chapter_number, fmt)
        content = render_stub(entry, fmt)

        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created += 1
            print(f"created {path.relative_to(project_root)}")
            continue

        existing = path.read_text(encoding="utf-8")
        if is_stub(existing, fmt):
            if existing != content:
                path.write_text(content, encoding="utf-8")
                updated += 1
                print(f"updated {path.relative_to(project_root)}")
            continue

        preserved += 1
        print(f"preserved {path.relative_to(project_root)}")

    print(
        f"done: created={created} updated={updated} preserved={preserved} total={len(outline)}"
    )
    return 0


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    try:
        return sync_outline(project_root)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        print(code, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
