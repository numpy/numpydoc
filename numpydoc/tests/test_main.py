from numpydoc.__main__ import main

import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def test_main():
    f = StringIO()
    sys.stdout, old_stdout = f, sys.stdout
    main(['numpydoc.__main__.main'])
    assert f.getvalue().strip() == main.__doc__
    sys.stdout = old_stdout
