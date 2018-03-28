from numpydoc.__main__ import main

import sys
import io


def test_main():
    f = io.StringIO()
    sys.stdout, old_stdout = f, sys.stdout
    main(['numpydoc.__main__.main'])
    assert f.getvalue().strip() == main.__doc__
    sys.stdout = old_stdout
