from portabellas.typing import DataType, Schema


def test_should_return_true_if_column_exists() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema.has_column("a") is True


def test_should_return_false_if_column_does_not_exist() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema.has_column("c") is False
