"""Test numpydoc.utils functions."""

import pytest

from numpydoc.validate import ERROR_MSGS
from numpydoc.utils import get_validation_checks

ALL_CHECKS = set(ERROR_MSGS.keys())


@pytest.mark.parametrize(
    ["checks", "expected"],
    [
        [{"all"}, ALL_CHECKS],
        [set(), set()],
        [{"EX01"}, {"EX01"}],
        [{"EX01", "SA01"}, {"EX01", "SA01"}],
        [{"all", "EX01", "SA01"}, ALL_CHECKS - {"EX01", "SA01"}],
        [{"all", "PR01"}, ALL_CHECKS - {"PR01"}],
    ],
)
def test_utils_get_validation_checks(checks, expected):
    """Ensure check selection is working."""
    assert get_validation_checks(checks) == expected


@pytest.mark.parametrize(
    "checks",
    [
        {"every"},
        {None},
        {"SM10"},
        {"EX01", "SM10"},
    ],
)
def test_get_validation_checks_validity(checks):
    """Ensure that invalid checks are flagged."""
    with pytest.raises(ValueError, match="Unrecognized validation code"):
        _ = get_validation_checks(checks)
