# sphinx_searchlite._index

Build the client-side search index.

Sphinx’s own `searchindex.js` is coupled to `searchtools.js` and its
dedicated `search.html` page. This emits plain records any front end can
score itself, keyed so that section anchors survive incremental builds.

## Functions

| [`collect_records`](#sphinx_searchlite._index.collect_records)(→ list[dict[str, str]])   | Return one record for the page plus one per addressable section and object description.   |
|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| [`setup_index`](#sphinx_searchlite._index.setup_index)(→ None)                           |                                                                                           |

## Module Contents

### sphinx_searchlite._index.collect_records(app, pagename: str, doctree: docutils.nodes.document) → list[dict[str, str]][[source]](../../../_modules/sphinx_searchlite/_index.html.md#collect_records)

Return one record for the page plus one per addressable section and object description.

Keys are short because the index ships to the browser: `u` url, `t` page
title, `s` section heading, `x` text.

### sphinx_searchlite._index.setup_index(app) → None[[source]](../../../_modules/sphinx_searchlite/_index.html.md#setup_index)
