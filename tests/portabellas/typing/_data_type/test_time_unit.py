import polars as pl
import pytest

from portabellas.typing import DataTypes
from portabellas.typing._data_type import _from_polars_data_type


@pytest.mark.parametrize(
    ("type_", "expected_time_unit"),
    [
        pytest.param(DataTypes.Datetime("ms"), "ms", id="datetime-ms"),
        pytest.param(DataTypes.Datetime("us"), "us", id="datetime-us"),
        pytest.param(DataTypes.Datetime("ns"), "ns", id="datetime-ns"),
        pytest.param(DataTypes.Duration("ms"), "ms", id="duration-ms"),
        pytest.param(DataTypes.Duration("us"), "us", id="duration-us"),
        pytest.param(DataTypes.Duration("ns"), "ns", id="duration-ns"),
    ],
)
def test_should_return_time_unit(type_: DataTypes.Duration | DataTypes.Datetime, expected_time_unit: str) -> None:
    assert type_.time_unit == expected_time_unit


@pytest.mark.parametrize(
    ("polars_dtype", "expected_time_unit"),
    [
        pytest.param(pl.Datetime("ms"), "ms", id="datetime-ms"),
        pytest.param(pl.Datetime("us"), "us", id="datetime-us"),
        pytest.param(pl.Datetime("ns"), "ns", id="datetime-ns"),
        pytest.param(pl.Duration("ms"), "ms", id="duration-ms"),
        pytest.param(pl.Duration("us"), "us", id="duration-us"),
        pytest.param(pl.Duration("ns"), "ns", id="duration-ns"),
    ],
)
def test_should_preserve_time_unit_from_polars_dtype(
    polars_dtype: pl.Datetime | pl.Duration, expected_time_unit: str
) -> None:
    result = _from_polars_data_type(polars_dtype)
    assert isinstance(result, (DataTypes.Datetime, DataTypes.Duration))
    assert result.time_unit == expected_time_unit
