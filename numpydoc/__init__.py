"""
This package provides the numpydoc Sphinx extension for handling docstrings
formatted according to the NumPy documentation format.
"""

from ._version import __version__


def setup(app, *args, **kwargs):
    from .numpydoc import setup  # noqa: PLC0415

    return setup(app, *args, **kwargs)
