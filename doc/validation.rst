==============================
Validating NumpyDoc docstrings
==============================

To see the Restructured Text generated for an object, the ``numpydoc`` module
can be called. For example, to do it for ``numpy.ndarray``, use:

.. code-block:: bash

    $ python -m numpydoc numpy.ndarray

This will validate that the docstring can be built.

For an exhaustive validation of the formatting of the docstring, use the
``--validate`` parameter. This will report the errors detected, such as
incorrect capitalization, wrong order of the sections, and many other
issues.
