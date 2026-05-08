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
    ("value", "old", "new", "expected"),
    [
        pytest.param("", "", "", "", id="all empty"),
        pytest.param("", "a", "z", "", id="empty value"),
        pytest.param("abc", "", "z", "zazbzcz", id="empty old"),
        pytest.param("abc", "a", "", "bc", id="empty new"),
        pytest.param("abc", "d", "z", "abc", id="no matches"),
        pytest.param("abc", "a", "z", "zbc", id="one match"),
        pytest.param("abcabc", "a", "z", "zbczbc", id="many matches"),
        pytest.param("abc", "abc", "z", "z", id="full match"),
        pytest.param(None, "a", "z", None, id="None value"),
        pytest.param("abc", None, "z", None, id="None old", marks=pytest.mark.xfail(reason="Not supported by polars.")),
        pytest.param("abc", "a", None, None, id="None new", marks=pytest.mark.xfail(reason="Not supported by polars.")),
    ],
)
class TestShouldReplaceAllOccurrencesOfOldWithNew:
    def test_plain_arguments(self, value: str | None, old: str | None, new: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.replace_all(old, new),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(
        self,
        value: str | None,
        old: str | None,
        new: str | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.replace_all(
                Cell.constant(old),
                Cell.constant(new),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.replace_all("a", "b"), DataTypes.String(), id="string"),
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
