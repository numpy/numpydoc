import sys
import os

import setuptools  # may monkeypatch distutils in some versions. # noqa
from distutils.command.sdist import sdist
from distutils.core import setup

from numpydoc import __version__ as version

if sys.version_info < (3, 5):
    raise RuntimeError("Python version >= 3.5 required.")


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
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 ],
    keywords="sphinx numpy",
    author="Pauli Virtanen and others",
    author_email="pav@iki.fi",
    url="https://numpydoc.readthedocs.io",
    license="BSD",
    install_requires=["sphinx >= 1.6.5", 'Jinja2>=2.3'],
    python_requires=">=3.5",
    extras_require={
        "testing": [
            req for req in read('test_requirements.txt').split('\n')
            if not req.startswith('#')
        ],
    },
    package_data={'numpydoc': [
        'tests/test_*.py',
        'tests/tinybuild/Makefile',
        'tests/tinybuild/index.rst',
        'tests/tinybuild/*.py',
        'templates/*.rst',
        ]},
    cmdclass={"sdist": sdist},
)
