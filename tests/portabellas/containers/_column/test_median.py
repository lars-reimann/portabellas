import pytest

from portabellas import Column
from portabellas.exceptions import NonNumericColumnError


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 2, 3], 2, id="odd number of values"),
        pytest.param([1, 2, 3, 4], 2.5, id="even number of values"),
        pytest.param([1, 2, 3, None], 2, id="some missing values"),
    ],
)
def test_should_return_median(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.median() == expected


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
    with pytest.raises(NonNumericColumnError):
        column.median()
