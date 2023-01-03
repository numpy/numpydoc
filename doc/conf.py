# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
import numpydoc

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

# for example.py
sys.path.insert(0, os.path.abspath("."))
# project root
sys.path.insert(0, os.path.abspath(".."))

os.environ["MPLBACKEND"] = "Agg"  # avoid tkinter import errors on rtfd.io

# -- Project information -----------------------------------------------------

project = "numpydoc"
copyright = f"2019-{date.today().year}, numpydoc maintainers"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.

# version = .__version__
# The full version, including alpha/beta/rc tags.
release = numpydoc.__version__
version = numpydoc.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "numpydoc",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The root toctree document
# master_doc = "index"  # NOTE: will be changed to `root_doc` in sphinx 4

numpydoc_xref_param_type = True
numpydoc_xref_ignore = {"optional", "type_without_description", "BadException"}
# Run docstring validation as part of build process
numpydoc_validation_checks = {"all", "GL01", "SA04", "RT03"}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/numpy/numpydoc",
    "show_prev_next": False,
    "navbar_end": ["search-field.html", "navbar-icon-links.html"],
}
# NOTE: The following is required for supporting of older sphinx toolchains.
#       The "theme-switcher" templated should be added directly to navbar_end
#       above and the following lines removed when the minimum supported
#       version of pydata_sphinx_theme is 0.9.0
# Add version switcher for versions of pydata_sphinx_theme that support it
import packaging
import pydata_sphinx_theme

if packaging.version.parse(pydata_sphinx_theme.__version__) >= packaging.version.parse(
    "0.9.0"
):
    html_theme_options["navbar_end"].insert(0, "theme-switcher")


html_sidebars = {
    "**": [],
}
html_context = {
    "default_mode": "light",
}

html_title = f"{project} v{version} Manual"
html_last_updated_fmt = "%b %d, %Y"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []  # ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = "project-templatedoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        "index",
        "numpydoc.tex",
        "numpydoc Documentation",
        "Numpydoc maintainers",
        "manual",
    ),
]

# -- Intersphinx setup ----------------------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/devdocs/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}
