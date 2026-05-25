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


def _v2_project(tmp_path):
    (tmp_path / "chapters").mkdir()
    (tmp_path / ".quill" / "summaries").mkdir(parents=True)
    quill = {
        "schema_version": 2,
        "format": "markdown",
        "outline": [{"chapter": 1, "status": "written"}],
        "open_threads": [],
        "resolved_threads": [],
    }
    (tmp_path / "quill.json").write_text(json.dumps(quill), encoding="utf-8")
    return tmp_path


def test_validate_flags_missing_chapter_and_summary(tmp_path):
    root = _v2_project(tmp_path)
    errors = validate.validate(root)
    assert any("ch-01.md is missing" in e for e in errors)
    assert any("ch-01.json is missing" in e for e in errors)


def test_validate_clean_project(tmp_path):
    root = _v2_project(tmp_path)
    (root / "chapters" / "ch-01.md").write_text("words", encoding="utf-8")
    (root / ".quill" / "summaries" / "ch-01.json").write_text(
        json.dumps({"chapter": 1}), encoding="utf-8"
    )
    assert validate.validate(root) == []


def test_validate_flags_orphan_summary(tmp_path):
    root = _v2_project(tmp_path)
    (root / "chapters" / "ch-01.md").write_text("words", encoding="utf-8")
    (root / ".quill" / "summaries" / "ch-01.json").write_text("{}", encoding="utf-8")
    (root / ".quill" / "summaries" / "ch-09.json").write_text("{}", encoding="utf-8")
    errors = validate.validate(root)
    assert any("ch-09.json has no matching outline entry" in e for e in errors)


def test_validate_flags_duplicate_open_thread_ids(tmp_path):
    root = _v2_project(tmp_path)
    (root / "chapters" / "ch-01.md").write_text("w", encoding="utf-8")
    (root / ".quill" / "summaries" / "ch-01.json").write_text("{}", encoding="utf-8")
    quill = json.loads((root / "quill.json").read_text())
    quill["open_threads"] = [{"id": "x"}, {"id": "x"}]
    (root / "quill.json").write_text(json.dumps(quill), encoding="utf-8")
    assert any("duplicate ids" in e for e in validate.validate(root))
