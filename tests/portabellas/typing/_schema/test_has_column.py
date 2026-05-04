from portabellas.typing import DataTypes, Schema


def test_should_return_true_if_column_exists() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert schema.has_column("a") is True


def test_should_return_false_if_column_does_not_exist() -> None:
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Float32()})
    assert schema.has_column("c") is False
