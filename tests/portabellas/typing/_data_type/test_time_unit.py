import pytest

from portabellas.typing import DataType
from portabellas.typing._data_type import Duration


@pytest.mark.parametrize(
    ("type_", "expected_time_unit"),
    [
        pytest.param(DataType.Duration("ms"), "ms", id="milliseconds"),
        pytest.param(DataType.Duration("us"), "us", id="microseconds"),
        pytest.param(DataType.Duration("ns"), "ns", id="nanoseconds"),
    ],
)
def test_should_return_time_unit(type_: Duration, expected_time_unit: str) -> None:
    assert type_.time_unit == expected_time_unit
