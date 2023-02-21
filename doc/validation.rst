==========
Validation
==========

Docstring Validation using Pre-Commit Hook
------------------------------------------

To enable validation of docstrings as you commit files, add the
following to your ``.pre-commit-config.yaml`` file::

    - repo: https://github.com/numpy/numpydoc
      rev: <version>
      hooks:
        - id: numpydoc-validation

After installing ``numpydoc``, run the following to see available
command line options for this hook:

.. code-block::

    $ python -m numpydoc.hooks.validate_docstrings --help

Using a ``setup.cfg`` file provides additional customization.
Options must be placed under the ``[tool:numpydoc_validation]`` section.
The example below configures the pre-commit hook to ignore three checks
and specifies exceptions to the checks ``SS05`` (allow docstrings to
start with "Process ", "Assess ", or "Access ") and ``GL08`` (allow
the class/method/function with name "__init__" to not have a docstring)::

    [tool:numpydoc_validation]
    ignore = EX01,SA01,ES01
    override_SS05 = ^((Process|Assess|Access) )
    override_GL08 = ^(__init__)$

If any issues are found when commiting, a report is printed out and the
commit is stopped::

    numpydoc-validation......................................................Failed
    - hook id: numpydoc-validation
    - exit code: 1

    +--------------------------+--------------------------+---------+--------------------------------------+
    | file                     | item                     | check   | description                          |
    +==========================+==========================+=========+======================================+
    | src/pkg/utils.py:1       | utils                    | GL08    | The object does not have a docstring |
    | src/pkg/utils.py:90      | utils.normalize          | PR04    | Parameter "field" has no type        |
    | src/pkg/module_one.py:12 | module_one.MyClass       | GL08    | The object does not have a docstring |
    | src/pkg/module_one.py:33 | module_one.MyClass.parse | RT03    | Return value has no description      |
    +--------------------------+--------------------------+---------+--------------------------------------+

See below for a full listing of checks.

Docstring Validation using Python
---------------------------------

To see the Restructured Text generated for an object, the ``numpydoc`` module
can be called. For example, to do it for ``numpy.ndarray``, use:

.. code-block:: bash

    $ python -m numpydoc numpy.ndarray

This will validate that the docstring can be built.

For an exhaustive validation of the formatting of the docstring, use the
``--validate`` parameter. This will report the errors detected, such as
incorrect capitalization, wrong order of the sections, and many other
issues.

Docstring Validation during Sphinx Build
----------------------------------------

It is also possible to run docstring validation as part of the sphinx build
process.
This behavior is controlled by the ``numpydoc_validation_checks`` configuration
parameter in ``conf.py``.
For example, to verify that all of the parameters in the function signature
are accounted for in the ``Parameters`` section of the docstring, add the
following line to ``conf.py``::

    numpydoc_validation_checks = {"PR01"}

This will cause a sphinx warning to be raised for any (non-module) docstring
that has undocumented parameters in the signature.
The full set of validation checks can be activated by::

    numpydoc_validation_checks = {"all"}

The complete validation suite contains :ref:`many checks <validation_checks>`
including some for style, capitalization, and grammar.
It is unlikely that reporting *all* validation warnings is desirable for
most use-cases.
Individual checks can be excluded by including them in the set with the
special keyword ``"all"``::

    # Report warnings for all validation checks except GL01, GL02, and GL05
    numpydoc_validation_checks = {"all", "GL01", "GL02", "GL05"}

.. _validation_checks:

Built-in Validation Checks
--------------------------

The ``numpydoc.validation`` module provides a mapping with all of the checks
that are run as part of the validation procedure.
The mapping is of the form: ``error_code : <explanation>`` where ``error_code``
provides a shorthand for the check being run, and ``<explanation>`` provides
a more detailed message. For example::

    "EX01" : "No examples section found"

The full mapping of validation checks is given below.

.. literalinclude:: ../numpydoc/validate.py
   :start-after: start-err-msg
   :end-before: end-err-msg
