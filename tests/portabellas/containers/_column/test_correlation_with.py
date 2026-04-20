import pytest

from portabellas import Column
from portabellas.exceptions import ColumnTypeError, LengthMismatchError, MissingValuesColumnError


@pytest.mark.parametrize(
    ("column1", "column2", "expected"),
    [
        pytest.param(Column("col1", [0, 1, 2]), Column("col2", [0, 1, 2]), 1.0, id="positive correlation"),
        pytest.param(Column("col1", [0, 1, 2]), Column("col2", [0, -1, -2]), -1.0, id="negative correlation"),
        pytest.param(Column("col", [0, 1, 2]), Column("col", [0, 1, 2]), 1.0, id="same column name"),
    ],
)
def test_should_return_correlation_between_two_columns(column1: Column, column2: Column, expected: float) -> None:
    assert column1.correlation_with(column2) == expected


@pytest.mark.parametrize(
    ("values_1", "values_2"),
    [
        pytest.param(["a"], [1], id="first string"),
        pytest.param([None], [1], id="first null"),
        pytest.param([1], ["a"], id="second string"),
        pytest.param([1], [None], id="second null"),
    ],
)
def test_should_raise_if_columns_are_not_numeric(values_1: list, values_2: list) -> None:
    column1 = Column("col1", values_1)
    column2 = Column("col2", values_2)
    with pytest.raises(ColumnTypeError):
        column1.correlation_with(column2)


def test_should_list_all_non_numeric_columns_in_error() -> None:
    column1 = Column("col1", ["a"])
    column2 = Column("col2", ["b"])
    with pytest.raises(ColumnTypeError, match=r"\['col1', 'col2'\]") as exc_info:
        column1.correlation_with(column2)
    assert "col1" in str(exc_info.value)
    assert "col2" in str(exc_info.value)


def test_should_raise_if_row_counts_differ() -> None:
    column1 = Column("col1", [1, 2, 3, 4])
    column2 = Column("col2", [2])
    with pytest.raises(LengthMismatchError):
        column1.correlation_with(column2)


@pytest.mark.parametrize(
    ("values_1", "values_2"),
    [
        pytest.param([None, 2], [1, 2], id="first missing"),
        pytest.param([1, 2], [1, None], id="second missing"),
    ],
)
def test_should_raise_if_columns_have_missing_values(values_1: list, values_2: list) -> None:
    column1 = Column("col1", values_1)
    column2 = Column("col2", values_2)
    with pytest.raises(MissingValuesColumnError):
        column1.correlation_with(column2)


def test_should_list_all_columns_with_missing_values_in_error() -> None:
    column1 = Column("col1", [None, 2])
    column2 = Column("col2", [1, None])
    with pytest.raises(MissingValuesColumnError, match=r"\['col1', 'col2'\]") as exc_info:
        column1.correlation_with(column2)
    assert "col1" in str(exc_info.value)
    assert "col2" in str(exc_info.value)
