"""Client-side documentation search for any Sphinx theme.

Emits a small JSON index next to the build and ships a dependency-free BM25
engine to score it in the browser. Themes can either use the bundled dialog or
drive ``window.SearchLite`` themselves.
"""

from pathlib import Path

from ._index import collect_records, setup_index

__all__ = ("ENGINE_DIR", "STATIC_DIR", "UI_DIR", "collect_records", "setup")
__version__ = "0.1.0"

STATIC_DIR = Path(__file__).parent / "static"
ENGINE_DIR = STATIC_DIR / "engine"
UI_DIR = STATIC_DIR / "ui"


def _on_builder_inited(app) -> None:
    if app.builder.format != "html":
        return
    # Sphinx flattens each static path into ``_static``, so keeping the optional
    # UI in its own directory means it is not copied when it is switched off.
    app.config.html_static_path.append(str(ENGINE_DIR))
    # The index filename rides on the script tag so the engine can resolve the
    # index relative to its own URL, which works from any page depth.
    app.add_js_file(
        "searchlite.js",
        loading_method="defer",
        **{"data-searchlite-index": app.config.searchlite_index_filename},
    )
    if app.config.searchlite_ui:
        app.config.html_static_path.append(str(UI_DIR))
        app.add_js_file(
            "searchlite-ui.js",
            loading_method="defer",
            **{"data-searchlite-adopt": "true" if app.config.searchlite_adopt_theme_search else "false"},
        )
        app.add_css_file("searchlite.css")


def setup(app) -> dict[str, object]:
    app.add_config_value("searchlite_index_filename", "searchlite-index.json", "html")
    app.add_config_value("searchlite_max_text", 1200, "html")
    app.add_config_value("searchlite_ui", True, "html")
    app.add_config_value("searchlite_adopt_theme_search", True, "html")
    app.connect("builder-inited", _on_builder_inited)
    setup_index(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
