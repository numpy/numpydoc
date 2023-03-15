import sys
import os

from setuptools import setup

# Adapted from MNE-Python (BSD)
version = None
with open(os.path.join("numpydoc", "_version.py")) as fid:
    for line in (line.strip() for line in fid):
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break
if version is None:
    raise RuntimeError("Could not determine version")

if sys.version_info < (3, 7):
    raise RuntimeError("Python version >= 3.7 required.")


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
    long_description=read("README.rst"),
    # classifiers from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "License :: OSI Approved :: BSD License",
        "Topic :: Documentation",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="sphinx numpy",
    author="Pauli Virtanen and others",
    author_email="pav@iki.fi",
    url="https://numpydoc.readthedocs.io",
    license="BSD",
    install_requires=["sphinx>=4.2", "Jinja2>=2.10"],
    python_requires=">=3.7",
    extras_require={
        "testing": [
            req
            for req in read("requirements/test.txt").split("\n")
            if not req.startswith("#")
        ],
    },
    package_data={
        "numpydoc": [
            "tests/test_*.py",
            "tests/tinybuild/Makefile",
            "tests/tinybuild/index.rst",
            "tests/tinybuild/*.py",
            "templates/*.rst",
        ]
    },
)
