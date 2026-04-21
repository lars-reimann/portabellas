import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected", "type_if_none"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            '{"name":"Alice","age":25}',
            None,
            id="struct with string and int",
        ),
        pytest.param(
            None,
            "null",
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            id="None",
        ),
    ],
)
def test_should_convert_struct_to_json(value: dict | None, expected: str | None, type_if_none: DataType | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.struct.to_json(), expected, type_if_none=type_if_none)
