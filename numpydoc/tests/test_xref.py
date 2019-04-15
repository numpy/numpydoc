# -*- encoding:utf-8 -*-
from __future__ import division, absolute_import, print_function

from numpydoc.xref import make_xref

xref_aliases = {
    # python
    'sequence': ':term:`python:sequence`',
    'iterable': ':term:`python:iterable`',
    'string': 'str',
    # numpy
    'array': 'numpy.ndarray',
    'dtype': 'numpy.dtype',
    'ndarray': 'numpy.ndarray',
    'matrix': 'numpy.matrix',
    'array-like': ':term:`numpy:array_like`',
    'array_like': ':term:`numpy:array_like`',
}

# Comes mainly from numpy
data = r"""
(...) array_like, float, optional
(...) :term:`numpy:array_like`, :obj:`float`, optional

(2,) ndarray
(2,) :obj:`ndarray <numpy.ndarray>`

(...,M,N) array_like
(...,M,N) :term:`numpy:array_like`

(..., M, N) array_like
(..., :obj:`M`, :obj:`N`) :term:`numpy:array_like`

(float, float), optional
(:obj:`float`, :obj:`float`), optional

1-D array or sequence
1-D :obj:`array <numpy.ndarray>` or :term:`python:sequence`

array of str or unicode-like
:obj:`array <numpy.ndarray>` of :obj:`str` or unicode-like

array_like of float
:term:`numpy:array_like` of :obj:`float`

bool or callable
:obj:`bool` or :obj:`callable`

int in [0, 255]
:obj:`int` in [0, 255]

int or None, optional
:obj:`int` or :obj:`None`, optional

list of str or array_like
:obj:`list` of :obj:`str` or :term:`numpy:array_like`

sequence of array_like
:term:`python:sequence` of :term:`numpy:array_like`

str or pathlib.Path
:obj:`str` or :obj:`pathlib.Path`

{'', string}, optional
{'', :obj:`string <str>`}, optional

{'C', 'F', 'A', or 'K'}, optional
{'C', 'F', 'A', or 'K'}, optional

{'linear', 'lower', 'higher', 'midpoint', 'nearest'}
{'linear', 'lower', 'higher', 'midpoint', 'nearest'}

{False, True, 'greedy', 'optimal'}
{:obj:`False`, :obj:`True`, 'greedy', 'optimal'}

{{'begin', 1}, {'end', 0}}, {string, int}
{{'begin', 1}, {'end', 0}}, {:obj:`string <str>`, :obj:`int`}

callable f'(x,*args)
:obj:`callable` f'(x,*args)

callable ``fhess(x, *args)``, optional
:obj:`callable` ``fhess(x, *args)``, optional

spmatrix (format: ``csr``, ``bsr``, ``dia`` or coo``)
:obj:`spmatrix` (format: ``csr``, ``bsr``, ``dia`` or coo``)

:ref:`strftime <strftime-strptime-behavior>`
:ref:`strftime <strftime-strptime-behavior>`

callable or :ref:`strftime <strftime-strptime-behavior>`
:obj:`callable` or :ref:`strftime <strftime-strptime-behavior>`

callable or :ref:`strftime behavior <strftime-strptime-behavior>`
:obj:`callable` or :ref:`strftime behavior <strftime-strptime-behavior>`

list(int)
:obj:`list`\(:obj:`int`)

list[int]
:obj:`list`\[:obj:`int`]

dict(str, int)
:obj:`dict`\(:obj:`str`, :obj:`int`)

dict[str,  int]
:obj:`dict`\[:obj:`str`,  :obj:`int`]

tuple(float, float)
:obj:`tuple`\(:obj:`float`, :obj:`float`)

dict[tuple(str, str), int]
:obj:`dict`\[:obj:`tuple`\(:obj:`str`, :obj:`str`), :obj:`int`]
"""  # noqa: E501

xref_ignore = {'or', 'in', 'of', 'default', 'optional'}


def test_make_xref():
    for s in data.strip().split('\n\n'):
        param_type, expected_result = s.split('\n')
        result = make_xref(
            param_type,
            xref_aliases,
            xref_ignore
        )
        assert result == expected_result
