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
        pytest.param("", "", 0, id="empty string, empty substring"),
        pytest.param("", "c", None, id="empty string, non-empty substring"),
        pytest.param("abc", "", 0, id="non-empty string, empty substring"),
        pytest.param("abc", "c", 2, id="correct substring"),
        pytest.param("abc", "abc", 0, id="substring equal to string"),
        pytest.param("abc", "d", None, id="incorrect substring"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as substring"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldGetIndexOfSubstring:
    def test_plain_arguments(self, value: str | None, substring: str | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.index_of(substring),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, substring: str | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.index_of(
                Cell.constant(substring),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.index_of("a"), DataTypes.UInt32(), id="string"),
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
