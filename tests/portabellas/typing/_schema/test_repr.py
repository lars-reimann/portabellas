from portabellas.typing import DataTypes, Schema


def test_should_return_repr() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert repr(schema) == f"Schema({schema!s})"


def test_should_return_repr_for_empty_schema() -> None:
    schema = Schema({})
    assert repr(schema) == f"Schema({schema!s})"
