import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    column = Column.ones("col1", 3)
    assert column.name == "col1"


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        pytest.param(0, [], id="zero count"),
        pytest.param(3, [1.0, 1.0, 1.0], id="non-zero count"),
    ],
)
def test_should_store_the_data(count: int, expected: list[float]) -> None:
    column = Column.ones("col1", count)
    assert list(column) == expected


@pytest.mark.parametrize(
    ("type", "expected"),
    [
        pytest.param(None, DataTypes.Float64(), id="default (None)"),
        pytest.param(DataTypes.Int64(), DataTypes.Int64(), id="explicit Int64"),
        pytest.param(DataTypes.Int32(), DataTypes.Int32(), id="explicit Int32"),
    ],
)
def test_should_have_correct_type(type: DataType | None, expected: DataType) -> None:  # noqa: A002
    column = Column.ones("col1", 3, type=type)
    assert column.type == expected


def test_should_raise_for_negative_count() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.ones("col1", -1)
