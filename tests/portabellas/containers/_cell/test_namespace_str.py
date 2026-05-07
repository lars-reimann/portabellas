import pytest

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
    ],
)
def test_should_not_raise_for_string_type(cell_type: DataType) -> None:
    _ = cell_of_type(cell_type).str


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
def test_should_raise_for_non_string_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected String type"):
        _ = cell_of_type(cell_type).str


def test_should_skip_validation_for_unknown_type() -> None:
    _ = cell_of_unknown_type().str
