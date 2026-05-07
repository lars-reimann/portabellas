import pytest

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Duration(time_unit="us"), id="duration"),
    ],
)
def test_should_not_raise_for_duration_type(cell_type: DataType) -> None:
    _ = cell_of_type(cell_type).dur


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.String(), id="string"),
    ],
)
def test_should_raise_for_non_duration_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected Duration type"):
        _ = cell_of_type(cell_type).dur


def test_should_skip_validation_for_unknown_type() -> None:
    _ = cell_of_unknown_type().dur
