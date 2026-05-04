import pytest

from portabellas.typing import DataType
from portabellas.typing._data_type import StructType


@pytest.mark.parametrize(
    ("type_", "expected_fields"),
    [
        pytest.param(
            DataType.Struct(fields={"name": DataType.String()}),
            {"name": DataType.String()},
            id="single field",
        ),
        pytest.param(
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            {"name": DataType.String(), "age": DataType.Int64()},
            id="multiple fields",
        ),
        pytest.param(
            DataType.Struct(fields={"a": DataType.List(DataType.Int64())}),
            {"a": DataType.List(DataType.Int64())},
            id="nested list field",
        ),
    ],
)
def test_should_return_fields(type_: StructType, expected_fields: dict[str, DataType]) -> None:
    assert type_.fields == expected_fields
