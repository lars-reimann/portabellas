import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "ignore_nulls", "expected"),
    [
        pytest.param([], True, 0, id="empty"),
        pytest.param([1, 2, 3], True, 3, id="no duplicates"),
        pytest.param([1, 2, 1], True, 2, id="some duplicate"),
        pytest.param([1, 2, 3, None], True, 3, id="with nulls (ignored)"),
        pytest.param([1, 2, 3, None], False, 4, id="with nulls (not ignored)"),
    ],
)
def test_should_return_number_of_distinct_values(values: list, ignore_nulls: bool, expected: int) -> None:
    column = Column("col", values)
    assert column.distinct_value_count(ignore_nulls=ignore_nulls) == expected
