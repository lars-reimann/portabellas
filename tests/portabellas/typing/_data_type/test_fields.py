import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected_fields"),
    [
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String()}),
            {"name": DataTypes.String()},
            id="single field",
        ),
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            {"name": DataTypes.String(), "age": DataTypes.Int64()},
            id="multiple fields",
        ),
        pytest.param(
            DataTypes.Struct(fields={"a": DataTypes.List(DataTypes.Int64())}),
            {"a": DataTypes.List(DataTypes.Int64())},
            id="nested list field",
        ),
    ],
)
def test_should_return_fields(type_: DataTypes.Struct, expected_fields: dict[str, DataType]) -> None:
    assert type_.fields == expected_fields
