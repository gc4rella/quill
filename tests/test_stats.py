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
