from portabellas.typing import DataType, Schema


def test_should_return_markdown_for_non_empty_schema() -> None:
    schema = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    result = schema._repr_markdown_()
    assert "| Column Name | Column Type |" in result
    assert "| --- | --- |" in result
    assert "| a | Int64 |" in result
    assert "| b | Float32 |" in result


def test_should_return_empty_schema_for_empty_schema() -> None:
    schema = Schema({})
    assert schema._repr_markdown_() == "Empty schema"
