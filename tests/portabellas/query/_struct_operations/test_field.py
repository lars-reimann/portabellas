import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "field_name", "expected", "type_if_none"),
    [
        pytest.param({"name": "Alice", "age": 25}, "name", "Alice", None, id="string field"),
        pytest.param({"name": "Alice", "age": 25}, "age", 25, None, id="int field"),
        pytest.param(
            None,
            "name",
            None,
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            id="None",
        ),
    ],
)
def test_should_return_struct_field(
    value: dict | None,
    field_name: str,
    expected: object,
    type_if_none: DataType | None,
) -> None:
    assert_cell_operation_works(value, lambda cell: cell.struct.field(field_name), expected, type_if_none=type_if_none)
