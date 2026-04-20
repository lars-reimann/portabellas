import pytest

from portabellas import Column, Table
from portabellas.exceptions import DuplicateColumnError, LengthMismatchError


@pytest.mark.parametrize(
    ("columns", "expected"),
    [
        pytest.param([], Table({}), id="empty list"),
        pytest.param(Column("A", []), Table({"A": []}), id="single column"),
        pytest.param(
            [Column("A", [1, 2]), Column("B", [3, 4])],
            Table({"A": [1, 2], "B": [3, 4]}),
            id="non-empty list",
        ),
    ],
)
def test_should_create_table_from_columns(columns: Column | list[Column], expected: Table) -> None:
    assert Table.from_columns(columns) == expected


def test_should_raise_if_row_counts_differ() -> None:
    with pytest.raises(LengthMismatchError):
        Table.from_columns([Column("col1", []), Column("col2", [1])])


def test_should_raise_if_duplicate_column_name() -> None:
    with pytest.raises(DuplicateColumnError):
        Table.from_columns([Column("col1", []), Column("col1", [])])
