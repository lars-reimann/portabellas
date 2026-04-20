import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "ignore_missing_values", "expected"),
    [
        pytest.param([], True, [], id="empty"),
        pytest.param([1, 2, 2], True, [2], id="numeric"),
        pytest.param(["a", "a", "b"], True, ["a"], id="non-numeric"),
        pytest.param([1, 2, None], True, [1, 2], id="multiple most frequent values (missing values ignored)"),
        pytest.param(
            [1, 2, None], False, [None, 1, 2], id="multiple most frequent values (missing values not ignored)"
        ),
        pytest.param([None, 2, None], True, [2], id="missing values are most frequent (missing values ignored)"),
        pytest.param(
            [None, 2, None], False, [None], id="missing values are most frequent (missing values not ignored)"
        ),
        pytest.param([None, None, None], True, [], id="only missing values (missing values ignored)"),
        pytest.param([None, None, None], False, [None], id="only missing values (missing values not ignored)"),
    ],
)
def test_should_return_most_frequent_values(values: list, ignore_missing_values: bool, expected: list) -> None:
    column = Column("col1", values)
    assert column.mode(ignore_missing_values=ignore_missing_values) == expected
