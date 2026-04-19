from portabellas.typing import DataType, Schema


def test_should_return_str_for_empty_schema() -> None:
    schema = Schema({})
    assert str(schema) == "{}"


def test_should_return_str_for_single_column_schema() -> None:
    schema = Schema({"a": DataType.Int64()})
    assert str(schema) == "{'a': i64}"


def test_should_return_str_for_multi_column_schema() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    result = str(schema)
    assert result.startswith("{")
    assert result.endswith("}")
    assert "'a': i64" in result
    assert "'b': f32" in result
