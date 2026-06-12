from __future__ import annotations

from portabellas.exceptions import OutOfBoundsError


def check_bounds(
    name: str,
    actual: float | None,
    *,
    lower_bound: float | None = None,
    lower_bound_inclusive: bool = True,
    upper_bound: float | None = None,
    upper_bound_inclusive: bool = True,
) -> None:
    """
    Check whether a value is within the expected range and raise an error if it is not.

    Parameters
    ----------
    name:
        The name of the offending variable.
    actual:
        The actual value that should be checked. If None, the check is skipped.
    lower_bound:
        The lower bound of the expected range. Use None if there is no lower bound.
    lower_bound_inclusive:
        Whether the lower bound is inclusive. Defaults to True.
    upper_bound:
        The upper bound of the expected range. Use None if there is no upper bound.
    upper_bound_inclusive:
        Whether the upper bound is inclusive. Defaults to True.

    Raises
    ------
    OutOfBoundsError
        If the actual value is outside its expected range.
    """
    if actual is None:
        return

    below_lower = False
    if lower_bound is not None:
        below_lower = actual < lower_bound if lower_bound_inclusive else actual <= lower_bound

    above_upper = False
    if upper_bound is not None:
        above_upper = actual > upper_bound if upper_bound_inclusive else actual >= upper_bound

    if below_lower or above_upper:
        lower_str = _bound_to_string(lower_bound, is_inclusive=lower_bound_inclusive, is_lower=True)
        upper_str = _bound_to_string(upper_bound, is_inclusive=upper_bound_inclusive, is_lower=False)
        message = f"{name} must be in {lower_str}, {upper_str} but was {actual}."
        raise OutOfBoundsError(message) from None


def _bound_to_string(value: float | None, *, is_inclusive: bool, is_lower: bool) -> str:
    if value is None:
        if is_lower:
            return "(-\u221e"
        return "\u221e)"

    bracket = "[" if is_inclusive else "("
    if is_lower:
        return f"{bracket}{value}"
    bracket = "]" if is_inclusive else ")"
    return f"{value}{bracket}"
