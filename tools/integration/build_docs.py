#!/usr/bin/env python3
"""Build a downstream project's documentation against this numpydoc checkout.

This is what the ``integration`` jobs in ``.circleci/config.yml`` run, and it
takes the same argument by hand::

    python tools/integration/build_docs.py networkx

Every project gets a throwaway virtualenv under ``build/integration``, built
and filled by ``uv``: we install the project's released wheel, clone its docs at
the matching tag, install its documentation requirements, force-install numpydoc
from this checkout on top, and run sphinx-build.  A nonzero sphinx-build exit is
the failure criterion.

Warnings are errors, because that is how a numpydoc regression usually shows
up.  A project with no ``allowed_warnings`` is built with ``-W --keep-going``
the way upstream builds it; one with ``allowed_warnings`` is built without
``-W``, and every line of the warnings file must then match one of them.
"""

from __future__ import annotations

import argparse
import dataclasses
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKDIR = REPO_ROOT / "build" / "integration"


@dataclasses.dataclass(frozen=True)
class Project:
    """A downstream project whose documentation we build."""

    #: Importable module name; the dict key below is the name on PyPI.
    module: str
    repo: str
    #: Documentation source directory, relative to the repository root.
    source_dir: str
    #: ``("file", <path in the clone>)`` or ``("group", <PEP 735 group>)`` entries.
    requirements: tuple[tuple[str, str], ...]
    #: ``str.format`` template mapping an installed version to a git tag.
    tag_template: str = "v{version}"
    #: Extra ``-D key=value`` overrides passed to ``sphinx-build``.
    sphinx_defines: tuple[str, ...] = ()
    #: Regexes for warning *lines* this project cannot avoid under our recipe.
    #: Empty (the default) means warning-free, i.e. built with ``-W``.
    allowed_warnings: tuple[str, ...] = ()
    #: Distributions to strip from the requirements files before installing.
    exclude_requirements: tuple[str, ...] = ()
    #: Commands run before ``sphinx-build``; ``{python}`` becomes the venv's.
    pre_build: tuple[tuple[str, ...], ...] = ()
    #: Where ``pre_build`` runs, relative to the clone: two of upstream's
    #: scripts hard-code paths relative to their own ``doc`` directory.
    pre_build_cwd: str = "."
    #: Python appended to the cloned ``conf.py``, for what ``-D`` cannot do.
    conf_append: str = ""


#: Rewrite missing-references.json keys for a non-editable install (see below).
_MPL_SED = r's#"lib/[^"]*/([^"/]+):#"<external>/\1:#'

