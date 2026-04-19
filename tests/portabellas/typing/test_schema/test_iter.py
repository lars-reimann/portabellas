from portabellas.typing import DataType, Schema


def test_should_iterate_over_column_names() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert list(schema) == ["a", "b"]


def test_should_iterate_over_empty_schema() -> None:
    schema = Schema({})
    assert list(schema) == []
