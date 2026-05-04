from collections.abc import Callable

import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    "type_factory",
    [
        pytest.param(lambda: DataTypes.ExperimentalFloat16(), id="Float16"),
        pytest.param(lambda: DataTypes.Float32(), id="Float32"),
        pytest.param(lambda: DataTypes.Float64(), id="Float64"),
        pytest.param(lambda: DataTypes.Int8(), id="Int8"),
        pytest.param(lambda: DataTypes.Int16(), id="Int16"),
        pytest.param(lambda: DataTypes.Int32(), id="Int32"),
        pytest.param(lambda: DataTypes.Int64(), id="Int64"),
        pytest.param(lambda: DataTypes.ExperimentalInt128(), id="Int128"),
        pytest.param(lambda: DataTypes.UInt8(), id="UInt8"),
        pytest.param(lambda: DataTypes.UInt16(), id="UInt16"),
        pytest.param(lambda: DataTypes.UInt32(), id="UInt32"),
        pytest.param(lambda: DataTypes.UInt64(), id="UInt64"),
        pytest.param(lambda: DataTypes.Date(), id="Date"),
        pytest.param(lambda: DataTypes.Datetime(), id="Datetime"),
        pytest.param(lambda: DataTypes.Duration("us"), id="Duration"),
        pytest.param(lambda: DataTypes.Time(), id="Time"),
        pytest.param(lambda: DataTypes.String(), id="String"),
        pytest.param(lambda: DataTypes.Binary(), id="Binary"),
        pytest.param(lambda: DataTypes.Boolean(), id="Boolean"),
        pytest.param(lambda: DataTypes.Null(), id="Null"),
        pytest.param(lambda: DataTypes.List(DataTypes.Int64()), id="List"),
        pytest.param(
            lambda: DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}), id="Struct"
        ),
    ],
)
def test_should_return_same_hash_for_equal_objects(type_factory: Callable[[], DataType]) -> None:
    type_1 = type_factory()
    type_2 = type_factory()
    assert hash(type_1) == hash(type_2)


@pytest.mark.parametrize(
    ("type_1", "type_2"),
    [
        pytest.param(DataTypes.Float32(), DataTypes.Float64(), id="different bit count"),
        pytest.param(DataTypes.Float32(), DataTypes.Int32(), id="float vs. int"),
        pytest.param(DataTypes.Int32(), DataTypes.UInt32(), id="signed vs. unsigned"),
        pytest.param(DataTypes.Int32(), DataTypes.String(), id="numeric vs. non-numeric"),
        pytest.param(
            DataTypes.List(DataTypes.Int64()),
            DataTypes.List(DataTypes.String()),
            id="list with different inner type",
        ),
        pytest.param(
            DataTypes.Struct(fields={"a": DataTypes.String()}),
            DataTypes.Struct(fields={"a": DataTypes.String(), "b": DataTypes.Int64()}),
            id="struct with different field count",
        ),
    ],
)
def test_should_be_good_hash(
    type_1: DataType,
    type_2: DataType,
) -> None:
    assert hash(type_1) != hash(type_2)