PROJECTS: dict[str, Project] = {
    # The small, fast smoke test.  Warning-free, so it gets -W even though
    # upstream's `make html` passes no SPHINXOPTS.
    "networkx": Project(
        module="networkx",
        repo="https://github.com/networkx/networkx.git",
        tag_template="networkx-{version}",
        source_dir="doc",
        # doc.txt alone is not enough: conf.py loads
        # matplotlib.sphinxext.plot_directive, which the other two extras pull in.
        requirements=(
            ("file", "requirements/default.txt"),
            ("file", "requirements/extra.txt"),
            ("file", "requirements/doc.txt"),
        ),
        # pygraphviz needs graphviz's C headers; conf.py treats it as optional.
        exclude_requirements=("pygraphviz",),
        # Don't execute the gallery examples or the myst-nb tutorial.
        sphinx_defines=("plot_gallery=0", "nb_execution_mode=off"),
        # The networkx 3.7 release notes have an unbalanced `*Matcher` that
        # docutils warns about (fixed upstream after 3.7); a no-op otherwise.
        pre_build_cwd="doc",
        pre_build=(
            (
                "sed",
                "-i",
                r"s/^- Expose \*Matcher classes/- Expose ``*Matcher`` classes/",
                "release/release_3.7.rst",
            ),
        ),
    ),
    # Upstream builds with SPHINXOPTS="-W -j auto" and so do we, once the images
    # `plot_gallery=0` never renders are suppressed.  suppress_warnings repeats
    # the two entries upstream's conf.py sets, because -D replaces the list.
    "scikit-image": Project(
        module="skimage",
        repo="https://github.com/scikit-image/scikit-image.git",
        source_dir="doc/source",
        requirements=(("file", "requirements/docs.txt"),),
        sphinx_defines=(
            "plot_gallery=0",
            "suppress_warnings=config.cache,skimage2,image.not_readable",
        ),
        # The docs Makefile's `api` target.  Without it doc/source/api does not
        # exist and the build silently covers no API reference at all.
        pre_build_cwd="doc",
        pre_build=(("{python}", "tools/build_modref_templates.py"),),
    ),
    "matplotlib": Project(
        module="matplotlib",
        repo="https://github.com/matplotlib/matplotlib.git",
        source_dir="doc",
        requirements=(("group", "doc"),),
        # This is `make html-noplot`: conf.py greps sys.argv for the literal
        # "plot_gallery=0", so it has to be spelled exactly this way.
        sphinx_defines=("plot_gallery=0",),
        # Allowlist rather than upstream's -W: a :scale: on an image that
        # plot_gallery=0 never rendered cannot be measured, and conf.py filters
        # only the first message, only on the `sphinx` logger, which the writing
        # phase bypasses.  sphx_glr_ is sphinx-gallery's own prefix.
        allowed_warnings=(
            r"WARNING: Could not obtain image size\. :scale: option is ignored\.$",
            r"WARNING: Cannot scale image!$",
            r"^\s+Could not get size from \"\S*sphx_glr_",
            r"^\s+\[Errno 2\] No such file or directory: '\S*sphx_glr_",
        ),
        # missing-references.json keys each known-broken reference by the
        # docstring's source path, which only matches the editable install their
        # CI uses; from our wheel they are filed under <external>/<basename>.
        # Rewriting the keys drops ~76 ref.class/ref.obj warnings that are
        # exactly the shape a numpydoc regression produces, so allowlisting
        # them instead would defeat the point.
        pre_build_cwd="doc",
        pre_build=(("sed", "-i", "-E", _MPL_SED, "missing-references.json"),),
        # conf.py turns every warning into an error, and released matplotlib
        # has "name: type" parameter headers that numpydoc now warns about
        # (fixed upstream after 3.11.x).  Keep them visible but non-fatal.
        conf_append="""\
warnings.filterwarnings(
    "default", message=r".*has no space before the colon", category=UserWarning
)
""",
    ),
    # numpy and scipy get sphinx-build pointed straight at doc/source: their
    # Makefiles insist the installed library was built from the checkout.
    "numpy": Project(
        module="numpy",
        repo="https://github.com/numpy/numpy.git",
        source_dir="doc/source",
        requirements=(("file", "requirements/doc_requirements.txt"),),
        # breathe renders the C-API reference from doxygen XML that only a
        # source build produces; numpy's conf.py drops it cleanly when absent.
        exclude_requirements=("breathe",),
        # Skip the JupyterLite deployment behind the "Try it" buttons.
        sphinx_defines=("global_enable_try_examples=0",),
        # Upstream's Makefile has SPHINXOPTS ?= -W and so do we, after two
        # fixups that are ours rather than upstream's: the release notes
        # .. include:: a file `spin notes` writes at release time, and the
        # doxygen directives have no extension behind them without breathe.
        pre_build=(("touch", "doc/source/release/notes-towncrier.rst"),),
        conf_append="""\
from docutils.parsers.rst import Directive
_prev_setup = globals().get("setup")
_stub = type("Stub", (Directive,), {"optional_arguments": 1, "run": lambda self: []})
def setup(app):
    for _name in ("doxygenfunction", "doxygenclass"):
        app.add_directive(_name, _stub)
    return _prev_setup(app) if _prev_setup else None
""",
    ),
    # Not in CI: a full scipy docs build is too slow for a per-PR job.  Kept so
    # a maintainer can run it before a release; upstream uses -WT --keep-going,
    # but this is the one recipe no PR exercises, so it may need an allowlist.
    "scipy": Project(
        module="scipy",
        repo="https://github.com/scipy/scipy.git",
        source_dir="doc/source",
        requirements=(("file", "requirements/doc.txt"),),
        sphinx_defines=("global_enable_try_examples=0", "nb_execution_mode=off"),
    ),
}


#: An intersphinx inventory that could not be downloaded.  Its cross-references
#: then fail to resolve, which looks exactly like a numpydoc regression.
_INVENTORY_RE = re.compile(
    r"inventory '\S+' not fetchable|failed to reach any of the inventories"
)


