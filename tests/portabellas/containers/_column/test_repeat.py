import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    column = Column.repeat("col1", 1, 3)
    assert column.name == "col1"


@pytest.mark.parametrize(
    ("value", "count", "expected"),
    [
        pytest.param(1, 0, [], id="zero count"),
        pytest.param(1, 3, [1, 1, 1], id="int"),
        pytest.param(1.5, 2, [1.5, 1.5], id="float"),
        pytest.param("a", 2, ["a", "a"], id="string"),
        pytest.param(True, 2, [True, True], id="bool"),
        pytest.param(None, 2, [None, None], id="none"),
    ],
)
def test_should_store_the_data(value: object, count: int, expected: list[object]) -> None:
    column = Column.repeat("col1", value, count)
    assert list(column) == expected


@pytest.mark.parametrize(
    ("value", "count", "expected"),
    [
        pytest.param(1, 3, DataTypes.Int32(), id="int"),
        pytest.param(1.5, 2, DataTypes.Float64(), id="float"),
        pytest.param("a", 2, DataTypes.String(), id="string"),
        pytest.param(True, 2, DataTypes.Boolean(), id="bool"),
        pytest.param(None, 2, DataTypes.Null(), id="none"),
    ],
)
def test_should_infer_type_from_value(value: object, count: int, expected: DataType) -> None:
    column = Column.repeat("col1", value, count)
    assert column.type == expected


@pytest.mark.parametrize(
    ("value", "type", "expected"),
    [
        pytest.param(1, DataTypes.Int64(), DataTypes.Int64(), id="int to Int64"),
        pytest.param(1, DataTypes.Float64(), DataTypes.Float64(), id="int to Float64"),
        pytest.param(1.5, DataTypes.String(), DataTypes.String(), id="float to String"),
    ],
)
def test_should_use_explicit_type(value: object, type: DataType, expected: DataType) -> None:  # noqa: A002
    column = Column.repeat("col1", value, 3, type=type)
    assert column.type == expected


@pytest.mark.parametrize(
    ("value", "type", "expected"),
    [
        pytest.param(1, DataTypes.String(), ["1", "1", "1"], id="int as String"),
        pytest.param(1.5, DataTypes.String(), ["1.5", "1.5", "1.5"], id="float as String"),
    ],
)
def test_should_cast_value_to_explicit_type(value: object, type: DataType, expected: list[str]) -> None:  # noqa: A002
    column = Column.repeat("col1", value, 3, type=type)
    assert list(column) == expected


def test_should_raise_for_negative_count() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.repeat("col1", 1, -1)
