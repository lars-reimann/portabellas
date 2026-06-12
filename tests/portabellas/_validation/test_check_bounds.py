import pytest

from portabellas._validation import check_bounds
from portabellas.exceptions import OutOfBoundsError


class TestLowerBound:
    @pytest.mark.parametrize(
        ("actual", "inclusive", "should_raise"),
        [
            pytest.param(4, True, True, id="below closed"),
            pytest.param(4, False, True, id="below open"),
            pytest.param(5, True, False, id="on closed"),
            pytest.param(5, False, True, id="on open"),
            pytest.param(6, True, False, id="above closed"),
            pytest.param(6, False, False, id="above open"),
        ],
    )
    def test_lower_bound(self, actual: float, inclusive: bool, should_raise: bool) -> None:
        if should_raise:
            with pytest.raises(OutOfBoundsError):
                check_bounds("x", actual, lower_bound=5, lower_bound_inclusive=inclusive)
        else:
            check_bounds("x", actual, lower_bound=5, lower_bound_inclusive=inclusive)


class TestUpperBound:
    @pytest.mark.parametrize(
        ("actual", "inclusive", "should_raise"),
        [
            pytest.param(4, True, False, id="below closed"),
            pytest.param(4, False, False, id="below open"),
            pytest.param(5, True, False, id="on closed"),
            pytest.param(5, False, True, id="on open"),
            pytest.param(6, True, True, id="above closed"),
            pytest.param(6, False, True, id="above open"),
        ],
    )
    def test_upper_bound(self, actual: float, inclusive: bool, should_raise: bool) -> None:
        if should_raise:
            with pytest.raises(OutOfBoundsError):
                check_bounds("x", actual, upper_bound=5, upper_bound_inclusive=inclusive)
        else:
            check_bounds("x", actual, upper_bound=5, upper_bound_inclusive=inclusive)


class TestBothBounds:
    @pytest.mark.parametrize(
        ("lower_inclusive", "upper_inclusive", "actual", "should_raise"),
        [
            pytest.param(True, True, 5, False, id="on both closed"),
            pytest.param(False, False, 5, False, id="inside both open"),
            pytest.param(False, True, 0, True, id="at lower exclusive"),
            pytest.param(True, False, 10, True, id="at upper exclusive"),
        ],
    )
    def test_both_bounds(
        self,
        lower_inclusive: bool,
        upper_inclusive: bool,
        actual: float,
        should_raise: bool,
    ) -> None:
        if should_raise:
            with pytest.raises(OutOfBoundsError):
                check_bounds(
                    "x",
                    actual,
                    lower_bound=0,
                    lower_bound_inclusive=lower_inclusive,
                    upper_bound=10,
                    upper_bound_inclusive=upper_inclusive,
                )
        else:
            check_bounds(
                "x",
                actual,
                lower_bound=0,
                lower_bound_inclusive=lower_inclusive,
                upper_bound=10,
                upper_bound_inclusive=upper_inclusive,
            )


def test_should_skip_check_when_actual_is_none() -> None:
    check_bounds("x", None, lower_bound=5, upper_bound=10)


def test_should_not_raise_when_no_bounds_specified() -> None:
    check_bounds("x", 42.0)


def test_should_include_name_in_error_message() -> None:
    with pytest.raises(OutOfBoundsError, match="my_param"):
        check_bounds("my_param", -1, lower_bound=0)
