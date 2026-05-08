from collections.abc import Callable

import pytest

from portabellas.containers import Cell
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
