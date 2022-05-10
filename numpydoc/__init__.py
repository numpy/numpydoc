"""
This package provides the numpydoc Sphinx extension for handling docstrings
formatted according to the NumPy documentation format.
"""
from ._version import __version__


def _verify_sphinx_jinja():
    """Ensure sphinx and jinja versions are compatible.

    Jinja2>=3.1 requires Sphinx>=4.0.2. Raises exception if this condition is
    not met.

    TODO: This check can be removed when the minimum supported sphinx version
    for numpydoc sphinx>=4.0.2
    """
    import sphinx, jinja2
    from packaging import version

    if version.parse(sphinx.__version__) <= version.parse("4.0.2"):
        if version.parse(jinja2.__version__) >= version.parse("3.1"):
            from sphinx.errors import VersionRequirementError

            raise VersionRequirementError(
                "\n\nSphinx<4.0.2 is incompatible with Jinja2>=3.1.\n"
                "If you wish to continue using sphinx<4.0.2 you need to pin "
                "Jinja2<3.1."
            )


_verify_sphinx_jinja()


def setup(app, *args, **kwargs):
    from .numpydoc import setup

    return setup(app, *args, **kwargs)
