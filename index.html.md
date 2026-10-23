# sphinx-searchlite

Client-side documentation search for any Sphinx theme. It needs no search
service, no runtime dependency, and no build step beyond Sphinx itself.

[![Build Status](https://github.com/python-project-templates/sphinx-searchlite/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/sphinx-searchlite/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/sphinx-searchlite/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/sphinx-searchlite)
[![License](https://img.shields.io/github/license/python-project-templates/sphinx-searchlite)](https://github.com/python-project-templates/sphinx-searchlite)
[![PyPI](https://img.shields.io/pypi/v/sphinx-searchlite.svg)](https://pypi.python.org/pypi/sphinx-searchlite)

## Quick start

Install the package:

```bash
pip install sphinx-searchlite
```

Add it to `conf.py`:

```python
extensions = ["sphinx_searchlite"]
```

Build your docs and open any page. Press `/` or `⌘K` (`Ctrl+K` on Linux and
Windows) to open the search dialog. If your theme has its own search box,
clicking it opens the same dialog.

## Documentation

- [How-to guides](docs/src/how-to.html.md): keep the theme’s search box, write your
  own UI, add triggers, and restyle the dialog.
- [Reference](docs/src/reference.html.md): configuration options, the JavaScript
  API, the index format, and CSS custom properties.
- [Explanation](docs/src/explanation.html.md): why searchlite exists, how ranking
  works, and how the dialog picks its colors.

#### NOTE
This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
