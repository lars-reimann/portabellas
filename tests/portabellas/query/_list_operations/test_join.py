from collections.abc import Callable

import pytest

from portabellas.containers import Cell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "separator", "expected"),
    [
        pytest.param(["a", "b", "c"], "-", "a-b-c", id="hyphen separator"),
        pytest.param(["a", "b", "c"], "", "abc", id="empty separator"),
        pytest.param(["x"], ",", "x", id="single element"),
        pytest.param(None, ",", None, id="None list"),
        pytest.param(["a", "b", "c"], None, None, id="None separator"),
    ],
)
class TestShouldJoinListElements:
    def test_plain_arguments(self, value: list | None, separator: str | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.join(separator),
            expected,
            type_=DataTypes.List(DataTypes.String()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, separator: str | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.join(Cell.constant(separator, type=DataTypes.String())),
            expected,
            type_=DataTypes.List(DataTypes.String()),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.List(DataTypes.String()), lambda cell: cell.list.join("-"), DataTypes.String(), id="string_list"
        ),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)


@pytest.mark.parametrize(
    "given_type",
    [
        pytest.param(DataTypes.List(DataTypes.Int64()), id="int64 inner"),
        pytest.param(DataTypes.List(DataTypes.Float64()), id="float64 inner"),
    ],
)
def test_should_raise_type_error_for_non_string_inner(given_type: DataType) -> None:
    cell = cell_of_type(given_type)
    with pytest.raises(ColumnTypeError):
        cell.list.join("-")


def test_should_skip_validation_for_unknown_type() -> None:
    cell = cell_of_type(DataTypes.Unknown())
    cell.list.join("-")
