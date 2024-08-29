"""Sphinx configuration."""
project = "bmh"
author = "Alexander Gundermann"
copyright = "2024, Alexander Gundermann"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
