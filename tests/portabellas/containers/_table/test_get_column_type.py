import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError
from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("table", "name", "expected"),
    [
        pytest.param(Table({"a": [1, 2, 3]}), "a", DataTypes.Int64(), id="int column"),
        pytest.param(Table({"a": [1.0, 2.0, 3.0]}), "a", DataTypes.Float64(), id="float column"),
        pytest.param(Table({"a": ["x", "y"]}), "a", DataTypes.String(), id="string column"),
        pytest.param(Table({"a": [True, False]}), "a", DataTypes.Boolean(), id="boolean column"),
    ],
)
def test_should_return_column_type(table: Table, name: str, expected: DataType) -> None:
    assert table.get_column_type(name) == expected


def test_should_raise_if_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3]})
    with pytest.raises(ColumnNotFoundError):
        table.get_column_type("b")
