# -*- encoding:utf-8 -*-
from __future__ import division, absolute_import, print_function

from numpydoc.numpydoc import mangle_docstrings
from sphinx.ext.autodoc import ALL

class MockConfig():
    numpydoc_use_plots = False
    numpydoc_use_blockquotes = True
    numpydoc_show_class_members = True
    numpydoc_show_inherited_class_members = True
    numpydoc_class_members_toctree = True
    numpydoc_xref_param_type = False
    numpydoc_xref_aliases = {}
    numpydoc_xref_ignore = set()
    templates_path = []
    numpydoc_edit_link = False
    numpydoc_citation_re = '[a-z0-9_.-]+'
    numpydoc_attributes_as_param_list = True

class MockBuilder():
    config = MockConfig()

class MockApp():
    config = MockConfig()
    builder = MockBuilder()
    translator = None


app = MockApp()
app.builder.app = app

def test_mangle_docstrings():
    s ='''
A top section before

.. autoclass:: str
    '''
    lines = s.split('\n')
    doc = mangle_docstrings(MockApp(), 'class', 'str', str, {}, lines)
    assert 'rpartition' in [x.strip() for x in lines]

    lines = s.split('\n')
    doc = mangle_docstrings(MockApp(), 'class', 'str', str, {'members': ['upper']}, lines)
    assert 'rpartition' not in [x.strip() for x in lines]
    assert 'upper' in [x.strip() for x in lines]

    lines = s.split('\n')
    doc = mangle_docstrings(MockApp(), 'class', 'str', str, {'exclude-members': ALL}, lines)
    assert 'rpartition' not in [x.strip() for x in lines]
    assert 'upper' not in [x.strip() for x in lines]

    lines = s.split('\n')
    doc = mangle_docstrings(MockApp(), 'class', 'str', str,
                            {'exclude-members': ['upper']}, lines)
    assert 'rpartition' in [x.strip() for x in lines]
    assert 'upper' not in [x.strip() for x in lines]

if __name__ == "__main__":
    import pytest
