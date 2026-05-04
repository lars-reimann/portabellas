import pytest

from portabellas import Column
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("value", "prefix", "expected", "type_if_none", "expected_type"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            "pre_",
            {"pre_name": "Alice", "pre_age": 25},
            None,
            None,
            id="prefix all fields",
        ),
        pytest.param(
            None,
            "pre_",
            None,
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            DataTypes.Struct(fields={"pre_name": DataTypes.String(), "pre_age": DataTypes.Int64()}),
            id="None",
        ),
    ],
)
def test_should_prefix_field_names(
    value: dict | None,
    prefix: str,
    expected: dict | None,
    type_if_none: DataType | None,
    expected_type: DataType | None,
) -> None:
    column = Column("a", [value], type=type_if_none)
    result = column.map(lambda cell: cell.struct.prefix_names(prefix))
    expected_column = Column("a", [expected], type=expected_type)
    assert_tables_are_equal(result.to_table(), expected_column.to_table())
