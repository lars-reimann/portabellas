import pytest

from portabellas import Column
from portabellas.typing import DataType
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("value", "old_name", "new_name", "expected", "type_if_none", "expected_type"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            "name",
            "first_name",
            {"first_name": "Alice", "age": 25},
            None,
            None,
            id="rename string field",
        ),
        pytest.param(
            {"name": "Alice", "age": 25},
            "age",
            "years",
            {"name": "Alice", "years": 25},
            None,
            None,
            id="rename int field",
        ),
        pytest.param(
            None,
            "name",
            "first_name",
            None,
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            DataType.Struct(fields={"first_name": DataType.String(), "age": DataType.Int64()}),
            id="None",
        ),
    ],
)
def test_should_rename_struct_field(
    value: dict | None,
    old_name: str,
    new_name: str,
    expected: dict | None,
    type_if_none: DataType | None,
    expected_type: DataType | None,
) -> None:
    column = Column("a", [value], type=type_if_none)
    result = column.map(lambda cell: cell.struct.rename(old_name, new_name))
    expected_column = Column("a", [expected], type=expected_type)
    assert_tables_are_equal(result.to_table(), expected_column.to_table())
