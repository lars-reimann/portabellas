import polars as pl
import pytest

from portabellas.typing import DataTypes
from portabellas.typing._data_type import _from_polars_data_type


@pytest.mark.parametrize(
    ("type_", "expected_time_unit"),
    [
        pytest.param(DataTypes.Duration("ms"), "ms", id="milliseconds"),
        pytest.param(DataTypes.Duration("us"), "us", id="microseconds"),
        pytest.param(DataTypes.Duration("ns"), "ns", id="nanoseconds"),
    ],
)
def test_should_return_time_unit(type_: DataTypes.Duration, expected_time_unit: str) -> None:
    assert type_.time_unit == expected_time_unit


@pytest.mark.parametrize(
    ("polars_dtype", "expected_time_unit"),
    [
        pytest.param(pl.Duration("ms"), "ms", id="ms"),
        pytest.param(pl.Duration("us"), "us", id="us"),
        pytest.param(pl.Duration("ns"), "ns", id="ns"),
    ],
)
def test_should_preserve_time_unit_from_polars_dtype(polars_dtype: pl.Duration, expected_time_unit: str) -> None:
    result = _from_polars_data_type(polars_dtype)
    assert isinstance(result, DataTypes.Duration)
    assert result.time_unit == expected_time_unit
