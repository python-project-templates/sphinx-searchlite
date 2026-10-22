"""Build the client-side search index.

Sphinx's own ``searchindex.js`` is coupled to ``searchtools.js`` and its
dedicated ``search.html`` page. This emits plain records any front end can
score itself, keyed so that section anchors survive incremental builds.
"""

import json
import re
from pathlib import Path

from docutils import nodes
from sphinx import addnodes

__all__ = ("collect_records", "setup_index")

_WHITESPACE = re.compile(r"\s+")
_ATTRIBUTE = "_sphinx_searchlite_records"
_OBJECT_NAMES = "_sphinx_searchlite_object_names"


def _flatten(text: str, limit: int) -> str:
    return _WHITESPACE.sub(" ", text).strip()[:limit]


def _anchor(desc: addnodes.desc) -> addnodes.desc_signature | None:
    """The object's first anchored signature, or ``None`` if it gets no record (e.g. ``:no-index:``)."""
    return next((child for child in desc.children if isinstance(child, addnodes.desc_signature) and child["ids"]), None)


def _without_objects(node: nodes.Node) -> str:
    """Text of ``node``, leaving out object descriptions that get their own records."""
    if isinstance(node, addnodes.desc) and _anchor(node) is not None:
        return ""
    # Defer to ``astext()`` wherever possible, since nodes like parameter lists override it.
    if not isinstance(node, nodes.Element) or not any(_anchor(desc) is not None for desc in node.findall(addnodes.desc)):
        return node.astext()
    # Match ``Element.astext()`` so inline markup inside a word does not split it.
    return node.child_text_separator.join(_without_objects(child) for child in node.children)


def _own_text(section: nodes.Element, limit: int) -> str:
    """Text belonging to a section, excluding its title, nested sections and object descriptions."""
    parts = [_without_objects(child) for child in section.children if not isinstance(child, (nodes.section, nodes.title))]
    return _flatten(" ".join(parts), limit)


def _object_name(signature: addnodes.desc_signature) -> str:
    """Qualified name of the object, without the types and parameters of C/C++ signatures."""
    if signature.get("fullname"):
        return signature["fullname"]
    # Multi-line signatures, such as C++ templates, put the declared name on the last line.
    lines = [child for child in signature.children if isinstance(child, addnodes.desc_signature_line)] or [signature]
    name = "".join(child.astext() for child in lines[-1].children if isinstance(child, (addnodes.desc_addname, addnodes.desc_name)))
    return name or signature.astext()


def _object_records(doctree: nodes.document, uri: str, page_title: str, limit: int, names: dict[str, str]) -> list[dict[str, str]]:
    """One record per anchored object description, such as an autodoc class, method or field.

    API reference pages are mostly object descriptions with few headings, so
    without these anything past the first ``limit`` characters of a section is
    unsearchable.
    """
    records = []
    for desc in doctree.findall(addnodes.desc):
        signature = _anchor(desc)
        if signature is None:
            continue
        # Every signature's text, so overloads stay searchable, then the body.
        text = " ".join(_without_objects(child) for child in desc.children)
        anchor = signature["ids"][0]
        name = names.get(anchor) or _object_name(signature)
        records.append({"u": f"{uri}#{anchor}", "t": page_title, "s": name, "x": _flatten(text, limit)})
    return records


def collect_records(app, pagename: str, doctree: nodes.document) -> list[dict[str, str]]:
    """Return one record for the page plus one per addressable section and object description.

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
    names = getattr(app, _OBJECT_NAMES, {}).get(pagename, {})
    records.extend(_object_records(doctree, uri, page_title, limit, names))
    return records


def _store(app) -> dict[str, list[dict[str, str]]]:
    # Keyed by docname so incremental builds keep records for unchanged pages.
    if not hasattr(app.env, _ATTRIBUTE):
        setattr(app.env, _ATTRIBUTE, {})
    return getattr(app.env, _ATTRIBUTE)


def _on_env_updated(app, env) -> None:
    names: dict[str, dict[str, str]] = {}
    for domain in env.domains.values():
        for name, _, _, docname, anchor, _ in domain.get_objects():
            # Parameters can share their enclosing object's target; keep the object's name.
            names.setdefault(docname, {}).setdefault(anchor, name)
    setattr(app, _OBJECT_NAMES, names)


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
    app.connect("env-updated", _on_env_updated)
    app.connect("html-page-context", _on_page_context)
    app.connect("build-finished", _on_build_finished)
