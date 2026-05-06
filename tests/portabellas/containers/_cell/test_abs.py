import polars as pl
import pytest

from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="zero int"),
        pytest.param(0.0, 0.0, id="zero float"),
        pytest.param(10, 10, id="positive int"),
        pytest.param(10.5, 10.5, id="positive float"),
        pytest.param(-10, 10, id="negative int"),
        pytest.param(-10.5, 10.5, id="negative float"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_absolute_value(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: abs(cell), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
def test_should_not_raise_for_numeric_type(cell_type: DataType) -> None:
    cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
    _ = abs(cell)


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
def test_should_raise_for_non_numeric_type(cell_type: DataType) -> None:
    cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
    with pytest.raises(ColumnTypeError, match="Expected numeric type"):
        _ = abs(cell)


def test_should_skip_validation_for_unknown_type() -> None:
    cell: ExprCell = ExprCell(pl.col("a"))
    _ = abs(cell)
