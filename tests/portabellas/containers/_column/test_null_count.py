import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1, 2, 3], 0, id="no nulls"),
        pytest.param([1, 2, 3, None], 1, id="some nulls"),
        pytest.param([None, None, None], 3, id="only nulls"),
    ],
)
def test_should_count_null_values(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.null_count() == expected
