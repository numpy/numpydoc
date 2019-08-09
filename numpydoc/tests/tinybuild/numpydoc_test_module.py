"""Numpydoc test module.

.. currentmodule:: numpydoc_test_module

.. autosummary::
   :toctree: generated/

   MyClass
   my_function
"""

__all__ = ['MyClass', 'my_function']


class MyClass(object):
    """A class.

    Parameters
    ----------
    *args : iterable
        Arguments.
    **kwargs : dict
        Keyword arguments.
    """

    def __init__(self, *args, **kwargs):
        pass


def my_function(*args, **kwargs):
    """Return None.

    See [1]_.

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
    .. [1] https://numpydoc.readthedocs.io
    """
    return None
