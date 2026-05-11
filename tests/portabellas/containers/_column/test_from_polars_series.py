import polars as pl
import pytest

from portabellas import Column
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    series = pl.Series("col1", [])
    assert Column._from_polars_series(series).name == "col1"


@pytest.mark.parametrize(
    ("series", "expected"),
    [
        pytest.param(
            pl.Series([]),
            [],
            id="empty",
        ),
        pytest.param(
            pl.Series([True]),
            [True],
            id="non-empty",
        ),
    ],
)
def test_should_store_the_data(series: pl.Series, expected: list) -> None:
    assert list(Column._from_polars_series(series)) == expected


def test_should_have_correct_type() -> None:
    series = pl.Series("col1", [1])
    assert Column._from_polars_series(series).type == DataTypes.Int64()


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataTypes.Int64(), DataTypes.Int64(), id="matching type"),
    ],
)
def test_should_use_provided_type_over_polars_dtype(type_: DataType, expected: DataType) -> None:
    series = pl.Series("col1", [1, 2, 3])
    result = Column._from_polars_series(series, type=type_)
    assert result.type == expected
