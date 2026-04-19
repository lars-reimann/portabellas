from portabellas.typing import DataType, Schema


def test_should_return_dict() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    result = schema.to_dict()
    assert result == {"a": DataType.Int64(), "b": DataType.Float32()}


def test_should_return_empty_dict_for_empty_schema() -> None:
    schema = Schema({})
    assert schema.to_dict() == {}
