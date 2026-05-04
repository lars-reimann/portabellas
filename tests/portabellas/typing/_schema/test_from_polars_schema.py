import polars as pl

from portabellas.typing import DataTypes, Schema


def test_should_create_schema_from_polars_schema() -> None:
    polars_schema = pl.Schema({"a": pl.Int64(), "b": pl.Float32()})
    schema = Schema._from_polars_schema(polars_schema)
    assert schema.column_names == ["a", "b"]
    assert schema["a"] == DataTypes.Int64()
    assert schema["b"] == DataTypes.Float32()


def test_should_create_empty_schema_from_empty_polars_schema() -> None:
    polars_schema = pl.Schema()
    schema = Schema._from_polars_schema(polars_schema)
    assert schema.column_count == 0
