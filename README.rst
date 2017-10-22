.. image:: https://travis-ci.org/numpy/numpydoc.png?branch=master
   :target: https://travis-ci.org/numpy/numpydoc/

.. |docs| image:: https://readthedocs.org/projects/numpydoc/badge/?version=latest
   :alt: Documentation Status
   :scale: 100%
   :target: https://numpydoc.readthedocs.io/en/latest/?badge=latest


=====================================
numpydoc -- Numpy's Sphinx extensions
=====================================

Numpy's documentation uses several custom extensions to Sphinx.  These
are shipped in this ``numpydoc`` package, in case you want to make use
of them in third-party projects.

The ``numpydoc`` extension provides support for the Numpy docstring format in
Sphinx, and adds the code description directives ``np:function``,
``np-c:function``, etc.  that support the Numpy docstring syntax.

See `numpydoc docstring guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_
for how to write docs that use this extension, and the `user guide <https://numpydoc.readthedocs.io>`_

Numpydoc inserts a hook into Sphinx's autodoc that converts docstrings
following the Numpy/Scipy format to a form palatable to Sphinx.
