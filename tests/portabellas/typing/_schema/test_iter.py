from portabellas.typing import DataTypes, Schema


def test_should_iterate_over_column_names() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert list(schema) == ["a", "b"]


def test_should_iterate_over_empty_schema() -> None:
    schema = Schema({})
    assert list(schema) == []
