import pytest

from portabellas._validation import check_bounds
from portabellas.exceptions import OutOfBoundsError


@pytest.mark.parametrize(
    ("actual", "inclusive", "should_raise"),
    [
        pytest.param(4, True, True, id="below inclusive"),
        pytest.param(4, False, True, id="below exclusive"),
        pytest.param(5, True, False, id="on inclusive"),
        pytest.param(5, False, True, id="on exclusive"),
        pytest.param(6, True, False, id="above inclusive"),
        pytest.param(6, False, False, id="above exclusive"),
    ],
)
def test_lower_bound(actual: float, inclusive: bool, should_raise: bool) -> None:
    if should_raise:
        with pytest.raises(OutOfBoundsError):
            check_bounds("x", actual, lower_bound=5, lower_bound_inclusive=inclusive)
    else:
        check_bounds("x", actual, lower_bound=5, lower_bound_inclusive=inclusive)


@pytest.mark.parametrize(
    ("actual", "inclusive", "should_raise"),
    [
        pytest.param(4, True, False, id="below inclusive"),
        pytest.param(4, False, False, id="below exclusive"),
        pytest.param(5, True, False, id="on inclusive"),
        pytest.param(5, False, True, id="on exclusive"),
        pytest.param(6, True, True, id="above inclusive"),
        pytest.param(6, False, True, id="above exclusive"),
    ],
)
def test_upper_bound(actual: float, inclusive: bool, should_raise: bool) -> None:
    if should_raise:
        with pytest.raises(OutOfBoundsError):
            check_bounds("x", actual, upper_bound=5, upper_bound_inclusive=inclusive)
    else:
        check_bounds("x", actual, upper_bound=5, upper_bound_inclusive=inclusive)


def test_should_skip_check_if_actual_is_none() -> None:
    check_bounds("x", None, lower_bound=5, upper_bound=10)


def test_should_skip_check_if_no_bounds_specified() -> None:
    check_bounds("x", 42.0)


def test_should_include_name_in_error_message() -> None:
    with pytest.raises(OutOfBoundsError, match="my_param"):
        check_bounds("my_param", -1, lower_bound=0)
