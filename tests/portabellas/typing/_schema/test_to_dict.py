from portabellas.typing import DataTypes, Schema


def test_should_return_dict() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    result = schema.to_dict()
    assert result == {"a": DataTypes.Int64(), "b": DataTypes.Float32()}


def test_should_return_empty_dict_for_empty_schema() -> None:
    schema = Schema({})
    assert schema.to_dict() == {}
