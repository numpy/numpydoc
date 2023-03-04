"""Utility functions for pre-commit hooks."""

import itertools
import os
from pathlib import Path
from typing import Sequence


def find_project_root(srcs: Sequence[str]):
    """
    Return a directory containing .git, .hg, pyproject.toml, or setup.cfg.

    That directory can be one of the directories passed in ``srcs`` or their
    common parent. If no directory in the tree contains a marker that would
    specify it's the project root, the root of the file system is returned.

    Parameters
    ----------
    srcs : Sequence[str]
        The filepaths to run the hook on.

    Returns
    -------
    str
        The project root directory.

    See Also
    --------
    black.find_project_root :
        This function was adapted from
        `Black <https://github.com/psf/black/blob/main/black.py>`_.
    """
    if not srcs:
        return Path(".").resolve(), "current directory"

    common_path = Path(
        os.path.commonpath([Path(src).expanduser().resolve() for src in srcs])
    )

    for dir in itertools.chain([common_path], common_path.parents):
        if (dir / "pyproject.toml").is_file():
            return dir, "pyproject.toml"
        if (dir / "setup.cfg").is_file():
            return dir, "setup.cfg"
        if (dir / ".git").exists() or (dir / ".hg").is_dir():
            return dir, "version control"

    return dir, "file system root"
