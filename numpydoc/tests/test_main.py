from __future__ import print_function

from contextlib import contextmanager
import os
import sys
import tempfile
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from numpydoc.__main__ import main


PACKAGE_CODE = """
'''This package has test stuff'''
"""

MODULE_CODE = """
'''This module has test stuff'''

def foo(a, b=5):
    '''Hello world

    Parameters
    ----------
    something : foo
        bar
    something_else
        bar
    '''
"""


@contextmanager
def _mock_module(pkg_name):
    try:
        tempdir = tempfile.mkdtemp()
        os.mkdir(os.path.join(tempdir, pkg_name))
        with open(os.path.join(tempdir, pkg_name, '__init__.py'), 'w') as f:
            print(PACKAGE_CODE, file=f)
        with open(os.path.join(tempdir, pkg_name, 'module.py'), 'w') as f:
            print(MODULE_CODE, file=f)

        sys.path.insert(0, tempdir)
        yield tempdir
    finally:
        try:
            os.path.rmdir(tempdir)
            sys.path.remove(tempdir)
        except:
            pass


def _capture_main(*args):
    f = StringIO()
    sys.stdout, old_stdout = f, sys.stdout
    try:
        main(args)
        return f.getvalue().strip('\n\r')
    finally:
        sys.stdout = old_stdout


def test_main():
    # TODO: does not currently check that numpydoc transformations are applied

    assert (_capture_main('numpydoc.__main__.main') ==
            main.__doc__.strip())

    # check it works with modules not imported from __init__
    with _mock_module('somepackage1'):
        out = _capture_main('somepackage1.module.foo')
    assert out.startswith('Hello world\n')
    with _mock_module('somepackage2'):
        out = _capture_main('somepackage2.module')
    assert out.startswith('This module has test')
    with _mock_module('somepackage3'):
        out = _capture_main('somepackage3')
    assert out.startswith('This package has test')
