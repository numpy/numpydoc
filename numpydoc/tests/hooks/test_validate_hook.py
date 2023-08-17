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
        / "hooks"
        / "example_module.py"
    )
    return str(fullpath.relative_to(request.config.rootdir))


@pytest.mark.parametrize("config", [None, "fake_dir"])
def test_validate_hook(example_module, config, capsys):
    """Test that a file is correctly processed in the absence of config files."""

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | file                                      | item                                | check   | description                                        |
        +===========================================+=====================================+=========+====================================================+
        | numpydoc/tests/hooks/example_module.py:1  | example_module                      | EX01    | No examples section found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | ES01    | No extended summary found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | PR01    | Parameters {'name'} not documented                 |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | SA01    | See Also section not found                         |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | EX01    | No examples section found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:9  | example_module.MyClass              | ES01    | No extended summary found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:9  | example_module.MyClass              | SA01    | See Also section not found                         |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:9  | example_module.MyClass              | EX01    | No examples section found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:12 | example_module.MyClass.__init__     | GL08    | The object does not have a docstring               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | ES01    | No extended summary found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented             |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | SA01    | See Also section not found                         |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | EX01    | No examples section found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:28 | example_module.MyClass.process      | SS05    | Summary must start with infinitive verb, not third |
        |                                           |                                     |         | person (e.g. use "Generate" instead of             |
        |                                           |                                     |         | "Generates")                                       |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:28 | example_module.MyClass.process      | ES01    | No extended summary found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:28 | example_module.MyClass.process      | SA01    | See Also section not found                         |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:28 | example_module.MyClass.process      | EX01    | No examples section found                          |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:33 | example_module.NewClass             | GL08    | The object does not have a docstring               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        """
    )

    args = [example_module]
    if config:
        args.append(f"--{config=}")

    return_code = main(args)
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_with_ignore(example_module, capsys):
    """
    Test that a file is correctly processed in the absence of config files
    with command line ignore options.
    """

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | file                                      | item                                | check   | description                                        |
        +===========================================+=====================================+=========+====================================================+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | PR01    | Parameters {'name'} not documented                 |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:12 | example_module.MyClass.__init__     | GL08    | The object does not have a docstring               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented             |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:28 | example_module.MyClass.process      | SS05    | Summary must start with infinitive verb, not third |
        |                                           |                                     |         | person (e.g. use "Generate" instead of             |
        |                                           |                                     |         | "Generates")                                       |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        | numpydoc/tests/hooks/example_module.py:33 | example_module.NewClass             | GL08    | The object does not have a docstring               |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------------------+
        """
    )

    return_code = main([example_module, "--ignore", "ES01", "SA01", "EX01"])
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_with_toml_config(example_module, tmp_path, capsys):
    """
    Test that a file is correctly processed with the config coming from
    a pyproject.toml file.
    """

    with open(tmp_path / "pyproject.toml", "w") as config_file:
        config_file.write(
            inspect.cleandoc(
                """
                [tool.numpydoc_validation]
                checks = [
                    "all",
                    "EX01",
                    "SA01",
                    "ES01",
                ]
                exclude = '\\.__init__$'
                override_SS05 = [
                    '^Process',
                    '^Assess',
                    '^Access',
                ]
                """
            )
        )

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | file                                      | item                                | check   | description                            |
        +===========================================+=====================================+=========+========================================+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | PR01    | Parameters {'name'} not documented     |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description   |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:33 | example_module.NewClass             | GL08    | The object does not have a docstring   |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        """
    )

    return_code = main([example_module, "--config", str(tmp_path)])
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_with_setup_cfg(example_module, tmp_path, capsys):
    """
    Test that a file is correctly processed with the config coming from
    a setup.cfg file.
    """

    with open(tmp_path / "setup.cfg", "w") as config_file:
        config_file.write(
            inspect.cleandoc(
                """
                [tool:numpydoc_validation]
                checks = all,EX01,SA01,ES01
                exclude = \\.__init__$
                override_SS05 = ^Process,^Assess,^Access
                """
            )
        )

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | file                                      | item                                | check   | description                            |
        +===========================================+=====================================+=========+========================================+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | PR01    | Parameters {'name'} not documented     |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description   |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:33 | example_module.NewClass             | GL08    | The object does not have a docstring   |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        """
    )

    return_code = main([example_module, "--config", str(tmp_path)])
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_help(capsys):
    """Test that help section is displaying."""

    with pytest.raises(SystemExit):
        return_code = main(["--help"])
        assert return_code == 0

    out = capsys.readouterr().out
    assert "--ignore" in out
    assert "--config" in out


def test_validate_hook_exclude_option_pyproject(example_module, tmp_path, capsys):
    """
    Test that a file is correctly processed with the config coming from
    a pyproject.toml file and exclusions provided.
    """

    with open(tmp_path / "pyproject.toml", "w") as config_file:
        config_file.write(
            inspect.cleandoc(
                r"""
                [tool.numpydoc_validation]
                checks = [
                    "all",
                    "EX01",
                    "SA01",
                    "ES01",
                ]
                exclude = [
                    '\.do_something$',
                    '\.__init__$',
                ]
                override_SS05 = [
                    '^Process',
                    '^Assess',
                    '^Access',
                ]
                """
            )
        )

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+------------------------------+---------+--------------------------------------+
        | file                                      | item                         | check   | description                          |
        +===========================================+==============================+=========+======================================+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function | PR01    | Parameters {'name'} not documented   |
        +-------------------------------------------+------------------------------+---------+--------------------------------------+
        | numpydoc/tests/hooks/example_module.py:33 | example_module.NewClass      | GL08    | The object does not have a docstring |
        +-------------------------------------------+------------------------------+---------+--------------------------------------+
        """
    )

    return_code = main([example_module, "--config", str(tmp_path)])
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected


def test_validate_hook_exclude_option_setup_cfg(example_module, tmp_path, capsys):
    """
    Test that a file is correctly processed with the config coming from
    a setup.cfg file and exclusions provided.
    """

    with open(tmp_path / "setup.cfg", "w") as config_file:
        config_file.write(
            inspect.cleandoc(
                """
                [tool:numpydoc_validation]
                checks = all,EX01,SA01,ES01
                exclude = \\.NewClass$,\\.__init__$
                override_SS05 = ^Process,^Assess,^Access
                """
            )
        )

    expected = inspect.cleandoc(
        """
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | file                                      | item                                | check   | description                            |
        +===========================================+=====================================+=========+========================================+
        | numpydoc/tests/hooks/example_module.py:4  | example_module.some_function        | PR01    | Parameters {'name'} not documented     |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR01    | Parameters {'**kwargs'} not documented |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        | numpydoc/tests/hooks/example_module.py:18 | example_module.MyClass.do_something | PR07    | Parameter "*args" has no description   |
        +-------------------------------------------+-------------------------------------+---------+----------------------------------------+
        """
    )

    return_code = main([example_module, "--config", str(tmp_path)])
    assert return_code == 1
    assert capsys.readouterr().err.rstrip() == expected
