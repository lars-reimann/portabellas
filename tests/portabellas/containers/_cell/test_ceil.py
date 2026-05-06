import math

import pytest

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works, cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="zero int"),
        pytest.param(0.0, 0, id="zero float"),
        pytest.param(10, 10, id="positive int"),
        pytest.param(10.5, 11, id="positive float"),
        pytest.param(-10, -10, id="negative int"),
        pytest.param(-10.5, -10, id="negative float"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_ceiling(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: math.ceil(cell), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
def test_should_raise_for_non_numeric_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected numeric type"):
        _ = math.ceil(cell_of_type(cell_type))


def test_should_skip_validation_for_unknown_type() -> None:
    _ = math.ceil(cell_of_unknown_type())
