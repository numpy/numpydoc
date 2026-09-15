"""
This package provides the numpydoc Sphinx extension for handling docstrings
formatted according to the NumPy documentation format.
"""

from importlib.metadata import version

__version__ = version("numpydoc")
del version


def setup(app, *args, **kwargs):
    from .numpydoc import setup

    return setup(app, *args, **kwargs)
