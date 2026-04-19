from portabellas.containers import Column
from portabellas.typing import DataType, Schema


def test_should_return_true_if_schemas_are_equal() -> None:
    schema1 = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    schema2 = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema1 == schema2


def test_should_return_true_if_same_object() -> None:
    schema = Schema({"a": DataType.Int64()})
    assert schema.__eq__(schema) is True


def test_should_return_false_if_schemas_have_different_column_names() -> None:
    schema1 = Schema({"a": DataType.Int64()})
    schema2 = Schema({"b": DataType.Int64()})
    assert schema1 != schema2


def test_should_return_false_if_schemas_have_different_column_types() -> None:
    schema1 = Schema({"a": DataType.Int64()})
    schema2 = Schema({"a": DataType.Float64()})
    assert schema1 != schema2


def test_should_return_false_if_schemas_have_different_column_count() -> None:
    schema1 = Schema({"a": DataType.Int64()})
    schema2 = Schema({"a": DataType.Int64(), "b": DataType.Float32()})
    assert schema1 != schema2


def test_should_return_not_implemented_if_other_is_not_schema() -> None:
    schema = Schema({"a": DataType.Int64()})
    assert schema.__eq__(Column("a", [])) is NotImplemented
