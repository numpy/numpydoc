from copy import deepcopy
from io import StringIO

import pytest
from numpydoc.xref import DEFAULT_LINKS
from sphinx.util import logging


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
    numpydoc_validation_checks = set()
    numpydoc_validation_exclude = set()


class MockBuilder():
    config = MockConfig()


class MockApp():
    config = MockConfig()
    builder = MockBuilder()
    translator = None

    def __init__(self):
        self.builder.app = self
        # Attrs required for logging
        self.verbosity = 2
        self._warncount = 0
        self.warningiserror = False


@pytest.fixture
def mock_app():
    app = MockApp()
    status, warning = StringIO(), StringIO()
    logging.setup(app, status, warning)

    yield app
