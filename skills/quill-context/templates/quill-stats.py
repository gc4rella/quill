#!/usr/bin/env python3
"""Compute accurate word counts and progress for a Quill project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_MD_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_MD_INLINE_CODE = re.compile(r"`([^`]*)`")
_MD_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_MD_EMPHASIS = re.compile(r"[*_#>]")
_LATEX_COMMENT = re.compile(r"(?<!\\)%.*")
_LATEX_COMMAND = re.compile(r"\\[a-zA-Z]+\*?")
_BRACES = re.compile(r"[{}]")
_WS = re.compile(r"\s+")


def count_words(text: str, fmt: str) -> int:
    if fmt == "markdown":
        text = _MD_HTML_COMMENT.sub(" ", text)
        text = _MD_CODE_FENCE.sub(" ", text)
        text = _MD_INLINE_CODE.sub(r" \1 ", text)
        text = _MD_EMPHASIS.sub(" ", text)
    elif fmt == "latex":
        text = _LATEX_COMMENT.sub(" ", text)
        text = _LATEX_COMMAND.sub(" ", text)
        text = _BRACES.sub(" ", text)
    else:
        raise ValueError(f"unknown format: {fmt}")
    tokens = [t for t in _WS.split(text) if t.strip()]
    return len(tokens)


def chapter_word_count(path: Path, fmt: str) -> int:
    if not path.exists():
        return 0
    return count_words(path.read_text(encoding="utf-8"), fmt)


def gather_stats(project_root: Path) -> dict:
    quill = json.loads((project_root / "quill.json").read_text(encoding="utf-8"))
    fmt = quill.get("format")
    ext = "tex" if fmt == "latex" else "md"
    outline = quill.get("outline") or []
    per_chapter = {}
    total = 0
    written = 0
    for entry in outline:
        n = int(entry["chapter"])
        status = entry.get("status", "planned")
        path = project_root / "chapters" / f"ch-{n:02d}.{ext}"
        words = chapter_word_count(path, fmt) if status in {"written", "revised", "needs-revision"} else 0
        per_chapter[n] = words
        total += words
        if status in {"written", "revised", "needs-revision"}:
            written += 1
    target = int(quill.get("structure", {}).get("target_word_count") or 0)
    return {
        "per_chapter": per_chapter,
        "total_words": total,
        "target_words": target,
        "progress_pct": round(100 * total / target, 1) if target else None,
        "chapters_written": written,
        "chapters_total": len(outline),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Quill word-count and progress stats.")
    p.add_argument("--project-root", default=".")
    p.add_argument("--file", help="Count a single file instead of the whole project.")
    p.add_argument("--format", choices=["markdown", "latex"], help="Format for --file.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.file:
        if not args.format:
            print("--format is required with --file", file=sys.stderr)
            return 2
        print(chapter_word_count(Path(args.file), args.format))
        return 0
    stats = gather_stats(Path(args.project_root).resolve())
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
