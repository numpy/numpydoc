===============
Getting started
===============

Installation
============

This extension requires Python 3.7+, sphinx 4.2+ and is available from:

* `numpydoc on PyPI <http://pypi.python.org/pypi/numpydoc>`_
* `numpydoc on GitHub <https://github.com/numpy/numpydoc/>`_

`'numpydoc'` should be added to the ``extensions`` option in your Sphinx
``conf.py``. ``'sphinx.ext.autosummary'`` will automatically be loaded
as well.

Configuration
=============

The following options can be set in your Sphinx ``conf.py``:

numpydoc_use_plots : bool
  Whether to produce ``plot::`` directives for Examples sections that
  contain ``import matplotlib`` or ``from matplotlib import``.
numpydoc_show_class_members : bool
  Whether to show all members of a class in the Methods and Attributes
  sections automatically.
  ``True`` by default.
numpydoc_show_inherited_class_members : bool | dict
  Whether to show all inherited members of a class in the Methods and Attributes
  sections automatically. If it's false, inherited members won't shown.
  ``True`` by default. It can also be a dict mapping names of classes to
  boolean values (missing keys are treated as ``True``).
  For example, ``defaultdict(lambda: False, {'mymod.MyClass': True})``
  would only show inherited class members for ``MyClass``, whereas
  ``{'mymod.MyClass': False}`` would show inherited class members for all
  classes except ``MyClass``. Note that disabling this for a limited set of
  classes might simultaneously require the use of a separate, custom
  autosummary class template with ``:no-inherited-members:`` in the
  ``autoclass`` directive options.
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
numpydoc_attributes_as_param_list : bool
  Whether to format the Attributes section of a class page in the same way
  as the Parameter section. If it's False, the Attributes section will be
  formatted as the Methods section using an autosummary table.
  ``True`` by default.
numpydoc_xref_param_type : bool
  Whether to create cross-references for the parameter types in the
  ``Parameters``, ``Other Parameters``, ``Returns`` and ``Yields``
  sections of the docstring.
  ``False`` by default.

  .. note:: Depending on the link types, the CSS styles might be different.
            consider overriding e.g. ``span.classifier a span.xref`` and
            ``span.classifier a code.docutils.literal.notranslate``
            CSS classes to achieve a uniform appearance.

numpydoc_xref_aliases : dict
  Mappings to fully qualified paths (or correct ReST references) for the
  aliases/shortcuts used when specifying the types of parameters.
  The keys should not have any spaces. Together with the ``intersphinx``
  extension, you can map to links in any documentation.

  The default ``numpydoc_xref_aliases`` will supply some common ``Python``
  standard library and ``NumPy`` names for you. Then for your module, a useful
  ``dict`` may look like the following (e.g., if you were documenting
  :mod:`sklearn.model_selection`)::

      numpydoc_xref_aliases = {
          'LeaveOneOut': 'sklearn.model_selection.LeaveOneOut',
          ...
      }

  This option depends on the ``numpydoc_xref_param_type`` option
  being ``True``.
numpydoc_xref_ignore : set or ``"all"``
  How to handle terms not in ``numpydoc_xref_aliases`` when
  ``numpydoc_xref_aliases=True``. The value can either be a ``set``
  containing terms to ignore, or ``"all"``. In the former case, the set
  contains words not to cross-reference. Most likely, these are common words
  used in parameter type descriptions that may be confused for
  classes of the same name. For example::

      numpydoc_xref_ignore = {'type', 'optional', 'default'}

  The default is an empty set.

  If the ``numpydoc_xref_ignore="all"``, then all unrecognized terms are
  ignored, i.e. terms not in ``numpydoc_xref_aliases`` are *not* wrapped in
  ``:obj:`` roles.
  This configuration parameter may be useful if you only want to create
  cross references for a small number of terms. In this case, including the
  desired cross reference mappings in ``numpydoc_xref_aliases`` and setting
  ``numpydoc_xref_ignore="all"`` is more convenient than explicitly listing
  terms to ignore in a set.
numpydoc_validation_checks : set
    The set of validation checks to report during the sphinx build process.
    The default is an empty set, so docstring validation is not run by
    default.
    If ``"all"`` is in the set, then the results of all of the
    :ref:`built-in validation checks <validation_checks>` are reported.
    If the set includes ``"all"`` and additional error codes, then all
    validation checks *except* the listed error codes will be run.
    If the set contains *only* individual error codes, then only those checks
    will be run.
    For example::

        # Report warnings for all validation checks
        numpydoc_validation_checks = {"all"}

        # Report warnings for all checks *except* for GL01, GL02, and GL05
        numpydoc_validation_checks = {"all", "GL01", "GL02", "GL05"}

        # Only report warnings for the SA01 and EX01 checks
        numpydoc_validation_checks = {"SA01", "EX01"}
numpydoc_validation_exclude : set
    A container of strings using :py:mod:`re` syntax specifying patterns to
    ignore for docstring validation.
    For example, to skip docstring validation for all objects in
    ``mypkg.mymodule``::

        numpydoc_validation_exclude = {"mypkg.mymodule."}

    If you wanted to also skip getter methods of ``MyClass``::

        numpydoc_validation_exclude = {r"mypkg\.mymodule\.", r"MyClass\.get$"}

    The default is an empty set meaning no objects are excluded from docstring
    validation.
    Only has an effect when docstring validation is activated, i.e.
    ``numpydoc_validation_checks`` is not an empty set.
