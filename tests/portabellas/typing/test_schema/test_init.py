from portabellas.typing import DataType, Schema


def test_should_store_the_schema() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema.column_names == ["a", "b"]
    assert schema["a"] == DataType.Int64()
    assert schema["b"] == DataType.Float32()


def test_should_store_empty_schema() -> None:
    schema = Schema({})
    assert schema.column_names == []
