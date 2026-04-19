import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow
from portabellas.exceptions import ColumnNotFoundError


@pytest.mark.parametrize(
    ("table", "name", "expected_type_name"),
    [
        pytest.param(Table({"A": [1]}), "A", "i64", id="int column"),
        pytest.param(Table({"A": [1.0]}), "A", "f64", id="float column"),
        pytest.param(Table({"A": ["x"]}), "A", "str", id="string column"),
        pytest.param(Table({"A": [True]}), "A", "bool", id="bool column"),
    ],
)
def test_should_return_column_type(table: Table, name: str, expected_type_name: str) -> None:
    row = ExprRow(table)
    assert str(row.get_column_type(name)) == expected_type_name


def test_should_raise_if_column_does_not_exist() -> None:
    table = Table({"A": [1]})
    row = ExprRow(table)
    with pytest.raises(ColumnNotFoundError):
        row.get_column_type("B")
