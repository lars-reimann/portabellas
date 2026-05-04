import pytest

from portabellas.typing import DataType
from portabellas.typing._data_type import DatetimeType


@pytest.mark.parametrize(
    ("type_", "expected_time_zone"),
    [
        pytest.param(DataType.Datetime(), None, id="local time"),
        pytest.param(DataType.Datetime(time_zone="UTC"), "UTC", id="UTC"),
        pytest.param(DataType.Datetime(time_zone="Europe/Berlin"), "Europe/Berlin", id="Europe/Berlin"),
    ],
)
def test_should_return_time_zone(type_: DatetimeType, expected_time_zone: str | None) -> None:
    assert type_.time_zone == expected_time_zone
