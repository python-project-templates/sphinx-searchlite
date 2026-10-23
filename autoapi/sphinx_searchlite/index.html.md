# sphinx_searchlite

Client-side documentation search for any Sphinx theme.

Emits a small JSON index next to the build and ships a dependency-free BM25
engine to score it in the browser. Themes can either use the bundled dialog or
drive `window.SearchLite` themselves.

## Submodules

## Attributes

| [`STATIC_DIR`](#sphinx_searchlite.STATIC_DIR)   |    |
|-------------------------------------------------|----|
| [`ENGINE_DIR`](#sphinx_searchlite.ENGINE_DIR)   |    |
| [`UI_DIR`](#sphinx_searchlite.UI_DIR)           |    |

## Functions

| [`collect_records`](#sphinx_searchlite.collect_records)(→ list[dict[str, str]])   | Return one record for the page plus one per addressable section and object description.   |
|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| [`setup`](#sphinx_searchlite.setup)(→ dict[str, object])                          |                                                                                           |

## Package Contents

### sphinx_searchlite.collect_records(app, pagename: str, doctree: docutils.nodes.document) → list[dict[str, str]][[source]](../../_modules/sphinx_searchlite/_index.html.md#collect_records)

Return one record for the page plus one per addressable section and object description.

Keys are short because the index ships to the browser: `u` url, `t` page
title, `s` section heading, `x` text.

### sphinx_searchlite.STATIC_DIR

### sphinx_searchlite.ENGINE_DIR

### sphinx_searchlite.UI_DIR

### sphinx_searchlite.setup(app) → dict[str, object][[source]](../../_modules/sphinx_searchlite.html.md#setup)
