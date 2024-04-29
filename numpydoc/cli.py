"""The CLI for numpydoc."""

import argparse
import ast
from typing import List, Sequence, Union

from .docscrape_sphinx import get_doc_object
from .hooks import validate_docstrings
from .validate import Validator, validate


def render_object(import_path: str, config: Union[List[str], None] = None) -> int:
    """Test numpydoc docstring generation for a given object."""
    # TODO: Move Validator._load_obj to a better place than validate
    print(get_doc_object(Validator._load_obj(import_path), config=dict(config or [])))
    return 0


def validate_object(import_path: str) -> int:
    """Run numpydoc docstring validation for a given object."""
    exit_status = 0
    results = validate(import_path)
    for err_code, err_desc in results["errors"]:
        exit_status += 1
        print(":".join([import_path, err_code, err_desc]))
    return exit_status


def main(argv: Union[Sequence[str], None] = None) -> int:
    """CLI for numpydoc."""
    ap = argparse.ArgumentParser(prog="numpydoc", description=__doc__)
    subparsers = ap.add_subparsers(title="subcommands")

    def _parse_config(s):
        key, _, value = s.partition("=")
        value = ast.literal_eval(value)
        return key, value

    render = subparsers.add_parser(
        "render",
        description="Test numpydoc docstring generation for a given object.",
        help="generate the docstring with numpydoc",
    )
    render.add_argument("import_path", help="e.g. numpy.ndarray")
    render.add_argument(
        "-c",
        "--config",
        type=_parse_config,
        action="append",
        help="key=val where val will be parsed by literal_eval, "
        "e.g. -c use_plots=True. Multiple -c can be used.",
    )
    render.set_defaults(func=render_object)

    validate = subparsers.add_parser(
        "validate",
        description="Validate the docstring with numpydoc.",
        help="validate the object and report errors",
    )
    validate.add_argument("import_path", help="e.g. numpy.ndarray")
    validate.set_defaults(func=validate_object)

    lint_parser = validate_docstrings.get_parser(parent=subparsers)
    lint_parser.set_defaults(func=validate_docstrings.run_hook)

    args = vars(ap.parse_args(argv))
    try:
        func = args.pop("func")
        return func(**args)
    except KeyError:
        ap.exit(status=2, message=ap.format_help())
