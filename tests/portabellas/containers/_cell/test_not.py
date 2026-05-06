from typing import Any

import pytest

from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works, cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(False, True, id="False"),
        pytest.param(True, False, id="True"),
        pytest.param(None, None, id="None"),
    ],
)
class TestShouldInvertValueOfCell:
    def test_dunder_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: ~cell, expected, type_if_none=DataTypes.Boolean())

    def test_named_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: cell.not_(), expected, type_if_none=DataTypes.Boolean())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
class TestShouldNotRaiseForBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        _ = ~cell_of_type(cell_type)


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
class TestShouldRaiseForNonBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = ~cell_of_type(cell_type)


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        _ = ~cell_of_unknown_type()
