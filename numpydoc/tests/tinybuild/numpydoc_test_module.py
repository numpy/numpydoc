"""Numpydoc test module.

.. currentmodule:: numpydoc_test_module

.. autosummary::
   :toctree: generated/

   MyClass
   my_function

Reference [1]_

References
----------
.. [1] https://numpydoc.readthedocs.io
"""

__all__ = ['MyClass', 'my_function']


class _MyBaseClass(object):

    def inherited(self):
        """Inherit a method."""
        pass


class MyClass(_MyBaseClass):
    """A class.

    Reference [2]_

    Parameters
    ----------
    *args : iterable
        Arguments.
    **kwargs : dict
        Keyword arguments.

    References
    ----------
    .. [2] https://numpydoc.readthedocs.io
    """

    def __init__(self, *args, **kwargs):
        pass

    def example(self):
        """Example function."""
        pass


def my_function(*args, **kwargs):
    """Return None.

    See [3]_.

    Parameters
    ----------
    *args : iterable
        Arguments.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    out : None
        The output.

    References
    ----------
    .. [3] https://numpydoc.readthedocs.io
    """
    return None
