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
    ("value", "substring", "expected"),
    [
        pytest.param("", "", True, id="empty string, empty substring"),
        pytest.param("", "c", False, id="empty string, non-empty substring"),
        pytest.param("abc", "", True, id="non-empty string, empty substring"),
        pytest.param("abc", "c", True, id="correct substring"),
        pytest.param("abc", "abc", True, id="substring equal to string"),
        pytest.param("abc", "d", False, id="incorrect substring"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as substring"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldCheckIfStringContainsSubstring:
    def test_plain_arguments(self, value: str | None, substring: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.contains(substring),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, substring: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.contains(
                Cell.constant(substring),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.contains("a"), DataTypes.Boolean(), id="string"),
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
