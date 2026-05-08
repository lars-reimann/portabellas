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
    ("value", "base", "expected"),
    [
        pytest.param("", 10, None, id="empty"),
        pytest.param("abc", 10, None, id="invalid"),
        pytest.param("10", 10, 10, id="base 10"),
        pytest.param("10", 2, 2, id="base 2"),
        pytest.param(None, 10, None, id="None as value"),
        pytest.param("0", None, None, id="None as base"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldConvertStringToInteger:
    def test_plain_arguments(self, value: str | None, base: int | None, expected: float | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.to_int(base=base),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, base: int | None, expected: float | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.to_int(
                base=Cell.constant(base),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.to_int(), DataTypes.Int64(), id="string"),
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
