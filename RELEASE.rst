Release process for ``numpydoc``
================================

Introduction
------------

Example ``__version__``

- 1.8.dev0     # development version of 1.8 (release candidate 1)
- 1.8rc1       # 1.8 release candidate 1
- 1.8rc2.dev0  # development version of 1.8 (release candidate 2)
- 1.8          # 1.8 release
- 1.9.dev0     # development version of 1.9 (release candidate 1)

Test release candidates on numpy, scipy, matplotlib, scikit-image, and networkx.

Process
-------

- Review and update ``doc/release_notes.rst``.

- Update ``__version__`` in ``numpydoc/_version.py``.

- Commit changes::

    git add numpydoc/_version.py doc/release_notes.rst
    git commit -m 'Designate <version> release'

- Add the version number (e.g., `v1.2.0`) as a tag in git::

    git tag -s [-u <key-id>] v<version> -m 'signed <version> tag'

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github::

    git push --tags origin main

  where ``origin`` is the name of the ``github.com:numpy/numpydoc`` repository

- Review the github release page::

    https://github.com/numpy/numpydoc/releases

- Publish on PyPi::

    git clean -fxd
    pip install build wheel twine
    python -m build --sdist --wheel
    twine upload -s dist/*

- Update ``__version__`` in ``numpydoc/_version.py``.

- Commit changes::

    git add numpydoc/_version.py
    git commit -m 'Bump version'
    git push origin main
