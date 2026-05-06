from typing import Any

import pytest

from portabellas.containers import Cell
from portabellas.containers._cell import ExprCell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        pytest.param(None, None, None, id="None"),
        pytest.param(1, None, 1, id="int"),
        pytest.param(1, DataTypes.String(), "1", id="with explicit type"),
    ],
)
def test_should_return_constant_value(value: Any, type_: DataType | None, expected: Any) -> None:
    assert_cell_operation_works(None, lambda _: Cell.constant(value, type=type_), expected)


@pytest.mark.parametrize(
    ("value", "expected_type"),
    [
        pytest.param(42, DataTypes.Int32(), id="int"),
        pytest.param(3.14, DataTypes.Float64(), id="float"),
        pytest.param("hello", DataTypes.String(), id="str"),
        pytest.param(True, DataTypes.Boolean(), id="bool"),
        pytest.param(None, DataTypes.Unknown(), id="none"),
    ],
)
def test_should_infer_type_from_value(value: object, expected_type: DataType) -> None:
    cell = Cell.constant(value)
    assert isinstance(cell, ExprCell)
    assert cell._type == expected_type


def test_should_use_explicit_type_over_inferred() -> None:
    cell = Cell.constant(42, type=DataTypes.Int64())
    assert isinstance(cell, ExprCell)
    assert cell._type == DataTypes.Int64()
