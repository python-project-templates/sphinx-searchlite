# How-to guides

## Keep the theme’s own search box

By default searchlite takes over the theme’s search box so that it opens the
dialog. To leave the box wired to Sphinx’s `search.html`, set:

```python
searchlite_adopt_theme_search = False
```

The dialog still opens with `/` and `⌘K`, and from any element with
`data-searchlite-open`.

## Add a button that opens the dialog

Add the `data-searchlite-open` attribute to any element in your templates:

```html
<button type="button" data-searchlite-open>Search</button>
```

## Use your own search UI

Turn off the bundled dialog so only the engine is shipped:

```python
searchlite_ui = False
```

Then query the engine from your own script:

```js
const engine = SearchLite.create({ url: SearchLite.indexUrl });

await engine.load();
const { items, terms } = engine.search("query");

for (const item of items) {
  const snippet = SearchLite.highlight(SearchLite.excerpt(item, terms), terms);
  // render item.u, item.t, item.s, and snippet
}
```

See the [JavaScript API](reference.html.md#javascript-api) for what each call
returns.

## Restyle the dialog

Set `--searchlite-*` custom properties on `#searchlite-dialog`:

```css
#searchlite-dialog {
  --searchlite-background: #111;
  --searchlite-foreground: #eee;
  --searchlite-radius: 0.25rem;
}
```

Target the dialog element rather than `:root`. The dialog copies the page’s
colors onto itself at runtime, and those inline values override anything
inherited from `:root`. Setting the background and foreground is usually
enough, because the muted, border, and accent colors are mixed from the
foreground.
