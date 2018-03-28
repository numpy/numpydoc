==============================
Validating NumpyDoc docstrings
==============================

One tool for validating docstrings is to see how an object's dosctring
translates to Restructured Text.  Using numpydoc as a command-line tool
facilitates this. For example to see the Restructured Text generated
for ``numpy.ndarray``, use:

.. code-block:: bash

    $ python -m numpydoc numpy.ndarray
