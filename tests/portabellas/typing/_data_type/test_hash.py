from collections.abc import Callable

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    "type_factory",
    [
        pytest.param(lambda: DataType.Float32(), id="Float32"),
        pytest.param(lambda: DataType.Float64(), id="Float64"),
        pytest.param(lambda: DataType.Int8(), id="Int8"),
        pytest.param(lambda: DataType.Int16(), id="Int16"),
        pytest.param(lambda: DataType.Int32(), id="Int32"),
        pytest.param(lambda: DataType.Int64(), id="Int64"),
        pytest.param(lambda: DataType.experimental_Int128(), id="Int128"),
        pytest.param(lambda: DataType.UInt8(), id="UInt8"),
        pytest.param(lambda: DataType.UInt16(), id="UInt16"),
        pytest.param(lambda: DataType.UInt32(), id="UInt32"),
        pytest.param(lambda: DataType.UInt64(), id="UInt64"),
        pytest.param(lambda: DataType.Date(), id="Date"),
        pytest.param(lambda: DataType.Datetime(), id="Datetime"),
        pytest.param(lambda: DataType.Duration("us"), id="Duration"),
        pytest.param(lambda: DataType.Time(), id="Time"),
        pytest.param(lambda: DataType.String(), id="String"),
        pytest.param(lambda: DataType.Binary(), id="Binary"),
        pytest.param(lambda: DataType.Boolean(), id="Boolean"),
        pytest.param(lambda: DataType.Null(), id="Null"),
    ],
)
def test_should_return_same_hash_for_equal_objects(type_factory: Callable[[], DataType]) -> None:
    type_1 = type_factory()
    type_2 = type_factory()
    assert hash(type_1) == hash(type_2)


@pytest.mark.parametrize(
    ("type_1", "type_2"),
    [
        pytest.param(DataType.Float32(), DataType.Float64(), id="different bit count"),
        pytest.param(DataType.Float32(), DataType.Int32(), id="float vs. int"),
        pytest.param(DataType.Int32(), DataType.UInt32(), id="signed vs. unsigned"),
        pytest.param(DataType.Int32(), DataType.String(), id="numeric vs. non-numeric"),
    ],
)
def test_should_be_good_hash(
    type_1: DataType,
    type_2: DataType,
) -> None:
    assert hash(type_1) != hash(type_2)
