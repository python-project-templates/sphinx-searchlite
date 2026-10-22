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

API_RST = """
API
===

Intro to the API.

Gadgets
-------

Things that frob\\ *nicate*.

.. py:function:: legacy(x)
   :no-index:

   Kept for older callers.

.. py:function:: over(a)
                 over(a, b)

   Overloaded.

.. cpp:class:: template<typename T> ns::Thing

   A templated thing.

.. py:class:: Gadget

   A gadget that frobnicates.

   .. py:method:: spin(speed)

      Spins the gadget sprocket.

.. py:data:: TIMEOUT

   Seconds before the gadget gives up.

.. py:module:: north

.. py:class:: Client

   Northern client.

   .. py:method:: connect()

      Opens the northern connection.

.. py:module:: south

.. py:class:: Client

   Southern client.

   .. py:method:: connect()

      Opens the southern connection.

.. cpp:namespace:: tools

.. cpp:class:: Socket

   Network socket.

   .. cpp:function:: void open()

      Opens the socket.

.. c:struct:: Data

   C structure.

   .. c:member:: int count

      Counts the entries.
"""


def _build(tmp_path_factory, conf: str, name: str) -> Path:
    src = tmp_path_factory.mktemp(name)
    (src / "conf.py").write_text(conf)
    (src / "index.md").write_text(INDEX_MD.replace("guide\n", "guide\napi\n"))
    (src / "guide.md").write_text(GUIDE_MD)
    (src / "api.rst").write_text(API_RST)
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


class TestResultLinks:
    def test_urls_resolve_against_the_documentation_root(self, built):
        js = (built / "_static" / "searchlite.js").read_text()
        # Records store root-relative urls, so a page nested below the root
        # would otherwise resolve them against its own directory.
        assert 'new URL("../", new URL(url, document.baseURI))' in js


class TestThemeSearchAdoption:
    def test_adoption_is_advertised_to_the_ui_script(self, built):
        assert 'data-searchlite-adopt="true"' in (built / "guide.html").read_text()

    def test_adoption_can_be_switched_off(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + "\nsearchlite_adopt_theme_search = False\n", "src_no_adopt")
        assert 'data-searchlite-adopt="false"' in (out / "guide.html").read_text()

    def test_adopted_fields_do_not_reopen_the_dialog_on_focus(self, built):
        js = (built / "_static" / "searchlite-ui.js").read_text()
        # Closing the dialog restores focus to the field that opened it, so an
        # opener bound to `focus` would reopen it and trap the reader.
        assert 'field.addEventListener("focus", open)' not in js

    def test_escape_closes_the_dialog_on_the_first_press(self, built):
        js = (built / "_static" / "searchlite-ui.js").read_text()
        # `<input type=search>` eats the first Escape to clear itself.
        assert 'event.key === "Escape"' in js

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


class TestObjectDescriptions:
    def test_objects_get_their_own_anchored_record(self, records):
        record = next(record for record in records if record.get("s") == "Gadget")
        assert record["u"] == "api.html#Gadget"
        assert record["t"] == "API"
        assert "A gadget that frobnicates" in record["x"]

    def test_nested_objects_are_indexed_by_full_name(self, records):
        record = next(record for record in records if record.get("s") == "Gadget.spin")
        assert record["u"] == "api.html#Gadget.spin"
        assert "sprocket" in record["x"]

    @pytest.mark.parametrize(
        ("name", "anchor"),
        [
            ("north.Client.connect", "north.Client.connect"),
            ("south.Client.connect", "south.Client.connect"),
            ("tools::Socket::open", "_CPPv4N5tools6Socket4openEv"),
            ("Data.count", "c.Data.count"),
        ],
    )
    def test_object_names_include_module_and_parent_scope(self, records, name, anchor):
        record = next(record for record in records if record["u"] == f"api.html#{anchor}")
        assert record["s"] == name

    def test_scoped_names_do_not_depend_on_object_toc_entries(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + "\ntoc_object_entries = False\n", "src_no_object_toc")
        entries = json.loads((out / "_static" / "searchlite-index.json").read_text())
        names = {record.get("s") for record in entries}
        assert {"north.Client.connect", "south.Client.connect", "tools::Socket::open", "Data.count"} <= names

    def test_object_text_excludes_nested_objects(self, records):
        record = next(record for record in records if record.get("s") == "Gadget")
        assert "sprocket" not in record["x"]

    def test_section_text_excludes_object_descriptions(self, records):
        section = next(record for record in records if record.get("s") == "Gadgets")
        assert "A gadget" not in section["x"]
        assert "Seconds before" not in section["x"]

    def test_inline_markup_does_not_split_words(self, records):
        section = next(record for record in records if record.get("s") == "Gadgets")
        assert "Things that frobnicate" in section["x"]

    def test_unindexed_objects_stay_in_section_text(self, records):
        section = next(record for record in records if record.get("s") == "Gadgets")
        assert "Kept for older callers" in section["x"]
        assert not [record for record in records if record.get("s") == "legacy"]

    def test_every_overload_is_searchable(self, records):
        record = next(record for record in records if record.get("s") == "over")
        assert "over(a)" in record["x"]
        assert "over(a, b)" in record["x"]

    def test_names_without_fullname_omit_signature_syntax(self, records):
        record = next(record for record in records if "_CPP" in record["u"])
        assert record["s"] == "ns::Thing"

    def test_objects_past_the_text_limit_stay_searchable(self, tmp_path_factory):
        out = _build(tmp_path_factory, CONF + "\nsearchlite_max_text = 20\n", "src_short_api")
        entries = json.loads((out / "_static" / "searchlite-index.json").read_text())
        assert any(record.get("s") == "TIMEOUT" for record in entries)
