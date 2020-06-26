# -*- encoding:utf-8 -*-
from copy import deepcopy
from numpydoc.numpydoc import mangle_docstrings, _clean_text_signature
from numpydoc.xref import DEFAULT_LINKS
from sphinx.ext.autodoc import ALL


class MockConfig():
    numpydoc_use_plots = False
    numpydoc_use_blockquotes = True
    numpydoc_show_class_members = True
    numpydoc_show_inherited_class_members = True
    numpydoc_class_members_toctree = True
    numpydoc_xref_param_type = False
    numpydoc_xref_aliases = {}
    numpydoc_xref_aliases_complete = deepcopy(DEFAULT_LINKS)
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
    s = '''
A top section before

.. autoclass:: str
    '''
    lines = s.split('\n')
    mangle_docstrings(MockApp(), 'class', 'str', str, {}, lines)
    assert 'rpartition' in [x.strip() for x in lines]

    lines = s.split('\n')
    mangle_docstrings(
        MockApp(), 'class', 'str', str, {'members': ['upper']}, lines)
    assert 'rpartition' not in [x.strip() for x in lines]
    assert 'upper' in [x.strip() for x in lines]

    lines = s.split('\n')
    mangle_docstrings(
        MockApp(), 'class', 'str', str, {'exclude-members': ALL}, lines)
    assert 'rpartition' not in [x.strip() for x in lines]
    assert 'upper' not in [x.strip() for x in lines]

    lines = s.split('\n')
    mangle_docstrings(
        MockApp(), 'class', 'str', str, {'exclude-members': ['upper']}, lines)
    assert 'rpartition' in [x.strip() for x in lines]
    assert 'upper' not in [x.strip() for x in lines]


def test_clean_text_signature():
    assert _clean_text_signature(None) is None
    assert _clean_text_signature('func($self)') == 'func()'
    assert (_clean_text_signature('func($self, *args, **kwargs)')
            == 'func(*args, **kwargs)')
    assert _clean_text_signature('($self)') == '()'
    assert _clean_text_signature('()') == '()'
    assert _clean_text_signature('func()') == 'func()'
    assert (_clean_text_signature('func($self, /, *args, **kwargs)')
            == 'func(*args, **kwargs)')
    assert (_clean_text_signature('func($self, other, /, *args, **kwargs)')
            == 'func(other, *args, **kwargs)')
    assert _clean_text_signature('($module)') == '()'
    assert _clean_text_signature('func($type)') == 'func()'
    assert (_clean_text_signature('func($self, foo="hello world")')
            == 'func(foo="hello world")')
    assert (_clean_text_signature("func($self, foo='hello world')")
            == "func(foo='hello world')")
    assert (_clean_text_signature('func(foo="hello world")')
            == 'func(foo="hello world")')
    assert (_clean_text_signature('func(foo="$self")')
            == 'func(foo="$self")')
    assert (_clean_text_signature('func($self, foo="$self")')
            == 'func(foo="$self")')
    assert _clean_text_signature('func(self, other)') == 'func(self, other)'
    assert _clean_text_signature('func($self, *args)') == 'func(*args)'


if __name__ == "__main__":
    import pytest
    pytest.main()
