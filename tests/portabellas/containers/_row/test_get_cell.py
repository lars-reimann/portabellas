from typing import Any

import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow
from portabellas.exceptions import ColumnNotFoundError
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_row_operation_works


@pytest.mark.parametrize(
    ("table", "name", "target", "expected"),
    [
        pytest.param(
            Table({"A": [1, 2]}),
            "A",
            1,
            [True, False],
            id="one column",
        ),
        pytest.param(
            Table({"A": [1, 2], "B": [3, 4]}),
            "A",
            1,
            [True, False],
            id="two columns",
        ),
    ],
)
def test_should_get_correct_cell(
    table: Table,
    name: str,
    target: int,
    expected: list[Any],
) -> None:
    assert_row_operation_works(table, lambda row: row.get_cell(name) == target, expected)


@pytest.mark.parametrize(
    ("table", "name"),
    [
        pytest.param(Table({"A": []}), "B", id="non-empty table, missing column"),
    ],
)
def test_should_raise_if_column_does_not_exist(table: Table, name: str) -> None:
    row = ExprRow(table)
    with pytest.raises(ColumnNotFoundError):
        row.get_cell(name)


def test_should_pass_column_type() -> None:
    table = Table({"A": [1, 2]})
    cell = ExprRow(table).get_cell("A")
    assert_cell_has_type(cell, DataTypes.Int64())
