import pytest

from portabellas.exceptions import ColumnNotFoundError
from portabellas.typing import DataTypes, Schema


def test_should_return_column_type() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert schema["a"] == DataTypes.Int64()
    assert schema["b"] == DataTypes.Float32()


def test_should_raise_column_not_found_error_if_column_does_not_exist() -> None:
    schema = Schema({"a": DataTypes.Int64()})
    with pytest.raises(ColumnNotFoundError):
        schema["b"]
