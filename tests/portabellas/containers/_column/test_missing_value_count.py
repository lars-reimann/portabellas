import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1, 2, 3], 0, id="no missing values"),
        pytest.param([1, 2, 3, None], 1, id="some missing values"),
        pytest.param([None, None, None], 3, id="only missing values"),
    ],
)
def test_should_count_missing_values(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.missing_value_count() == expected
