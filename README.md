# CS Animation

![](https://shields.io/github/license/phuang1024/csanim)
![](https://shields.io/github/issues/phuang1024/csanim)
![](https://shields.io/github/issues-pr/phuang1024/csanim)
![](https://github.com/phuang1024/csanim/workflows/Tests/badge.svg)
![](https://readthedocs.org/projects/csanim/badge/?version=latest)
![](https://shields.io/github/repo-size/phuang1024/csanim)
![](https://shields.io/github/commit-activity/m/phuang1024/csanim)
![](https://readthedocs.org/projects/piano-video/badge/?version=latest)
![](https://img.shields.io/tokei/lines/github/phuang1024/csanim)

A tool for creating computer science explanatory videos.

Inspired by 3Blue1Brown.

[Documentation][docs]

## Installation

Please see the [docs page][install].

## Building

### Module

``` bash
# Install Python packages
pip install -r requirements.txt

# Build the C++ sources.
make cpp

# Next, build the wheel file.
make wheel

# Last (optional), install the wheel file.
make install
```

### Docs

``` bash
# The documentation uses sphinx autodoc, which depends
# on the module. Follow above instructions to build and
# install the module first.

# Install Python packages
pip install sphinx sphinx_rtd_theme

# Build docs with sphinx
make docs

# Open in a browser
firefox ./docs/_build/html/index.html
```

[docs]: https://csanim.rtfd.io
[install]: https://csanim.rtfd.io/en/latest/install.html
