import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    column = Column.repeat("col1", 1, 3)
    assert column.name == "col1"


@pytest.mark.parametrize(
    ("value", "count", "type_", "expected"),
    [
        pytest.param(2, 0, None, [], id="zero count"),
        pytest.param(2, 3, None, [2, 2, 2], id="non-zero count"),
        pytest.param(2, 3, DataTypes.String(), ["2", "2", "2"], id="explicit type"),
    ],
)
def test_should_store_the_data(value: object, count: int, type_: DataType | None, expected: list[float]) -> None:
    column = Column.repeat("col1", value, count, type=type_)
    assert list(column) == expected


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        pytest.param(2, None, DataTypes.Int32(), id="inferred"),
        pytest.param(2, DataTypes.String(), DataTypes.String(), id="explicit"),
    ],
)
def test_should_have_correct_type(value: object, type_: DataType | None, expected: DataType) -> None:
    column = Column.repeat("col1", value, 3, type=type_)
    assert column.type == expected


def test_should_raise_for_negative_count() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.repeat("col1", 1, -1)
