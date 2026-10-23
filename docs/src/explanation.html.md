# Explanation

## Why not Sphinx’s own search?

Sphinx ships `searchindex.js`, but it is tied to `searchtools.js` and the
dedicated `search.html` page, and there is no supported way to query it from
your own UI. searchlite writes plain JSON records instead, so a theme can score
and render results however it likes.

## How ranking works

Results are scored with BM25 over the record text, with extra weight for two
fields:

- the record’s own heading, weighted heavily
- the title of the page it belongs to, weighted lightly

These are kept separate because every section of a page shares that page’s
title. If both were weighted heavily, searching for a page title would rank
its subsections alongside the page itself, often above it.

The last word of the query is matched as a prefix as well as exactly, since
you are probably still typing it. That way `install` also finds
`installation`. Results must match every query word that appears in the index,
so adding words narrows the results. Words that appear nowhere in the index are
ignored.

## Why the dialog takes over the theme’s search box

Most themes render a search box that submits to `search.html`. Left alone, a
page would have two different searches, and the dialog would have no visible
way to open it. searchlite makes that box read-only and opens the dialog when
it is clicked, activated with `Enter` or `Space`, or its form is submitted.
It does not open on focus, because closing the dialog returns focus to the box,
which would open it again.

## How the dialog picks its colors

The dialog reads the page’s background and text colors and copies them onto
itself. It watches for changes, so it follows the theme’s light and dark
toggle. Most themes switch modes with a class or attribute, which
`prefers-color-scheme` does not detect.
