import json
from conftest import load_script

validate = load_script("quill-validate.py")


def _v1_project(tmp_path):
    quill = {
        "title": "Book",
        "format": "markdown",
        "structure": {"chapter_count": 3},
        "outline": [
            {"chapter": 1, "status": "written"},
            {"chapter": 2, "status": "written"},
        ],
        "chapter_summaries": {
            "1": {"what_happened_or_covered": "c1", "actual_word_count": 100},
            "2": {"what_happened_or_covered": "c2", "actual_word_count": 200},
        },
        "last_chapter_written": 2,
        "last_chapter_ending": "the final words of chapter two",
    }
    (tmp_path / "quill.json").write_text(json.dumps(quill), encoding="utf-8")
    return tmp_path


def test_migrate_creates_summary_files(tmp_path):
    root = _v1_project(tmp_path)
    validate.migrate(root)
    s1 = json.loads((root / ".quill" / "summaries" / "ch-01.json").read_text())
    s2 = json.loads((root / ".quill" / "summaries" / "ch-02.json").read_text())
    assert s1["what_happened_or_covered"] == "c1"
    assert s1["chapter"] == 1
    assert s1["ending_excerpt"] == ""            # not the last written chapter
    assert s2["ending_excerpt"] == "the final words of chapter two"  # last written


def test_migrate_rewrites_quill_json(tmp_path):
    root = _v1_project(tmp_path)
    validate.migrate(root)
    quill = json.loads((root / "quill.json").read_text())
    assert quill["schema_version"] == 2
    assert "chapter_summaries" not in quill
    assert "last_chapter_ending" not in quill


def test_migrate_is_idempotent(tmp_path):
    root = _v1_project(tmp_path)
    validate.migrate(root)
    first = (root / "quill.json").read_text()
    validate.migrate(root)  # second run is a no-op
    assert (root / "quill.json").read_text() == first
