"""Test the numpydoc validate pre-commit hook."""

import inspect
from pathlib import Path

import pytest

from numpydoc.hooks.validate_docstrings import main


@pytest.fixture
def example_module(request):
    fullpath = (
        Path(request.config.rootdir)
        / "numpydoc"
        / "tests"
        / "validate-hook"
        / "example_module.py"
    )
    return str(fullpath.relative_to(request.config.rootdir))


def test_validate_hook(example_module, capsys):
    """Test that a file is correctly processed in the absence of config files."""

    expected = inspect.cleandoc(
        """
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | file                                              | item                                | check   | description                            |
        +===================================================+=====================================+=========+========================================+
        | numpydoc/tests/validate-hook/example_module.py:1  | example_module                      | EX01    | No examples section found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:3  | example_module.some_function        | ES01    | No extended summary found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:3  | example_module.some_function        | PR01    | Parameters {'name'} not documented     |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:3  | example_module.some_function        | SA01    | See Also section not found             |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:3  | example_module.some_function        | EX01    | No examples section found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:7  | example_module.MyClass              | ES01    | No extended summary found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:7  | example_module.MyClass              | SA01    | See Also section not found             |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:7  | example_module.MyClass              | EX01    | No examples section found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:10 | example_module.MyClass.__init__     | GL08    | The object does not have a docstring   |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | ES01    | No extended summary found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description   |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | SA01    | See Also section not found             |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | EX01    | No examples section found              |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        """
    )

    main([example_module])
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_with_ignore(example_module, capsys):
    """
    Test that a file is correctly processed in the absence of config files
    with command line ignore options.
    """

    expected = inspect.cleandoc(
        """
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | file                                              | item                                | check   | description                            |
        +===================================================+=====================================+=========+========================================+
        | numpydoc/tests/validate-hook/example_module.py:3  | example_module.some_function        | PR01    | Parameters {'name'} not documented     |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:10 | example_module.MyClass.__init__     | GL08    | The object does not have a docstring   |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/validate-hook/example_module.py:16 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description   |
        +---------------------------------------------------+-------------------------------------+---------+----------------------------------------+
        """
    )

    main([example_module, "--ignore", "ES01", "SA01", "EX01"])
    assert capsys.readouterr().err.rstrip() == expected
