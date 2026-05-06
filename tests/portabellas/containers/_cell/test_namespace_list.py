import polars as pl
import pytest

from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.List(DataTypes.Int64()), id="list of int"),
    ],
)
def test_should_not_raise_for_list_type(cell_type: DataType) -> None:
    cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
    _ = cell.list


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.String(), id="string"),
    ],
)
def test_should_raise_for_non_list_type(cell_type: DataType) -> None:
    cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
    with pytest.raises(ColumnTypeError, match="Expected list type"):
        _ = cell.list


def test_should_skip_validation_for_unknown_type() -> None:
    cell: ExprCell = ExprCell(pl.col("a"))
    _ = cell.list
