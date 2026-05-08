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
    ("value", "prefix", "expected"),
    [
        pytest.param("", " ", "", id="empty"),
        pytest.param("~ a ~", "", "~ a ~", id="empty prefix"),
        pytest.param("~ a ~", "~ ", "a ~", id="non-empty (has prefix)"),
        pytest.param("~ a ~", " ~", "~ a ~", id="non-empty (does not have prefix)"),
        pytest.param(None, " ", None, id="None as string"),
        pytest.param("~ a ~", None, None, id="None as prefix"),
        pytest.param(None, None, None, id="None as both"),
    ],
)
class TestShouldRemovePrefix:
    def test_plain_arguments(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_prefix(prefix),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_prefix(
                Cell.constant(prefix, type=DataTypes.String()),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.remove_prefix("a"), DataTypes.String(), id="string"),
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
