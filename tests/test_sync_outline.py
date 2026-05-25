from conftest import load_script

sync = load_script("quill-sync-outline.py")


def test_is_stub_empty_markdown():
    assert sync.is_stub("", "markdown") is True


def test_is_stub_marker_only_markdown():
    content = "<!-- quill:chapter-stub -->\n<!-- title: X -->\n"
    assert sync.is_stub(content, "markdown") is True


def test_is_stub_false_when_prose_markdown():
    content = "<!-- quill:chapter-stub -->\nReal prose here.\n"
    assert sync.is_stub(content, "markdown") is False


def test_is_stub_latex_chapter_only():
    content = "% quill:chapter-stub\n\\chapter{Title}\n"
    assert sync.is_stub(content, "latex") is True


def test_is_stub_latex_false_with_prose():
    content = "% quill:chapter-stub\n\\chapter{Title}\nReal prose.\n"
    assert sync.is_stub(content, "latex") is False


def test_latex_escape_specials():
    assert sync.latex_escape("a & b % c _ d") == r"a \& b \% c \_ d"


def test_latex_escape_backslash_no_double_escape():
    # backslash becomes \textbackslash{} and the braces are NOT re-escaped
    assert sync.latex_escape("a\\b") == r"a\textbackslash{}b"


def test_render_stub_markdown_has_marker_and_title():
    entry = {"chapter": 1, "title": "Opening", "brief": "b", "purpose": "p"}
    out = sync.render_stub(entry, "markdown")
    assert out.startswith("<!-- quill:chapter-stub -->")
    assert "<!-- title: Opening -->" in out


def test_render_stub_latex_has_marker_and_chapter():
    entry = {"chapter": 2, "title": "Two", "brief": "b", "purpose": "p"}
    out = sync.render_stub(entry, "latex")
    assert out.startswith("% quill:chapter-stub")
    assert "\\chapter{Two}" in out
