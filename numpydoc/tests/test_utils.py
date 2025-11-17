from numpydoc._utils import _clean_text_signature


def test_clean_text_signature():
    assert _clean_text_signature(None) is None
    assert _clean_text_signature("func($self)") == "func()"
    assert (
        _clean_text_signature("func($self, *args, **kwargs)") == "func(*args, **kwargs)"
    )
    assert _clean_text_signature("($self)") == "()"
    assert _clean_text_signature("()") == "()"
    assert _clean_text_signature("func()") == "func()"
    assert (
        _clean_text_signature("func($self, /, *args, **kwargs)")
        == "func(*args, **kwargs)"
    )
    assert (
        _clean_text_signature("func($self, other, /, *args, **kwargs)")
        == "func(other, *args, **kwargs)"
    )
    assert _clean_text_signature("($module)") == "()"
    assert _clean_text_signature("func($type)") == "func()"
    assert (
        _clean_text_signature('func($self, foo="hello world")')
        == 'func(foo="hello world")'
    )
    assert (
        _clean_text_signature("func($self, foo='hello world')")
        == "func(foo='hello world')"
    )
    assert _clean_text_signature('func(foo="hello world")') == 'func(foo="hello world")'
    assert _clean_text_signature('func(foo="$self")') == 'func(foo="$self")'
    assert _clean_text_signature('func($self, foo="$self")') == 'func(foo="$self")'
    assert _clean_text_signature("func(self, other)") == "func(self, other)"
    assert _clean_text_signature("func($self, *args)") == "func(*args)"
