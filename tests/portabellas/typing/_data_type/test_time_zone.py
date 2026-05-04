import pytest

from portabellas.typing import DataTypes


@pytest.mark.parametrize(
    ("type_", "expected_time_zone"),
    [
        pytest.param(DataTypes.Datetime(), None, id="local time"),
        pytest.param(DataTypes.Datetime(time_zone="UTC"), "UTC", id="UTC"),
        pytest.param(DataTypes.Datetime(time_zone="Europe/Berlin"), "Europe/Berlin", id="Europe/Berlin"),
    ],
)
def test_should_return_time_zone(type_: DataTypes.Datetime, expected_time_zone: str | None) -> None:
    assert type_.time_zone == expected_time_zone
