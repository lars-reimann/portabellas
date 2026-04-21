import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("abc", "abc", id="full lowercase"),
        pytest.param("ABC", "abc", id="full uppercase"),
        pytest.param("aBc", "abc", id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_string_to_lowercase(value: str | None, expected: str | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_lowercase(),
        expected,
        type_if_none=DataType.String(),
    )
