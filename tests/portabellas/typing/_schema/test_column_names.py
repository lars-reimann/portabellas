from portabellas.typing import DataType, Schema


def test_should_return_column_names() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema.column_names == ["a", "b"]


def test_should_return_empty_list_for_empty_schema() -> None:
    schema = Schema({})
    assert schema.column_names == []


def test_should_return_defensive_copy() -> None:
    schema = Schema({"a": DataType.Int64()})
    names = schema.column_names
    names.append("b")
    assert schema.column_names == ["a"]
