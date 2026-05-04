from portabellas.typing import DataTypes, Schema


def test_should_return_column_count() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert len(schema) == 2


def test_should_return_zero_for_empty_schema() -> None:
    schema = Schema({})
    assert len(schema) == 0
