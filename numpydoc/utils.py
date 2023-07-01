"""Utility functions for numpydoc."""

from copy import deepcopy
from typing import Set

from .validate import ERROR_MSGS


def get_validation_checks(validation_checks: Set[str]) -> Set[str]:
    """
    Get the set of validation checks to report on.

    Parameters
    ----------
    validation_checks : set[str]
        A set of validation checks to report on. If the set is ``{"all"}``,
        all checks will be reported. If the set contains just specific checks,
        only those will be reported on. If the set contains both ``"all"`` and
        specific checks, all checks except those included in the set will be
        reported on.

    Returns
    -------
    set[str]
        The set of validation checks to report on.
    """
    # TODO: add tests
    valid_error_codes = set(ERROR_MSGS.keys())
    if "all" in validation_checks:
        block = deepcopy(validation_checks)
        validation_checks = valid_error_codes - block

    # Ensure that the validation check set contains only valid error codes
    invalid_error_codes = validation_checks - valid_error_codes
    if invalid_error_codes:
        raise ValueError(
            f"Unrecognized validation code(s) in numpydoc_validation_checks "
            f"config value: {invalid_error_codes}"
        )

    return validation_checks
