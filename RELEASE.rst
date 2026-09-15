Release process for ``numpydoc``
================================

Introduction
------------

The version is derived from git tags by ``setuptools_scm``; there is no
version string to edit by hand. Example ``__version__`` values:

- 1.8rc0            # tag ``v1.8rc0`` (1.8 release candidate 1)
- 1.8rc1.dev3+gabc  # 3 commits after ``v1.8rc0`` (development version)
- 1.8               # tag ``v1.8`` (1.8 release)
- 1.9.dev2+gdef     # 2 commits after ``v1.8`` (development version)

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

- Commit changes::

    git add ${LOG}
    git commit -m "Designate ${VERSION} release"

- Add the version number (e.g., `v1.2.0`) as a tag in git::

    git tag -s v${VERSION} -m "signed ${VERSION} tag"

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


  Pushing the tag triggers the ``Build Wheel and Release`` workflow, which
  builds the sdist and wheel and uploads them to PyPI. Check that the run
  succeeded and that the new version appears on
  https://pypi.org/project/numpydoc/.

- Update https://github.com/numpy/numpydoc/milestones::

   - close old milestone
   - ensure new milestone exists (perhaps setting due date)
