import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("", None, id="empty"),
        pytest.param("abc", None, id="invalid"),
        pytest.param("1", 1.0, id="int"),
        pytest.param("1.5", 1.5, id="positive float"),
        pytest.param("-1.5", -1.5, id="negative float"),
        pytest.param("1e3", 1000, id="exponential"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_string_to_float(value: str | None, expected: float | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_float(),
        expected,
        type_if_none=DataType.String(),
    )
