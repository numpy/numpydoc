==========
Validation
==========

.. _pre_commit_hook:

Docstring Validation using Pre-Commit Hook
------------------------------------------

To enable validation of docstrings as you commit files, add the
following to your ``.pre-commit-config.yaml`` file:

.. code-block:: yaml

    - repo: https://github.com/numpy/numpydoc
      rev: <version>
      hooks:
        - id: numpydoc-validation

After installing ``numpydoc``, run the following to see available
command line options for this hook:

.. code-block:: bash

    $ python -m numpydoc.hooks.validate_docstrings --help

Using a config file provides additional customization. Both ``pyproject.toml``
and ``setup.cfg`` are supported; however, if the project contains both
you must use the ``pyproject.toml`` file. The example below configures
the pre-commit hook as follows:

* ``checks``: Report findings on all checks except ``EX01``, ``SA01``, and
  ``ES01`` (using the same logic as the :ref:`validation during Sphinx build
  <validation_during_sphinx_build>` for ``numpydoc_validation_checks``).
* ``exclude``: Don't report issues on objects matching any of the regular
  regular expressions ``\.undocumented_method$`` or ``\.__repr__$``. This
  maps to ``numpydoc_validation_exclude`` from the
  :ref:`Sphinx build configuration <validation_during_sphinx_build>`.
* ``override_SS05``: Allow docstrings to start with "Process ", "Assess ",
  or "Access ". To override different checks, add a field for each code in
  the form of ``override_<code>`` with a collection of regular expression(s)
  to search for in the contents of a docstring, not the object name. This
  maps to ``numpydoc_validation_overrides`` from the
  :ref:`Sphinx build configuration <validation_during_sphinx_build>`.

``pyproject.toml``::

    [tool.numpydoc_validation]
    checks = [
        "all",   # report on all checks, except the below
        "EX01",
        "SA01",
        "ES01",
    ]
    exclude = [  # don't report on objects that match any of these regex
        '\.undocumented_method$',
        '\.__repr__$',
    ]
    override_SS05 = [  # override SS05 to allow docstrings starting with these words
        '^Process ',
        '^Assess ',
        '^Access ',
    ]

``setup.cfg``::

    [tool:numpydoc_validation]
    checks = all,EX01,SA01,ES01
    exclude = \.undocumented_method$,\.__repr__$
    override_SS05 = ^Process ,^Assess ,^Access ,

In addition to the above, :ref:`inline ignore comments <inline_ignore_comments>`
can be used to ignore findings on a case by case basis.

If any issues are found when committing, a report is printed out, and the
commit is halted:

.. code-block:: output

    numpydoc-validation......................................................Failed
    - hook id: numpydoc-validation
    - exit code: 1

    +----------------------+----------------------+---------+--------------------------------------+
    | file                 | item                 | check   | description                          |
    +======================+======================+=========+======================================+
    | src/pkg/utils.py:1   | utils                | GL08    | The object does not have a docstring |
    | src/pkg/utils.py:90  | utils.normalize      | PR04    | Parameter "field" has no type        |
    | src/pkg/module.py:12 | module.MyClass       | GL08    | The object does not have a docstring |
    | src/pkg/module.py:33 | module.MyClass.parse | RT03    | Return value has no description      |
    +----------------------+----------------------+---------+--------------------------------------+

See :ref:`below <validation_checks>` for a full listing of checks.

.. _validation_via_cli:

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
issues. Note that this will honor :ref:`inline ignore comments <inline_ignore_comments>`,
but will not look for any configuration like the :ref:`pre-commit hook <pre_commit_hook>`
or :ref:`Sphinx extension <validation_during_sphinx_build>` do.

.. _validation_during_sphinx_build:

Docstring Validation during Sphinx Build
----------------------------------------

It is also possible to run docstring validation as part of the Sphinx build
process.
This behavior is controlled by the ``numpydoc_validation_checks`` configuration
parameter in ``conf.py``.
For example, to verify that all of the parameters in the function signature
are accounted for in the ``Parameters`` section of the docstring, add the
following line to ``conf.py``::

    numpydoc_validation_checks = {"PR01"}

This will cause a Sphinx warning to be raised for any (non-module) docstring
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

In addition, you can exclude any findings on certain objects with
``numpydoc_validation_exclude``, which maps to ``exclude`` in the
:ref:`pre-commit hook setup <pre_commit_hook>`::

    # don't report on objects that match any of these regex
    numpydoc_validation_exclude = [
        '\.undocumented_method$',
        '\.__repr__$',
    ]

Overrides based on docstring contents are also supported, but the structure
is slightly different than the :ref:`pre-commit hook setup <pre_commit_hook>`::

    numpydoc_validation_overrides = {
        "SS02": [  # override SS05 to allow docstrings starting with these words
            '^Process ',
            '^Assess ',
            '^Access ',
        ]
    }

.. _inline_ignore_comments:

Ignoring Validation Checks with Inline Comments
-----------------------------------------------

Sometimes you only want to ignore a specific check or set of checks for a
specific piece of code. This level of fine-tuned control is provided via
inline comments:

.. code-block:: python

    class SomeClass:  # numpydoc ignore=EX01,SA01,ES01
        """This is the docstring for SomeClass."""

        def __init__(self):  # numpydoc ignore=GL08
            pass

This is supported by the :ref:`CLI <validation_via_cli>`,
:ref:`pre-commit hook <pre_commit_hook>`, and
:ref:`Sphinx extension <validation_during_sphinx_build>`.

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
