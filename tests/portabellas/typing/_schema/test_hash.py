from portabellas.typing import DataType, Schema


def test_should_return_same_hash_for_equal_schemas() -> None:
    schema1 = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    schema2 = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert hash(schema1) == hash(schema2)


def test_should_return_different_hash_for_different_schemas() -> None:
    schema1 = Schema({"a": DataType.Int64()})
    schema2 = Schema({"a": DataType.Float64()})
    assert hash(schema1) != hash(schema2)


def test_should_be_usable_in_set() -> None:
    schema1 = Schema({"a": DataType.Int64()})
    schema2 = Schema({"a": DataType.Int64()})
    schema3 = Schema({"b": DataType.Float64()})
    schema_set = {schema1, schema2, schema3}
    assert len(schema_set) == 2
