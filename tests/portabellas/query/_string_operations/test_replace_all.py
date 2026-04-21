import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


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
            type_if_none=DataType.String(),
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
            type_if_none=DataType.String(),
        )
