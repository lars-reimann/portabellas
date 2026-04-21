import pytest

from portabellas import Column
from portabellas.typing import DataType
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("value", "suffix", "expected", "type_if_none", "expected_type"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            "_suf",
            {"name_suf": "Alice", "age_suf": 25},
            None,
            None,
            id="suffix all fields",
        ),
        pytest.param(
            None,
            "_suf",
            None,
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            DataType.Struct(fields={"name_suf": DataType.String(), "age_suf": DataType.Int64()}),
            id="None",
        ),
    ],
)
def test_should_suffix_field_names(
    value: dict | None,
    suffix: str,
    expected: dict | None,
    type_if_none: DataType | None,
    expected_type: DataType | None,
) -> None:
    column = Column("a", [value], type=type_if_none)
    result = column.map(lambda cell: cell.struct.suffix_names(suffix))
    expected_column = Column("a", [expected], type=expected_type)
    assert_tables_are_equal(result.to_table(), expected_column.to_table())
