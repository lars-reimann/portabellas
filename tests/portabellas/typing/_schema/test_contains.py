from portabellas.typing import DataType, Schema


def test_should_return_true_if_column_exists() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert "a" in schema


def test_should_return_false_if_column_does_not_exist() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert "c" not in schema


def test_should_return_false_if_key_is_not_a_string() -> None:
    schema = Schema({"a": DataType.Int64()})
    assert 1 not in schema  # type: ignore[comparison-overlap]
