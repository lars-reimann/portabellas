from typing import Any

import pytest

from portabellas.containers import Column, Table
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_1", "type_2", "expected"),
    [
        pytest.param(
            DataType.Float32(),
            DataType.Float32(),
            True,
            id="equal",
        ),
        pytest.param(
            DataType.Float32(),
            DataType.Float64(),
            False,
            id="not equal (different bit count)",
        ),
        pytest.param(
            DataType.Float32(),
            DataType.Int32(),
            False,
            id="not equal (float vs. int)",
        ),
        pytest.param(
            DataType.Int32(),
            DataType.UInt32(),
            False,
            id="not equal (signed vs. unsigned)",
        ),
        pytest.param(
            DataType.Int32(),
            DataType.String(),
            False,
            id="not equal (numeric vs. non-numeric)",
        ),
        pytest.param(
            DataType.List(DataType.Int64()),
            DataType.List(DataType.String()),
            False,
            id="not equal (list with different inner type)",
        ),
        pytest.param(
            DataType.List(DataType.Int64()),
            DataType.Int64(),
            False,
            id="not equal (list vs. non-list)",
        ),
        pytest.param(
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}),
            DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int32()}),
            False,
            id="not equal (struct with different field type)",
        ),
        pytest.param(
            DataType.Struct(fields={"name": DataType.String()}),
            DataType.String(),
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
        pytest.param(DataType.Float32(), id="Float32"),
        pytest.param(DataType.Float64(), id="Float64"),
        pytest.param(DataType.Int8(), id="Int8"),
        pytest.param(DataType.Int16(), id="Int16"),
        pytest.param(DataType.Int32(), id="Int32"),
        pytest.param(DataType.Int64(), id="Int64"),
        pytest.param(DataType.experimental_Int128(), id="Int128"),
        pytest.param(DataType.UInt8(), id="UInt8"),
        pytest.param(DataType.UInt16(), id="UInt16"),
        pytest.param(DataType.UInt32(), id="UInt32"),
        pytest.param(DataType.UInt64(), id="UInt64"),
        pytest.param(DataType.Date(), id="Date"),
        pytest.param(DataType.Datetime(), id="Datetime"),
        pytest.param(DataType.Duration("us"), id="Duration"),
        pytest.param(DataType.Time(), id="Time"),
        pytest.param(DataType.String(), id="String"),
        pytest.param(DataType.Binary(), id="Binary"),
        pytest.param(DataType.Boolean(), id="Boolean"),
        pytest.param(DataType.Null(), id="Null"),
        pytest.param(DataType.List(DataType.Int64()), id="List"),
        pytest.param(DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}), id="Struct"),
    ],
)
def test_should_return_true_if_objects_are_identical(type_: DataType) -> None:
    assert (type_.__eq__(type_)) is True


@pytest.mark.parametrize(
    ("type_", "other"),
    [
        pytest.param(DataType.Null(), None, id="DataType vs. None"),
        pytest.param(DataType.Null(), Column("col1", []), id="DataType vs. Column"),
    ],
)
def test_should_return_not_implemented_if_other_has_different_type(type_: DataType, other: Any) -> None:
    assert (type_.__eq__(other)) is NotImplemented
