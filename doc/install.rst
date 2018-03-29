
============
Installation
============

The extension is available from:

* `numpydoc on PyPI <http://pypi.python.org/pypi/numpydoc>`_
* `numpydoc on GitHub <https://github.com/numpy/numpydoc/>`_

'numpydoc' should be added to the ``extensions`` option in your Sphinx
``conf.py``. (Note that `sphinx.ext.autosummary` will automatically be loaded
as well.)

Sphinx config options
=====================

The following options can be set in your Sphinx ``conf.py``:

numpydoc_use_plots : bool
  Whether to produce ``plot::`` directives for Examples sections that
  contain ``import matplotlib`` or ``from matplotlib import``.
numpydoc_show_class_members : bool
  Whether to show all members of a class in the Methods and Attributes
  sections automatically.
  ``True`` by default.
numpydoc_show_inherited_class_members : bool
  Whether to show all inherited members of a class in the Methods and Attributes
  sections automatically. If it's false, inherited members won't shown.
  ``True`` by default.
numpydoc_class_members_toctree : bool
  Whether to create a Sphinx table of contents for the lists of class
  methods and attributes. If a table of contents is made, Sphinx expects
  each entry to have a separate page.
  ``True`` by default.
numpydoc_citation_re : str
  A regular expression matching citations which
  should be mangled to avoid conflicts due to
  duplication across the documentation.  Defaults
  to ``[\w-]+``.
numpydoc_use_blockquotes : bool
  Until version 0.8, parameter definitions were shown as blockquotes, rather
  than in a definition list.  If your styling requires blockquotes, switch
  this config option to True.  This option will be removed in version 0.10.
numpydoc_edit_link : bool
  .. deprecated:: edit your HTML template instead

  Whether to insert an edit link after docstrings.
