# test_searchlite

## Attributes

| [`CONF`](#test_searchlite.CONF)         |    |
|-----------------------------------------|----|
| [`INDEX_MD`](#test_searchlite.INDEX_MD) |    |
| [`GUIDE_MD`](#test_searchlite.GUIDE_MD) |    |
| [`API_RST`](#test_searchlite.API_RST)   |    |

## Classes

| [`TestIndex`](#test_searchlite.TestIndex)                             |    |
|-----------------------------------------------------------------------|----|
| [`TestAssets`](#test_searchlite.TestAssets)                           |    |
| [`TestUiDisabled`](#test_searchlite.TestUiDisabled)                   |    |
| [`TestResultLinks`](#test_searchlite.TestResultLinks)                 |    |
| [`TestThemeSearchAdoption`](#test_searchlite.TestThemeSearchAdoption) |    |
| [`TestCustomFilename`](#test_searchlite.TestCustomFilename)           |    |
| [`TestObjectDescriptions`](#test_searchlite.TestObjectDescriptions)   |    |

## Functions

| [`_build`](#test_searchlite._build)(→ pathlib.Path)   |    |
|-------------------------------------------------------|----|
| [`built`](#test_searchlite.built)(→ pathlib.Path)     |    |
| [`records`](#test_searchlite.records)(→ list[dict])   |    |

## Module Contents

### test_searchlite.CONF *= Multiline-String*

<details><summary>Show Value</summary>
```python
"""
extensions = ["myst_parser", "sphinx_searchlite"]
project = "Demo"
html_theme = "basic"
"""
```

</details>

### test_searchlite.INDEX_MD *= Multiline-String*

<details><summary>Show Value</summary>
```python
"""
# Demo

Intro text.

```{toctree}

guide
```
"""
```

</details>

### test_searchlite.GUIDE_MD *= Multiline-String*

<details><summary>Show Value</summary>
```python
"""
# Guide

## First section

Content about widgets.

### Nested heading

More detail.

## Second section

Other content.
"""
```

</details>

### test_searchlite.API_RST *= Multiline-String*

<details><summary>Show Value</summary>
```python
"""
API
===

Intro to the API.

Gadgets
-------

Things that frob\ *nicate*.

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
```

</details>

### test_searchlite.\_build(tmp_path_factory, conf: str, name: str) → pathlib.Path

### test_searchlite.built(tmp_path_factory) → pathlib.Path

### test_searchlite.records(built) → list[dict]

### *class* test_searchlite.TestIndex

#### test_index_is_emitted(built)

#### test_page_records_carry_url_title_and_text(records)

#### test_sections_get_their_own_anchored_record(records)

#### test_section_text_excludes_nested_sections(records)

#### test_page_title_is_not_duplicated_as_a_section(records)

#### test_text_is_truncated_to_the_configured_limit(tmp_path_factory)

### *class* test_searchlite.TestAssets

#### test_engine_is_linked_with_the_index_name(built)

#### test_bundled_ui_is_shipped_by_default(built)

### *class* test_searchlite.TestUiDisabled

#### *classmethod* built(tmp_path_factory) → pathlib.Path

#### test_engine_is_still_shipped(built)

#### test_dialog_and_styles_are_omitted(built)

#### test_ui_assets_are_not_copied(built)

#### test_index_is_still_emitted(built)

### *class* test_searchlite.TestResultLinks

#### test_urls_resolve_against_the_documentation_root(built)

### *class* test_searchlite.TestThemeSearchAdoption

#### test_adoption_is_advertised_to_the_ui_script(built)

#### test_adoption_can_be_switched_off(tmp_path_factory)

#### test_adopted_fields_do_not_reopen_the_dialog_on_focus(built)

#### test_escape_closes_the_dialog_on_the_first_press(built)

#### test_styles_no_longer_hardcode_a_dark_palette(built)

#### test_palette_derives_from_two_variables(built)

### *class* test_searchlite.TestCustomFilename

#### test_index_name_is_configurable(tmp_path_factory)

### *class* test_searchlite.TestObjectDescriptions

#### test_objects_get_their_own_anchored_record(records)

#### test_nested_objects_are_indexed_by_full_name(records)

#### test_object_names_include_module_and_parent_scope(records, name, anchor)

#### test_scoped_names_do_not_depend_on_object_toc_entries(tmp_path_factory)

#### test_object_text_excludes_nested_objects(records)

#### test_section_text_excludes_object_descriptions(records)

#### test_inline_markup_does_not_split_words(records)

#### test_unindexed_objects_stay_in_section_text(records)

#### test_every_overload_is_searchable(records)

#### test_names_without_fullname_omit_signature_syntax(records)

#### test_objects_past_the_text_limit_stay_searchable(tmp_path_factory)
