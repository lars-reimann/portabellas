from typing import Any

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, cell_of_type, cell_of_unknown_type

_none_cell = Cell.constant(None)


@pytest.mark.parametrize(
    ("cells", "expected"),
    [
        pytest.param([], None, id="empty"),
        pytest.param([_none_cell], None, id="all None"),
        pytest.param([_none_cell, Cell.constant(1)], 1, id="one not null"),
        pytest.param([Cell.constant(1), _none_cell, Cell.constant(2)], 1, id="multiple not null"),
    ],
)
def test_should_return_first_non_null_value(cells: list[Cell], expected: Any) -> None:
    column = Column("a", [None])
    transformed = column.map(lambda _: Cell.first_not_null(cells))
    assert transformed.get_value(0) == expected


@pytest.mark.parametrize(
    ("cells", "expected_type"),
    [
        pytest.param([cell_of_type(DataTypes.Int32())], DataTypes.Int32(), id="single cell with known type"),
        pytest.param(
            [cell_of_type(DataTypes.Int32()), cell_of_type(DataTypes.Int32())],
            DataTypes.Int32(),
            id="multiple cells with same type",
        ),
        pytest.param(
            [cell_of_type(DataTypes.Int32()), cell_of_type(DataTypes.String())],
            DataTypes.Unknown(),
            id="mixed types",
        ),
        pytest.param([cell_of_unknown_type()], DataTypes.Unknown(), id="unknown type"),
        pytest.param(
            [cell_of_type(DataTypes.Int32()), cell_of_unknown_type()],
            DataTypes.Unknown(),
            id="known and unknown types",
        ),
        pytest.param([_none_cell], DataTypes.Unknown(), id="constant None"),
    ],
)
def test_should_infer_type(cells: list[Cell], expected_type: DataType) -> None:
    result = Cell.first_not_null(cells)
    assert isinstance(result, ExprCell)
    assert_cell_has_type(result, expected_type)
