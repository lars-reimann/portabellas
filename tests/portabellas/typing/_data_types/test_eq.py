from typing import Any

import pytest

from portabellas.containers import Column, Table
from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_1", "type_2", "expected"),
    [
        pytest.param(
            DataTypes.Float32(),
            DataTypes.Float32(),
            True,
            id="equal",
        ),
        pytest.param(
            DataTypes.Float32(),
            DataTypes.Float64(),
            False,
            id="not equal (different bit count)",
        ),
        pytest.param(
            DataTypes.Float32(),
            DataTypes.Int32(),
            False,
            id="not equal (float vs. int)",
        ),
        pytest.param(
            DataTypes.Int32(),
            DataTypes.UInt32(),
            False,
            id="not equal (signed vs. unsigned)",
        ),
        pytest.param(
            DataTypes.Int32(),
            DataTypes.String(),
            False,
            id="not equal (numeric vs. non-numeric)",
        ),
        pytest.param(
            DataTypes.List(DataTypes.Int64()),
            DataTypes.List(DataTypes.String()),
            False,
            id="not equal (list with different inner type)",
        ),
        pytest.param(
            DataTypes.List(DataTypes.Int64()),
            DataTypes.Int64(),
            False,
            id="not equal (list vs. non-list)",
        ),
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int32()}),
            False,
            id="not equal (struct with different field type)",
        ),
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String()}),
            DataTypes.String(),
            False,
            id="not equal (struct vs. non-struct)",
        ),
    ],
)
def test_should_return_whether_objects_are_equal(type_1: Table, type_2: Table, expected: bool) -> None:
    assert (type_1.__eq__(type_2)) == expected


@pytest.mark.parametrize(
    "type_",
    [
        pytest.param(DataTypes.Float32(), id="Float32"),
        pytest.param(DataTypes.Float64(), id="Float64"),
        pytest.param(DataTypes.Int8(), id="Int8"),
        pytest.param(DataTypes.Int16(), id="Int16"),
        pytest.param(DataTypes.Int32(), id="Int32"),
        pytest.param(DataTypes.Int64(), id="Int64"),
        pytest.param(DataTypes.ExperimentalInt128(), id="Int128"),
        pytest.param(DataTypes.UInt8(), id="UInt8"),
        pytest.param(DataTypes.UInt16(), id="UInt16"),
        pytest.param(DataTypes.UInt32(), id="UInt32"),
        pytest.param(DataTypes.UInt64(), id="UInt64"),
        pytest.param(DataTypes.Date(), id="Date"),
        pytest.param(DataTypes.Datetime(), id="Datetime"),
        pytest.param(DataTypes.Duration("us"), id="Duration"),
        pytest.param(DataTypes.Time(), id="Time"),
        pytest.param(DataTypes.String(), id="String"),
        pytest.param(DataTypes.Binary(), id="Binary"),
        pytest.param(DataTypes.Boolean(), id="Boolean"),
        pytest.param(DataTypes.Null(), id="Null"),
        pytest.param(DataTypes.List(DataTypes.Int64()), id="List"),
        pytest.param(DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}), id="Struct"),
    ],
)
def test_should_return_true_if_objects_are_identical(type_: DataType) -> None:
    assert (type_.__eq__(type_)) is True


@pytest.mark.parametrize(
    ("type_", "other"),
    [
        pytest.param(DataTypes.Null(), None, id="DataType vs. None"),
        pytest.param(DataTypes.Null(), Column("col1", []), id="DataType vs. Column"),
    ],
)
def test_should_return_not_implemented_if_other_has_different_type(type_: DataType, other: Any) -> None:
    assert (type_.__eq__(other)) is NotImplemented
