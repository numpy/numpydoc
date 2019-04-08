from __future__ import division, print_function

import sys
import os

import setuptools  # may monkeypatch distutils in some versions. # noqa
from distutils.command.sdist import sdist
from distutils.core import setup

from numpydoc import __version__ as version

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[0:2] < (3, 4):
    raise RuntimeError("Python version 2.7 or >= 3.4 required.")


def read(fname):
    """Utility function to get README.rst into long_description.

    ``long_description`` is what ends up on the PyPI front page.
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        contents = f.read()

    return contents


setup(
    name="numpydoc",
    packages=["numpydoc"],
    version=version,
    description="Sphinx extension to support docstrings in Numpy format",
    long_description=read('README.rst'),
    # classifiers from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Development Status :: 4 - Beta",
                 "Environment :: Plugins",
                 "License :: OSI Approved :: BSD License",
                 "Topic :: Documentation",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6"],
    keywords="sphinx numpy",
    author="Pauli Virtanen and others",
    author_email="pav@iki.fi",
    url="https://numpydoc.readthedocs.io",
    license="BSD",
    install_requires=["sphinx >= 1.2.3", 'Jinja2>=2.3'],
    package_data={'numpydoc': ['tests/test_*.py', 'templates/*.rst']},
    test_suite = 'nose.collector',
    cmdclass={"sdist": sdist},
)
