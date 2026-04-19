import pytest

from portabellas.typing import DataType


def test_should_raise_if_time_zone_is_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid time zone"):
        DataType.Datetime(time_zone="invalid")


def test_should_suggest_similar_time_zone() -> None:
    with pytest.raises(ValueError, match="Europe/Berlin"):
        DataType.Datetime(time_zone="Europe/Berlinx")
