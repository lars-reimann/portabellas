import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "ignore_nulls", "expected"),
    [
        pytest.param([], True, [], id="empty"),
        pytest.param([1, 2, 2], True, [2], id="numeric"),
        pytest.param(["a", "a", "b"], True, ["a"], id="non-numeric"),
        pytest.param([1, 2, None], True, [1, 2], id="multiple most frequent values (nulls ignored)"),
        pytest.param([1, 2, None], False, [None, 1, 2], id="multiple most frequent values (nulls not ignored)"),
        pytest.param([None, 2, None], True, [2], id="nulls are most frequent (nulls ignored)"),
        pytest.param([None, 2, None], False, [None], id="nulls are most frequent (nulls not ignored)"),
        pytest.param([None, None, None], True, [], id="only nulls (nulls ignored)"),
        pytest.param([None, None, None], False, [None], id="only nulls (nulls not ignored)"),
    ],
)
def test_should_return_most_frequent_values(values: list, ignore_nulls: bool, expected: list) -> None:
    column = Column("col1", values)
    assert column.mode(ignore_nulls=ignore_nulls) == expected
