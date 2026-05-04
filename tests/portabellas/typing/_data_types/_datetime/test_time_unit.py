import polars as pl
import pytest

from portabellas.typing import DataTypes
from portabellas.typing._data_type import _from_polars_data_type


@pytest.mark.parametrize(
    ("type_", "expected_time_unit"),
    [
        pytest.param(DataTypes.Datetime(time_unit="ms"), "ms", id="milliseconds"),
        pytest.param(DataTypes.Datetime(time_unit="us"), "us", id="microseconds"),
        pytest.param(DataTypes.Datetime(time_unit="ns"), "ns", id="nanoseconds"),
    ],
)
def test_should_return_time_unit(type_: DataTypes.Datetime, expected_time_unit: str) -> None:
    assert type_.time_unit == expected_time_unit


@pytest.mark.parametrize(
    ("polars_dtype", "expected_time_unit"),
    [
        pytest.param(pl.Datetime("ms"), "ms", id="ms"),
        pytest.param(pl.Datetime("us"), "us", id="us"),
        pytest.param(pl.Datetime("ns"), "ns", id="ns"),
    ],
)
def test_should_preserve_time_unit_from_polars_dtype(polars_dtype: pl.Datetime, expected_time_unit: str) -> None:
    result = _from_polars_data_type(polars_dtype)
    assert isinstance(result, DataTypes.Datetime)
    assert result.time_unit == expected_time_unit
