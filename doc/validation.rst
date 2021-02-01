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

.. _validation_checks:

Built-in Validation Checks
--------------------------

The `~numpydoc.validation` module provides a mapping with all of the checks
that are run as part of the validation procedure.
The mapping is of the form: ``error_code : <explanation>`` where ``error_code``
provides a shorthand for the check being run, and ``<explanation>`` provides
a more detailed message. For example::

    "EX01" : "No examples section found"

The full mapping of validation checks is given below.

.. literalinclude:: ../numpydoc/validate.py
   :lines: 36-90
