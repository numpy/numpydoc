# -*- encoding:utf-8 -*-
from __future__ import division, absolute_import, print_function

from nose.tools import assert_equal
from numpydoc.xref import make_xref_param_type

xref_aliases = {
    # python
    'sequence': ':term:`python:sequence`',
    'iterable': ':term:`python:iterable`',
    'string': 'str',
    # numpy
    'array': '~numpy.array',
    'dtype': 'numpy.dtype',
    'ndarray': '~numpy.ndarray',
    'matrix': 'numpy.matrix',
    'array-like': ':term:`numpy:array_like`',
    'array_like': ':term:`numpy:array_like`',
}

# Comes mainly from numpy
data = """
(...) array_like, float, optional
(...) :term:`numpy:array_like`, :xref_param_type:`float`, optional

(2,) ndarray
(2,) :xref_param_type:`~numpy.ndarray`

(...,M,N) array_like
(...,M,N) :term:`numpy:array_like`

(float, float), optional
(:xref_param_type:`float`, :xref_param_type:`float`), optional

1-D array or sequence
1-D :xref_param_type:`~numpy.array` or :term:`python:sequence`

array of str or unicode-like
:xref_param_type:`~numpy.array` of :xref_param_type:`str` or unicode-like

array_like of float
:term:`numpy:array_like` of :xref_param_type:`float`

bool or callable
:xref_param_type:`bool` or :xref_param_type:`callable`

int in [0, 255]
:xref_param_type:`int` in [0, 255]

int or None, optional
:xref_param_type:`int` or :xref_param_type:`None`, optional

list of str or array_like
:xref_param_type:`list` of :xref_param_type:`str` or :term:`numpy:array_like`

sequence of array_like
:term:`python:sequence` of :term:`numpy:array_like`

str or pathlib.Path
:xref_param_type:`str` or :xref_param_type:`pathlib.Path`

{'', string}, optional
{'', :xref_param_type:`str`}, optional

{'C', 'F', 'A', or 'K'}, optional
{'C', 'F', 'A', or 'K'}, optional

{'linear', 'lower', 'higher', 'midpoint', 'nearest'}
{'linear', 'lower', 'higher', 'midpoint', 'nearest'}

{False, True, 'greedy', 'optimal'}
{:xref_param_type:`False`, :xref_param_type:`True`, 'greedy', 'optimal'}

{{'begin', 1}, {'end', 0}}, {string, int}
{{'begin', 1}, {'end', 0}}, {string, :xref_param_type:`int`}

callable f'(x,*args)
:xref_param_type:`callable` f'(x,*args)

callable ``fhess(x, *args)``, optional
:xref_param_type:`callable` ``fhess(x, *args)``, optional

spmatrix (format: ``csr``, ``bsr``, ``dia`` or coo``)
:xref_param_type:`spmatrix` (format: ``csr``, ``bsr``, ``dia`` or coo``)

list(int)
:xref_param_type:`list`(:xref_param_type:`int`)

list[int]
:xref_param_type:`list`[:xref_param_type:`int`]

dict(str, int)
:xref_param_type:`dict`(:xref_param_type:`str`, :xref_param_type:`int`)

dict[str,  int]
:xref_param_type:`dict`[:xref_param_type:`str`,  :xref_param_type:`int`]

tuple(float, float)
:xref_param_type:`tuple`(:xref_param_type:`float`, :xref_param_type:`float`)

dict[tuple(str, str), int]
:xref_param_type:`dict`[:xref_param_type:`tuple`(:xref_param_type:`str`, :xref_param_type:`str`), :xref_param_type:`int`]
"""  # noqa: E501


def test_make_xref_param_type():
    for s in data.strip().split('\n\n'):
        param_type, expected_result = s.split('\n')
        result = make_xref_param_type(param_type, xref_aliases)
        assert_equal(result, expected_result)
