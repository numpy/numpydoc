Release process for ``numpydoc``
================================

Introduction
------------

Example ``__version__``

- 1.8rc0.dev0  # development version of 1.8 (first release candidate)
- 1.8rc0       # 1.8 release candidate 1
- 1.8rc1.dev0  # development version of 1.8 (second release candidate)
- 1.8          # 1.8 release
- 1.9rc0.dev0  # development version of 1.9 (first release candidate)

Test release candidates on numpy, scipy, matplotlib, scikit-image, and networkx.

Process
-------

- Set release variables::

   export VERSION=<version number>
   export PREVIOUS=<previous version number>
   export ORG="numpy"
   export REPO="numpydoc"
   export LOG="doc/release/notes.rst"

- Autogenerate release notes::

   changelist ${ORG}/${REPO} v${PREVIOUS} main --version ${VERSION} --config pyproject.toml --format rst --out ${VERSION}.rst
   changelist ${ORG}/${REPO} v${PREVIOUS} main --version ${VERSION} --config pyproject.toml --out ${VERSION}.md
   cat ${VERSION}.rst | cat - ${LOG} > temp && mv temp ${LOG} && rm ${VERSION}.rst

- Update ``__version__`` in ``numpydoc/_version.py``.

- Commit changes::

    git add numpydoc/_version.py ${LOG}
    git commit -m 'Designate <version> release'

- Add the version number (e.g., `v1.2.0`) as a tag in git::

    git tag -s [-u <key-id>] v<version> -m 'signed <version> tag'

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github::

    git push --tags origin main

  where ``origin`` is the name of the ``github.com:numpy/numpydoc`` repository

- Create release from tag::

   - go to https://github.com/numpy/numpydoc/releases/new?tag=v${VERSION}
   - add v${VERSION} for the `Release title`
   - paste contents (or upload) of ${VERSION}.md in the `Describe this release section`
   - if pre-release check the box labelled `Set as a pre-release`


- Update https://github.com/numpy/numpydoc/milestones::

   - close old milestone
   - ensure new milestone exists (perhaps setting due date)

- Update ``__version__`` in ``numpydoc/_version.py``.

- Commit changes::

    git add numpydoc/_version.py
    git commit -m 'Bump version'
    git push origin main
