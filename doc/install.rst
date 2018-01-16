
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
numpydoc_use_blockqutoes : bool
  Until version 0.8, parameter definitions were shown as blockquotes, rather
  than in a definition list.  If your styling requires blockquotes, switch
  this config option to True.  This option will be removed in version 0.10.
numpydoc_xref_param_type : bool
  Whether to create cross-references for the parameter types in the
  ``Parameters``, ``Other Parameters``, ``Returns`` and ``Yields``
  sections of the docstring.
  ``True`` by default.
numpydoc_xref_aliases : dict
  Mappings to fully qualified paths (or correct ReST references) for the
  aliases/shortcuts used when specifying the types of parameters.
  The keys should not have any spaces. Together with the ``intersphinx``
  extension, you can map to links in any documentation.
  The default is an empty ``dict``.

  If you have the following ``intersphinx`` namespace configuration::

      intersphinx_mapping = {
          'python': ('https://docs.python.org/3/', None),
          'numpy': ('https://docs.scipy.org/doc/numpy', None),
      }

  A useful ``dict`` may look like the following::

      numpydoc_xref_aliases = {
          # python
          'sequence': ':term:`python:sequence`',
          'iterable': ':term:`python:iterable`',
          'string': 'str',
          # numpy
          'array': 'numpy.ndarray',
          'dtype': 'numpy.dtype',
          'ndarray': 'numpy.ndarray',
          'matrix': 'numpy.matrix',
          'array-like': ':term:`numpy:array_like`',
          'array_like': ':term:`numpy:array_like`',
      }

   This option depends on the ``numpydoc_xref_param_type`` option
   being ``True``.

numpydoc_xref_ignore : set
    Words not to cross-reference. Most likely, these are common words
    used in parameter type descriptions that may be confused for
    classes of the same name. For example::

        numpydoc_xref_ignore = {'type', 'optional', 'default'}

    The default is an empty set.

numpydoc_edit_link : bool
  .. deprecated:: edit your HTML template instead

  Whether to insert an edit link after docstrings.
