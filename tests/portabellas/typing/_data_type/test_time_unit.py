import pytest

from portabellas.typing import DataTypes


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
