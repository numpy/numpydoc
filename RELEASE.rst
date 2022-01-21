Release process for ``numpydoc``
================================

- Review and update ``doc/release_notes.rst``.

- Update ``__version__`` in ``numpydoc/__init__.py``.

- Commit changes::

    git add numpydoc/__init__.py doc/release_notes.rst
    git commit -m 'Designate <version> release'

- Add the version number as a tag in git::

    git tag -s [-u <key-id>] numpydoc-<version> -m 'signed <version> tag'

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github::

    git push --tags origin main

  where ``origin`` is the name of the ``github.com:numpy/numpydoc`` repository

- Review the github release page::

    https://github.com/numpy/numpydoc/releases

- Publish on PyPi::

    git clean -fxd
    python setup.py sdist bdist_wheel
    twine upload -s dist/*

- Update ``__version__`` in ``numpydoc/__init__.py``.

- Commit changes::

    git add numpydoc/__init__.py
    git commit -m 'Bump version'
