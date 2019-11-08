"""
This package provides the numpydoc Sphinx extension for handling docstrings
formatted according to the NumPy documentation format.
"""
__version__ = '1.0.0.dev0'


def setup(app, *args, **kwargs):
    from .numpydoc import setup
    return setup(app, *args, **kwargs)
