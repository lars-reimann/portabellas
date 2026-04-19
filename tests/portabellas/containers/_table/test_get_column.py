import pytest

from portabellas import Column, Table
from portabellas.exceptions import ColumnNotFoundError


@pytest.mark.parametrize(
    ("table", "name", "expected"),
    [
        pytest.param(Table({"col1": [1]}), "col1", Column("col1", [1]), id="one column"),
        pytest.param(Table({"col1": [1], "col2": [2]}), "col2", Column("col2", [2]), id="multiple columns"),
    ],
)
def test_should_get_column(table: Table, name: str, expected: Column) -> None:
    actual = table.get_column(name)
    assert list(actual) == list(expected)
    assert actual.name == expected.name


def test_should_raise_if_column_name_is_unknown() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({}).get_column("col1")
