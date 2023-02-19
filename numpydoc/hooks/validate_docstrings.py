"""Run numpydoc validation on contents of a file."""

import argparse
import ast
import configparser
import os
import sys
from pathlib import Path

from tabulate import tabulate

from .. import docscrape, validate


class AstValidator(validate.Validator):
    """
    Overrides the :class:`Validator` to work entirely with the AST.

    Parameters
    ----------
    ast_node : ast.AST
        The node under inspection.
    filename : path-like
        The file where the node is defined.
    obj_name : str
        A name for the node to use in the listing of issues for the file as a whole.
    """

    def __init__(self, *, ast_node, filename, obj_name):
        self.node = ast_node
        self.raw_doc = ast.get_docstring(self.node, clean=False) or ""
        self.clean_doc = ast.get_docstring(self.node, clean=True)
        self.doc = docscrape.NumpyDocString(self.raw_doc)

        self._source_file = os.path.abspath(filename)
        self._name = obj_name

        self.is_class = isinstance(ast_node, ast.ClassDef)
        self.is_module = isinstance(ast_node, ast.Module)

    @staticmethod
    def _load_obj(name):
        raise NotImplementedError("AstValidator does not support this method.")

    @property
    def name(self):
        return self._name

    @property
    def is_function_or_method(self):
        return isinstance(self.node, (ast.FunctionDef, ast.AsyncFunctionDef))

    @property
    def is_generator_function(self):
        if not self.is_function_or_method:
            return False
        for child in ast.iter_child_nodes(self.node):
            if isinstance(child, ast.Expr) and isinstance(child.value, ast.Yield):
                return True
        return False

    @property
    def type(self):
        if self.is_function_or_method:
            return "function"
        if self.is_class:
            return "type"
        if self.is_module:
            return "module"
        raise ValueError("Unknown type.")

    @property
    def source_file_name(self):
        return self._source_file

    @property
    def source_file_def_line(self):
        return self.node.lineno if not self.is_module else 0

    @property
    def signature_parameters(self):
        def extract_signature(node):
            args_node = node.args
            params = []
            for arg_type in ["posonlyargs", "args", "vararg", "kwonlyargs", "kwarg"]:
                entries = getattr(args_node, arg_type)
                if arg_type in ["vararg", "kwarg"]:
                    if entries and arg_type == "vararg":
                        params.append(f"*{entries}")
                    if entries and arg_type == "kwarg":
                        params.append(f"**{entries}")
                else:
                    params.extend([arg.arg for arg in entries])
            params = tuple(params)
            if params and params[0] in {"self", "cls"}:
                return params[1:]
            return params

        params = tuple()
        if self.is_function_or_method:
            params = extract_signature(self.node)
        elif self.is_class:
            for child in self.node.body:
                if isinstance(child, ast.FunctionDef) and child.name == "__init__":
                    params = extract_signature(child)
        return params

    @property
    def method_source(self):
        with open(self.source_file_name) as file:
            source = ast.get_source_segment(file.read(), self.node)
        return source


class DocstringVisitor(ast.NodeVisitor):
    """
    Visits nodes in the AST from a given module and reporting numpydoc issues.

    Parameters
    ----------
    filepath : path-like
        The absolute or relative path to the file to inspect.
    ignore : list[str]
        A list of check codes to ignore, if desired.
    """

    def __init__(self, filepath, ignore):
        self.findings = []
        self.parent = None
        self.filepath = filepath.replace("../", "")
        self.name = self.filepath.replace("/", ".").replace(".py", "")
        self.ignore = ignore

    def _get_numpydoc_issues(self, name, node):
        """
        Get numpydoc validation issues.

        Parameters
        ----------
        name : str
            The full name of the node under inspection.
        node : ast.AST
            The node under inspection.
        """
        report = validate.validate(
            name, AstValidator, ast_node=node, filename=self.filepath
        )
        self.findings.extend(
            [
                [name, check, description]
                for check, description in report["errors"]
                if check not in self.ignore
            ]
        )

    def visit(self, node):
        """
        Visit a node in the AST and report on numpydoc validation issues.

        Parameters
        ----------
        node : ast.AST
            The node to visit.
        """
        if isinstance(node, ast.Module):
            self._get_numpydoc_issues(self.name, node)
            self.parent = self.name
            self.generic_visit(node)

        elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            node_name = f"{self.parent}.{node.name}"
            self._get_numpydoc_issues(node_name, node)
            if isinstance(node, ast.ClassDef):
                self.parent = node_name
            self.generic_visit(node)


def parse_config():
    """
    Parse config information from setup.cfg, if present.

    Returns
    -------
    dict
        Config options for the numpydoc validation hook.
    """
    filename = "setup.cfg"
    options = {"exclusions": []}
    config = configparser.ConfigParser()
    if Path(filename).exists():
        config.read(filename)
        numpydoc_validation_config_section = "tool:numpydoc_validation"
        try:
            try:
                options["exclusions"] = config.get(
                    numpydoc_validation_config_section, "ignore"
                ).split(",")
            except configparser.NoOptionError:
                pass
        except configparser.NoSectionError:
            pass
    return options


def process_file(filepath, ignore):
    """
    Run numpydoc validation on a file.

    Parameters
    ----------
    filepath : path-like
        The absolute or relative path to the file to inspect.
    ignore : list[str]
        A list of check codes to ignore, if desired.

    Returns
    -------
    dict
        Config options for the numpydoc validation hook.
    """
    with open(filepath) as file:
        module_node = ast.parse(file.read(), filepath)

    docstring_visitor = DocstringVisitor(filepath=filepath, ignore=ignore)
    docstring_visitor.visit(module_node)

    return docstring_visitor.findings


def main(argv=None):
    """Run the numpydoc validation hook."""

    config_options = parse_config()
    ignored_checks = (
        "\n  "
        + "\n  ".join(
            [
                f"- {check}: {validate.ERROR_MSGS[check]}"
                for check in config_options["exclusions"]
            ]
        )
        + "\n"
    )

    parser = argparse.ArgumentParser(
        description="Run numpydoc validation on files with option to ignore individual checks.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "files", type=str, nargs="+", help="File(s) to run numpydoc validation on."
    )
    parser.add_argument(
        "--ignore",
        type=str,
        nargs="*",
        help=(
            f"""Check codes to ignore.{
                ' Currently ignoring the following from setup.cfg:'
                f'{ignored_checks}'
                'Values provided here will be in addition to the above.'
                if config_options["exclusions"] else ''
            }"""
        ),
    )

    args = parser.parse_args(argv)

    ignore = config_options["exclusions"] + (args.ignore or [])
    findings = []
    for file in args.files:
        findings.extend(process_file(file, ignore))

    if findings:
        print(
            tabulate(
                findings,
                headers=["item", "check", "description"],
                tablefmt="grid",
                maxcolwidths=80,
            ),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
