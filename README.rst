.. image:: https://travis-ci.org/numpy/numpydoc.png?branch=master
   :target: https://travis-ci.org/numpy/numpydoc/

=====================================
numpydoc -- Numpy's Sphinx extensions
=====================================

Numpy's documentation uses several custom extensions to Sphinx.  These
are shipped in this ``numpydoc`` package, in case you want to make use
of them in third-party projects.

The following extensions are available:

  - ``numpydoc``: support for the Numpy docstring format in Sphinx, and add
    the code description directives ``np:function``, ``np-c:function``, etc.
    that support the Numpy docstring syntax.

  - ``numpydoc.traitsdoc``: For gathering documentation about Traits attributes.

  - ``numpydoc.plot_directive``: Adaptation of Matplotlib's ``plot::``
    directive. Note that this implementation may still undergo severe
    changes or eventually be deprecated.

See `A Guide to NumPy/SciPy Documentation <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_
for how to write docs that use this extension.


numpydoc
========

Numpydoc inserts a hook into Sphinx's autodoc that converts docstrings
following the Numpy/Scipy format to a form palatable to Sphinx.

Options
-------

The following options can be set in conf.py:

- numpydoc_use_plots: bool

  Whether to produce ``plot::`` directives for Examples sections that
  match `numpydoc_plot_examples_re`.

- numpydoc_plot_examples_re : str

  The regular expression used to match Examples sections containing plots.
  ``'import matplotlib'`` by default.

- numpydoc_show_class_members: bool

  Whether to show all members of a class in the Methods and Attributes
  sections automatically.
  ``True`` by default.

- numpydoc_show_inherited_class_members: bool

  Whether to show all inherited members of a class in the Methods and Attributes
  sections automatically. If it's false, inherited members won't shown.
  ``True`` by default.

- numpydoc_class_members_toctree: bool

  Whether to create a Sphinx table of contents for the lists of class
  methods and attributes. If a table of contents is made, Sphinx expects
  each entry to have a separate page.
  ``True`` by default.

- numpydoc_edit_link: bool  (DEPRECATED -- edit your HTML template instead)

  Whether to insert an edit link after docstrings.
