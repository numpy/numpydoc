"""
This package provides the numpydoc Sphinx extension for handling docstrings
formatted according to the NumPy documentation format.
"""

from ._version import __version__


# NOTE: Determine whether sphinx is installed with an explicit import.
# If so, define the setup function for registering the numpydoc extension;
# otherwise skip this step.
try:
    import sphinx


    def setup(app, *args, **kwargs):
        from .numpydoc import setup

        return setup(app, *args, **kwargs)
except ModuleNotFoundError:
    pass
