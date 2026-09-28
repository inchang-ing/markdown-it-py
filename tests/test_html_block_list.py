"""Regression tests for HTML blocks interacting with list items (#434)."""

import pytest

from markdown_it import MarkdownIt


@pytest.fixture
def md() -> MarkdownIt:
    return MarkdownIt("commonmark", {"html": True})


def test_html_block_under_indented_closes_list(md: MarkdownIt) -> None:
    """A type-7 HTML block at outer indentation ends the list, like cmark."""
    assert md.render("## Opts\n\n- a\n<br>\n## Next\n") == (
        "<h2>Opts</h2>\n"
        "<ul>\n"
        "<li>a</li>\n"
        "</ul>\n"
        "<br>\n## Next\n"
    )


def test_html_block_at_item_indent_is_lazy_continuation(md: MarkdownIt) -> None:
    """At the item's content indent, type 7 cannot interrupt the paragraph."""
    assert md.render("- a\n  <br>\n") == "<ul>\n<li>a\n<br></li>\n</ul>\n"


def test_html_block_cannot_interrupt_top_level_paragraph(md: MarkdownIt) -> None:
    assert md.render("para\n<br>\n") == "<p>para\n<br></p>\n"


def test_plain_text_is_still_lazy_continuation(md: MarkdownIt) -> None:
    assert md.render("- a\nb\n") == "<ul>\n<li>a\nb</li>\n</ul>\n"


def test_type_6_html_block_closes_list(md: MarkdownIt) -> None:
    assert md.render("- a\n<div>\n") == "<ul>\n<li>a</li>\n</ul>\n<div>\n"
