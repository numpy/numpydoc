from io import StringIO
import os.path as op
import shutil

import pytest
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace


# Test framework adapted from sphinx-gallery
@pytest.fixture(scope='module')
def sphinx_app(tmpdir_factory):
    temp_dir = (tmpdir_factory.getbasetemp() / 'root').strpath
    src_dir = op.join(op.dirname(__file__), 'tinybuild')

    def ignore(src, names):
        return ('_build', 'generated')

    shutil.copytree(src_dir, temp_dir, ignore=ignore)
    # For testing iteration, you can get similar behavior just doing `make`
    # inside the tinybuild directory
    src_dir = temp_dir
    conf_dir = temp_dir
    out_dir = op.join(temp_dir, '_build', 'html')
    toctrees_dir = op.join(temp_dir, '_build', 'toctrees')
    # Avoid warnings about re-registration, see:
    # https://github.com/sphinx-doc/sphinx/issues/5038
    with docutils_namespace():
        app = Sphinx(src_dir, conf_dir, out_dir, toctrees_dir,
                     buildername='html', status=StringIO())
        # need to build within the context manager
        # for automodule and backrefs to work
        app.build(False, [])
    return app


def test_class(sphinx_app):
    """Test that class documentation is reasonable."""
    src_dir, out_dir = sphinx_app.srcdir, sphinx_app.outdir
    class_rst = op.join(src_dir, 'generated', 'nd_test_mod.MyClass.rst')
    with open(class_rst, 'r') as fid:
        rst = fid.read()
    assert r'nd\_test\_mod.MyClass' in rst  # properly escaped
    class_html = op.join(out_dir, 'generated', 'nd_test_mod.MyClass.html')
    with open(class_html, 'r') as fid:
        html = fid.read()
    # escaped * chars should no longer be preceded by \'s
    assert r'\*' in html  # XXX should be "not in", bug!
    assert 'self,' in html   # XXX should be "not in", bug!


def test_function(sphinx_app):
    """Test that a timings page is created."""
    out_dir = sphinx_app.outdir
    function_html = op.join(out_dir, 'generated',
                            'nd_test_mod.my_function.html')
    with open(function_html, 'r') as fid:
        html = fid.read()
    assert r'\*args' not in html
    assert '*args' in html
