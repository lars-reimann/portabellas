import pytest

from portabellas import Column
from portabellas.exceptions import ColumnTypeError


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 2, 3], 2, id="no missing values"),
        pytest.param([1, 2, 3, None], 2, id="some missing values"),
    ],
)
def test_should_return_mean(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.mean() == expected


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([], id="empty"),
        pytest.param([None], id="all missing values"),
        pytest.param(["a"], id="non-numeric"),
    ],
)
def test_should_raise_if_column_is_not_numeric(values: list) -> None:
    column = Column("col1", values)
    with pytest.raises(ColumnTypeError):
        column.mean()
