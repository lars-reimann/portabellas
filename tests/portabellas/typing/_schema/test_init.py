from portabellas.typing import DataTypes, Schema


def test_should_store_the_schema() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert schema.column_names == ["a", "b"]
    assert schema["a"] == DataTypes.Int64()
    assert schema["b"] == DataTypes.Float32()


def test_should_store_empty_schema() -> None:
    schema = Schema({})
    assert schema.column_names == []
