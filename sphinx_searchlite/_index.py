"""Build the client-side search index.

Sphinx's own ``searchindex.js`` is coupled to ``searchtools.js`` and its
dedicated ``search.html`` page. This emits plain records any front end can
score itself, keyed so that section anchors survive incremental builds.
"""

import json
import re
from pathlib import Path

from docutils import nodes

__all__ = ("collect_records", "setup_index")

_WHITESPACE = re.compile(r"\s+")
_ATTRIBUTE = "_sphinx_searchlite_records"


def _flatten(text: str, limit: int) -> str:
    return _WHITESPACE.sub(" ", text).strip()[:limit]


def _own_text(section: nodes.Element, limit: int) -> str:
    """Text belonging to a section, excluding its title and nested sections."""
    parts = [child.astext() for child in section.children if not isinstance(child, (nodes.section, nodes.title))]
    return _flatten(" ".join(parts), limit)


def collect_records(app, pagename: str, doctree: nodes.document) -> list[dict[str, str]]:
    """Return one record for the page plus one per addressable section.

    Keys are short because the index ships to the browser: ``u`` url, ``t`` page
    title, ``s`` section heading, ``x`` text.
    """
    limit = app.config.searchlite_max_text
    uri = app.builder.get_target_uri(pagename)
    title_node = app.env.titles.get(pagename)
    page_title = title_node.astext() if title_node else pagename
    records = [{"u": uri, "t": page_title, "x": _flatten(doctree.astext(), limit)}]
    for section in doctree.findall(nodes.section):
        if not section["ids"]:
            continue
        title = section.next_node(nodes.title)
        if title is None:
            continue
        heading = title.astext()
        if heading == page_title and section.parent is doctree:
            continue
        records.append({"u": f"{uri}#{section['ids'][0]}", "t": page_title, "s": heading, "x": _own_text(section, limit)})
    return records


def _store(app) -> dict[str, list[dict[str, str]]]:
    # Keyed by docname so incremental builds keep records for unchanged pages.
    if not hasattr(app.env, _ATTRIBUTE):
        setattr(app.env, _ATTRIBUTE, {})
    return getattr(app.env, _ATTRIBUTE)


def _on_page_context(app, pagename, templatename, context, doctree):
    if doctree is None or app.builder.format != "html":
        return
    _store(app)[pagename] = collect_records(app, pagename, doctree)


def _on_build_finished(app, exception):
    if exception is not None or app.builder.format != "html":
        return
    found = app.env.found_docs
    records = [record for docname, entries in sorted(_store(app).items()) if docname in found for record in entries]
    static = Path(app.builder.outdir) / "_static"
    static.mkdir(parents=True, exist_ok=True)
    (static / app.config.searchlite_index_filename).write_text(json.dumps(records, separators=(",", ":")), encoding="utf-8")


def setup_index(app) -> None:
    app.connect("html-page-context", _on_page_context)
    app.connect("build-finished", _on_build_finished)
