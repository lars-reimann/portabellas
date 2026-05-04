import pytest

from portabellas import Column
from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        pytest.param(Column("col1", [1]), DataTypes.Int64(), id="int"),
        pytest.param(Column("col1", ["a"]), DataTypes.String(), id="string"),
    ],
)
def test_should_return_type(column: Column, expected: DataType) -> None:
    assert column.type == expected
