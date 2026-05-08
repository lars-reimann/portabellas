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
    ("value", "suffix", "expected"),
    [
        pytest.param("", "", True, id="empty string, empty suffix"),
        pytest.param("", "c", False, id="empty string, non-empty suffix"),
        pytest.param("abc", "", True, id="non-empty string, empty suffix"),
        pytest.param("abc", "c", True, id="correct suffix"),
        pytest.param("abc", "abc", True, id="suffix equal to string"),
        pytest.param("abc", "d", False, id="incorrect suffix"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as suffix"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldCheckIfStringEndsWithSuffix:
    def test_plain_arguments(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.ends_with(suffix),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.ends_with(
                Cell.constant(suffix),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.ends_with("a"), DataTypes.Boolean(), id="string"),
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
