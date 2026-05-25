from conftest import load_script

stats = load_script("quill-stats.py")


def test_count_words_plain():
    assert stats.count_words("one two three", "markdown") == 3


def test_count_words_markdown_strips_code_fence():
    text = "alpha beta\n```\ncode that should not count here\n```\ngamma"
    assert stats.count_words(text, "markdown") == 3  # alpha beta gamma


def test_count_words_markdown_strips_inline_code_and_emphasis():
    assert stats.count_words("a `code` **bold** word", "markdown") == 4


def test_count_words_markdown_strips_html_comment():
    assert stats.count_words("<!-- title: X -->\nreal words only", "markdown") == 3


def test_count_words_latex_strips_commands_and_comments():
    text = "\\chapter{Title}\n% a comment\nReal prose words here."
    # "Title" counts (1) + Real prose words here (4) = 5
    assert stats.count_words(text, "latex") == 5


import json


def _make_project(tmp_path):
    (tmp_path / "chapters").mkdir()
    quill = {
        "format": "markdown",
        "structure": {"target_word_count": 10},
        "outline": [
            {"chapter": 1, "status": "written"},
            {"chapter": 2, "status": "planned"},
        ],
    }
    (tmp_path / "quill.json").write_text(json.dumps(quill), encoding="utf-8")
    (tmp_path / "chapters" / "ch-01.md").write_text("one two three four five", encoding="utf-8")
    return tmp_path


def test_gather_stats_counts_written_only(tmp_path):
    root = _make_project(tmp_path)
    result = stats.gather_stats(root)
    assert result["total_words"] == 5
    assert result["per_chapter"] == {1: 5, 2: 0}
    assert result["chapters_written"] == 1
    assert result["chapters_total"] == 2
    assert result["progress_pct"] == 50.0