def run(cmd: list, **kwargs) -> subprocess.CompletedProcess:
    """Run ``cmd``, echoing it first, and raise on a nonzero exit."""
    cmd = [str(arg) for arg in cmd]
    print(f"$ {subprocess.list2cmdline(cmd)}", flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


def filter_requirements(path: Path, exclude: tuple[str, ...]) -> Path:
    """Write a copy of ``path`` with the ``exclude``-ed distributions removed."""
    if not exclude:
        return path
    kept = [
        line
        for line in path.read_text().splitlines()
        if re.split(r"[<>=!~;\[\s#]", line.strip(), maxsplit=1)[0].lower()
        not in exclude
    ]
    out = path.with_name(f"{path.stem}-numpydoc{path.suffix}")
    out.write_text("\n".join(kept) + "\n")
    return out


def run_sphinx(cmd: list[str], source: Path, build_log: Path) -> int:
    """Run ``cmd``, teeing its output into ``build_log``, and return its status."""
    print(f"\n==> {subprocess.list2cmdline(cmd)}", flush=True)
    start = time.monotonic()
    # Line-buffered, and readline() rather than iterating the pipe (which reads
    # a buffer ahead), so a slow build keeps printing and a killed one still
    # leaves its log behind for the CI artifact.
    with build_log.open("w", buffering=1) as fid:
        proc = subprocess.Popen(
            cmd,
            cwd=source,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        for line in iter(proc.stdout.readline, ""):
            print(line, end="", flush=True)
            fid.write(line)
        returncode = proc.wait()
    minutes = (time.monotonic() - start) / 60
    print(f"\nsphinx-build exited {returncode} after {minutes:.1f} min")
    return returncode


def check_warnings(name: str, project: Project, warnings_log: Path) -> int:
    """Complain about every warning line that no allowlist entry matches."""
    text = warnings_log.read_text(errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    allowed = [re.compile(pattern) for pattern in project.allowed_warnings]
    left = [line for line in lines if not any(a.search(line) for a in allowed)]
    mode = "allowlist" if allowed else "-W --keep-going"
    print(f"\n{name}: {len(lines)} warning line(s) [{mode} mode]")
    for line in left:
        print(f"unexpected: {line}")
    return 1 if left else 0


def build(name: str, project: Project) -> int:
    """Run the whole recipe for ``project``.  Return a process exit code."""
    WORKDIR.mkdir(parents=True, exist_ok=True)
    checkout = WORKDIR / name
    warnings_log = WORKDIR / f"{name}-warnings.txt"
    build_log = WORKDIR / f"{name}-build.txt"

    # A fresh virtualenv per project: this installs dozens of packages and
    # force-reinstalls numpydoc, so the caller's environment is off limits.
    # Nothing in it needs pip, which is why uv never seeds one.
    env_dir = WORKDIR / f"venv-{name}"
    print(f"\n==> Creating the build environment in {env_dir}", flush=True)
    run(["uv", "venv", "--python", sys.executable, env_dir])
    python = env_dir / "bin" / "python"

    def pip(*args) -> None:
        # --compile-bytecode because pip byte-compiles on install and uv does
        # not: an old dependency whose source has an invalid escape sequence
        # then emits a SyntaxWarning on first import, which matplotlib's
        # `warnings.filterwarnings("error")` conf.py turns into a hard failure.
        run(["uv", "pip", "install", "--compile-bytecode", "--python", python, *args])

    # 1. Install the released wheel -- never build the project from source.
    pip("--only-binary", ":all:", name)
    version = subprocess.run(
        [python, "-c", f"import {project.module} as m; print(m.__version__)"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    tag = project.tag_template.format(version=version)

    # 2. Clone the docs sources at the tag matching the installed wheel.
    if checkout.exists():
        shutil.rmtree(checkout)
    run(["git", "clone", "--depth", "1", "--branch", tag, project.repo, checkout])

    # 3. Install the project's own documentation requirements.
    for kind, value in project.requirements:
        if kind == "file":
            req = filter_requirements(checkout / value, project.exclude_requirements)
            pip("-r", req)
        else:
            pip("--group", f"{checkout / 'pyproject.toml'}:{value}")

    # 4. Install numpydoc from this checkout LAST so it wins over any pin.
    pip("--force-reinstall", "--no-deps", REPO_ROOT)
    show = "import numpydoc; print(numpydoc.__version__, numpydoc.__file__)"
    # Not from the repo root: `python -c` would find the source tree on sys.path.
    run([python, "-c", show], cwd=WORKDIR)

    # 5. Stand in for what upstream generates outside of sphinx-build.
    for pre in project.pre_build:
        run(
            [python if arg == "{python}" else arg for arg in pre],
            cwd=checkout / project.pre_build_cwd,
        )
    if project.conf_append:
        conf = checkout / project.source_dir / "conf.py"
        conf.write_text(f"{conf.read_text()}\n\n{project.conf_append}")

    # 6. Build the docs.
    source = checkout / project.source_dir
    doctrees, out_dir = WORKDIR / f"{name}-doctrees", WORKDIR / f"{name}-html"
    cmd = [python, "-m", "sphinx", "-b", "html", "-j", "auto", "-T"]
    cmd += ["-d", doctrees, "-w", warnings_log]
    if not project.allowed_warnings:
        # `--keep-going` is a no-op in sphinx >= 8.1 but is upstream's spelling.
        cmd += ["-W", "--keep-going"]
    for define in project.sphinx_defines:
        cmd += ["-D", define]
    cmd += [source, out_dir]
    cmd = [str(arg) for arg in cmd]

    # matplotlib's wxPython inventory once failed to download on CircleCI, and
    # the unresolved references it left behind are indistinguishable from a
    # numpydoc regression, so a build that blames the network gets one retry --
    # from scratch, because a second pass over the cached doctrees would write
    # nothing and report no warnings at all.
    for _ in range(2):
        returncode = run_sphinx(cmd, source, build_log)
        if not _INVENTORY_RE.search(warnings_log.read_text(errors="replace")):
            break
        print("\n==> an intersphinx inventory was unreachable; rebuilding once")
        shutil.rmtree(doctrees, ignore_errors=True)
        shutil.rmtree(out_dir, ignore_errors=True)
    return returncode or check_warnings(name, project, warnings_log)


def main() -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project", choices=sorted(PROJECTS))
    args = parser.parse_args()
    return build(args.project, PROJECTS[args.project])


if __name__ == "__main__":
    raise SystemExit(main())
