from portabellas.typing import DataType, Schema


def test_should_return_column_count() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema.column_count == 2


def test_should_return_zero_for_empty_schema() -> None:
    schema = Schema({})
    assert schema.column_count == 0
