import json
from pathlib import Path

import pytest
from sphinx.application import Sphinx

CONF = """
extensions = ["myst_parser", "sphinx_searchlite"]
project = "Demo"
html_theme = "basic"
"""

INDEX_MD = """
# Demo

Intro text.

```{toctree}

guide
```
"""

GUIDE_MD = """
# Guide

## First section

Content about widgets.

### Nested heading

More detail.

## Second section

Other content.
"""


def _build(tmp_path_factory, conf: str, name: str) -> Path:
    src = tmp_path_factory.mktemp(name)
    (src / "conf.py").write_text(conf)
    (src / "index.md").write_text(INDEX_MD)
    (src / "guide.md").write_text(GUIDE_MD)
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> Path:
    return _build(tmp_path_factory, CONF, "src")


@pytest.fixture(scope="module")
def records(built) -> list[dict]:
    return json.loads((built / "_static" / "searchlite-index.json").read_text())


class TestIndex:
    def test_index_is_emitted(self, built):
        assert (built / "_static" / "searchlite-index.json").is_file()

    def test_page_records_carry_url_title_and_text(self, records):
        assert {"u", "t", "x"} <= set(records[0])

    def test_sections_get_their_own_anchored_record(self, records):
        section = next(record for record in records if record.get("s") == "First section")
        assert section["u"].endswith("#first-section")
        assert "widgets" in section["x"]

    def test_section_text_excludes_nested_sections(self, records):
        section = next(record for record in records if record.get("s") == "First section")
        assert "More detail" not in section["x"]

    def test_page_title_is_not_duplicated_as_a_section(self, records):
        assert not [record for record in records if record.get("s") == "Guide"]

    def test_text_is_truncated_to_the_configured_limit(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + "\nsearchlite_max_text = 20\n", "src_short")
        entries = json.loads((out / "_static" / "searchlite-index.json").read_text())
        assert all(len(record["x"]) <= 20 for record in entries)


class TestAssets:
    def test_engine_is_linked_with_the_index_name(self, built):
        html = (built / "guide.html").read_text()
        assert "searchlite.js" in html
        assert 'data-searchlite-index="searchlite-index.json"' in html

    def test_bundled_ui_is_shipped_by_default(self, built):
        html = (built / "guide.html").read_text()
        assert "searchlite-ui.js" in html
        assert "searchlite.css" in html


class TestUiDisabled:
    @pytest.fixture(scope="class")
    @classmethod
    def built(cls, tmp_path_factory) -> Path:
        return _build(tmp_path_factory, CONF + "\nsearchlite_ui = False\n", "src_no_ui")

    def test_engine_is_still_shipped(self, built):
        assert "searchlite.js" in (built / "guide.html").read_text()

    def test_dialog_and_styles_are_omitted(self, built):
        html = (built / "guide.html").read_text()
        assert "searchlite-ui.js" not in html
        assert "searchlite.css" not in html

    def test_ui_assets_are_not_copied(self, built):
        assert not (built / "_static" / "searchlite-ui.js").exists()
        assert not (built / "_static" / "searchlite.css").exists()

    def test_index_is_still_emitted(self, built):
        assert (built / "_static" / "searchlite-index.json").is_file()


class TestThemeSearchAdoption:
    def test_adoption_is_advertised_to_the_ui_script(self, built):
        assert 'data-searchlite-adopt="true"' in (built / "guide.html").read_text()

    def test_adoption_can_be_switched_off(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + "\nsearchlite_adopt_theme_search = False\n", "src_no_adopt")
        assert 'data-searchlite-adopt="false"' in (out / "guide.html").read_text()

    def test_styles_no_longer_hardcode_a_dark_palette(self, built):
        css = (built / "_static" / "searchlite.css").read_text()
        # Colours are adopted from the host page instead, since themes signal
        # dark mode with their own class rather than the media query.
        assert "@media (prefers-color-scheme" not in css

    def test_palette_derives_from_two_variables(self, built):
        css = (built / "_static" / "searchlite.css").read_text()
        for name in ("--searchlite-muted", "--searchlite-border", "--searchlite-accent"):
            assert f"{name}: color-mix(" in css


class TestCustomFilename:
    def test_index_name_is_configurable(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + '\nsearchlite_index_filename = "docs-index.json"\n', "src_named")
        assert (out / "_static" / "docs-index.json").is_file()
        assert 'data-searchlite-index="docs-index.json"' in (out / "guide.html").read_text()
