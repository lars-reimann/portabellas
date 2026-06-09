import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    column = Column.zeros("col1", 3)
    assert column.name == "col1"


@pytest.mark.parametrize(
    ("count", "type_", "expected"),
    [
        pytest.param(0, None, [], id="zero count"),
        pytest.param(3, None, [0.0, 0.0, 0.0], id="non-zero count"),
        pytest.param(3, DataTypes.String(), ["0", "0", "0"], id="explicit type"),
    ],
)
def test_should_store_the_data(count: int, type_: DataType | None, expected: list[float]) -> None:
    column = Column.zeros("col1", count, type=type_)
    assert list(column) == expected


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(None, DataTypes.Float64(), id="inferred"),
        pytest.param(DataTypes.Int64(), DataTypes.Int64(), id="explicit"),
    ],
)
def test_should_have_correct_type(type_: DataType | None, expected: DataType) -> None:
    column = Column.zeros("col1", 3, type=type_)
    assert column.type == expected


def test_should_raise_for_negative_count() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.zeros("col1", -1)
