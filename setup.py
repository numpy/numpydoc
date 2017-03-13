from __future__ import division, print_function

import sys

from distutils.command.sdist import sdist
import setuptools
from distutils.core import setup

if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[0:2] < (3, 4):
    raise RuntimeError("Python version 2.7 or >= 3.4 required.")

with open('numpydoc/__init__.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(
    name="numpydoc",
    packages=["numpydoc"],
    version=version,
    description="Sphinx extension to support docstrings in Numpy format",
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
    url="https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt",
    license="BSD",
    install_requires=["sphinx >= 1.2.3", 'Jinja2>=2.3'],
    package_data={'numpydoc': ['tests/test_*.py', 'templates/*.rst']},
    test_suite = 'nose.collector',
    cmdclass={"sdist": sdist},
)
