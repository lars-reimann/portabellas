import pytest

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Date(), id="date"),
        pytest.param(DataTypes.Datetime(), id="datetime"),
        pytest.param(DataTypes.Time(), id="time"),
    ],
)
def test_should_not_raise_for_dt_type(cell_type: DataType) -> None:
    _ = cell_of_type(cell_type).dt


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Duration(time_unit="us"), id="duration"),
    ],
)
def test_should_raise_for_non_dt_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected Date, Datetime, or Time type"):
        _ = cell_of_type(cell_type).dt


def test_should_skip_validation_for_unknown_type() -> None:
    _ = cell_of_unknown_type().dt
