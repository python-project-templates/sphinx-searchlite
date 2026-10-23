# Reference

## Configuration

Set these in `conf.py`.

| Option                          | Default                 | Description                                                                                 |
|---------------------------------|-------------------------|---------------------------------------------------------------------------------------------|
| `searchlite_index_filename`     | `searchlite-index.json` | Name of the index file written to `_static/`.                                               |
| `searchlite_max_text`           | `1200`                  | Maximum characters of body text kept per record.                                            |
| `searchlite_ui`                 | `True`                  | Ship the bundled dialog and its CSS. When `False`, only the engine is shipped.              |
| `searchlite_adopt_theme_search` | `True`                  | Make the theme’s search box open the dialog. Has no effect when `searchlite_ui` is `False`. |

## Index format

The index is a JSON array of records. Each page produces one record for the
page, one for each section that has an anchor, and one for each object
description that has an anchor, such as an autodoc class, method or attribute.

| Key   | Description                                                                                                             |
|-------|-------------------------------------------------------------------------------------------------------------------------|
| `u`   | URL relative to the documentation root, with `#anchor` for sections and objects.                                        |
| `t`   | Title of the page.                                                                                                      |
| `s`   | Section heading, or the object’s full name. Absent on page records.                                                     |
| `x`   | Text, truncated to `searchlite_max_text`. Sections exclude nested sections and objects; objects exclude nested objects. |

`engine.load()` rewrites `u` to an absolute URL.

## JavaScript API

The engine defines a global `SearchLite` object.

### `SearchLite.create({ url })`

Returns an engine for the index at `url`. Nothing is fetched until `load()` is
called.

### `engine.load()`

Fetches and indexes the records. Returns a promise. Repeated calls return the
same promise. A failed fetch produces an empty index.

### `engine.ready()`

Returns `true` once the index is built.

### `engine.search(query)`

Returns `{ items, terms }`. `items` is an array of up to 20 records, best match
first. `terms` lists the index terms that matched, including prefix expansions.
Returns empty arrays if the index is not loaded or the query has no words.

### `SearchLite.indexUrl`

Absolute URL of the index for the current page, or `null` if it cannot be
resolved.

### `SearchLite.tokenize(text)`

Returns the lowercase words in `text`, split on anything other than `a-z`,
`0-9`, and `_`.

### `SearchLite.excerpt(record, terms, length = 120)`

Returns about `length` characters of `record.x`, starting just before the first
matching term. Prefixed with `…` when it does not start at the beginning.

### `SearchLite.highlight(text, terms)`

Returns a `DocumentFragment` of `text` with each match wrapped in `<mark>`.

## Dialog

| Key                 | Action                     |
|---------------------|----------------------------|
| `/`, `⌘K`, `Ctrl+K` | Open the dialog.           |
| `↑`, `↓`            | Move between results.      |
| `Enter`             | Go to the selected result. |
| `Escape`            | Close the dialog.          |

Any element with the `data-searchlite-open` attribute opens the dialog when
clicked.

## CSS custom properties

| Property                  | Default                           | Set on                   |
|---------------------------|-----------------------------------|--------------------------|
| `--searchlite-background` | `#fff`, or the page background    | `:root`, then the dialog |
| `--searchlite-foreground` | `#18181b`, or the page text color | `:root`, then the dialog |
| `--searchlite-radius`     | `0.75rem`                         | `:root`                  |
| `--searchlite-muted`      | foreground at 60%                 | `#searchlite-dialog`     |
| `--searchlite-border`     | foreground at 20%                 | `#searchlite-dialog`     |
| `--searchlite-accent`     | foreground at 10%                 | `#searchlite-dialog`     |
