# sphinx-searchlite

Client-side documentation search for any Sphinx theme. No search service, no
runtime dependency, no build step beyond Sphinx itself.

```python
extensions = ["sphinx_searchlite"]
```

That is the whole setup. A `⌘K` / `/` dialog appears on every page, backed by a
JSON index emitted next to the build.

## Why not Sphinx's own search?

Sphinx ships `searchindex.js`, but it is coupled to `searchtools.js` and to the
dedicated `search.html` page. There is no supported way to query it from your
own UI. `sphinx-searchlite` emits plain records instead, so a theme can render
results however it likes.

## Ranking

Results are scored with BM25 over two fields:

- the record's own heading, boosted heavily
- the title of the page it belongs to, boosted lightly

The distinction matters. Boosting both together makes every section of a page
inherit that page's relevance, so searching for a page title surfaces its
subsections above the page itself.

The word you are still typing is matched as a prefix *in addition to* an exact
match, so `install` also reaches `installation`. All query words must match, so
extra words narrow the result set.

## Configuration

| Option                          | Default                 | Description                                                                     |
| ------------------------------- | ----------------------- | ------------------------------------------------------------------------------- |
| `searchlite_index_filename`     | `searchlite-index.json` | Written to `_static/`.                                                          |
| `searchlite_max_text`           | `1200`                  | Characters of body text kept per record.                                        |
| `searchlite_ui`                 | `True`                  | Ship the bundled dialog. Set `False` to supply your own.                        |
| `searchlite_adopt_theme_search` | `True`                  | Rebind the theme's own search box to the dialog. Set `False` to leave it alone. |

## Working with an existing theme

Most themes already render a search box wired to Sphinx's `search.html`. Left
alone that gives a page two different searches, and the dialog has no visible
trigger of its own. By default searchlite takes that box over: it is made
read-only, and focusing, clicking, or submitting it opens the dialog instead.

The dialog also adopts the page's own colours, so it follows a theme's
light/dark toggle rather than the `prefers-color-scheme` media query — themes
typically switch on a class or attribute, which that query does not track.

## Driving it yourself

Set `searchlite_ui = False` and use the engine directly:

```js
const engine = SearchLite.create({ url: SearchLite.indexUrl });

await engine.load();
const { items, terms } = engine.search("query");
```

Each item is `{ u, t, s, x }` — url, page title, section heading, text.
`terms` includes prefix expansions, so it can be passed to the bundled
`SearchLite.highlight(text, terms)` and `SearchLite.excerpt(record, terms)`
helpers.

Add `data-searchlite-open` to any element to make it a trigger.

## Styling

The bundled dialog reads `--searchlite-*` custom properties, so a theme can
recolour it without overriding rules:

```css
:root {
  --searchlite-background: #111;
  --searchlite-border: #333;
}
```

`--searchlite-muted`, `--searchlite-border`, and `--searchlite-accent` are
derived from `--searchlite-foreground`, so setting the background and
foreground pair is usually enough. Note that the adopted page colours are set
on the dialog element itself and so win over `:root`; style
`#searchlite-dialog` directly to override them.

## Licence

Apache-2.0.
