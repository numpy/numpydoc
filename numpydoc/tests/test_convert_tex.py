from __future__ import division, print_function, absolute_import

import nose
from nose.tools import assert_raises
from numpydoc.numpydoc import convert_tex


good_pairs = [
    ("",
     ""),

    ("a quick brown fox", 
     "a quick brown fox"),

    ("$a quick brown fox$", 
     ":math:`a quick brown fox`"),

    ("Let $x$ equal $2^{42}$",
     "Let :math:`x` equal :math:`2^{42}`"),

    ("$x$ being an unknown",
     ":math:`x` being an unknown"),

    (r"For $xi\to 0$, $\sin(1/\xi)$ is undefined",
     r"For :math:`xi\to 0`, :math:`\sin(1/\xi)` is undefined"),

    ("For $x\\to 0$, $\\sin(1/x)$ is undefined",
     "For :math:`x\\to 0`, :math:`\\sin(1/x)` is undefined"),
]


# these should fail loudly
bad_ones = [
    "$$",
    "$$sorry, no displaymath$$",
    "and $math$ better fit in one $line",
]


def test_bad():
    for line in bad_ones:
        yield assert_raises, ValueError, convert_tex, line


def test_good():
    for inp, outp in good_pairs:
        yield check_pair, inp, outp


def check_pair(inp, outp):
    assert convert_tex(inp) == outp


if __name__ == "__main__":
    nose.run()
