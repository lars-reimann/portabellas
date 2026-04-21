from datetime import timedelta
from typing import Literal

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param(timedelta(weeks=1), "iso", "P7D", id="iso - positive weeks"),
        pytest.param(timedelta(weeks=-1), "iso", "-P7D", id="iso - negative weeks"),
        pytest.param(timedelta(days=1), "iso", "P1D", id="iso - positive days"),
        pytest.param(timedelta(days=-1), "iso", "-P1D", id="iso - negative days"),
        pytest.param(timedelta(hours=1), "iso", "PT1H", id="iso - positive hours"),
        pytest.param(timedelta(hours=-1), "iso", "-PT1H", id="iso - negative hours"),
        pytest.param(timedelta(minutes=1), "iso", "PT1M", id="iso - positive minutes"),
        pytest.param(timedelta(minutes=-1), "iso", "-PT1M", id="iso - negative minutes"),
        pytest.param(timedelta(seconds=1), "iso", "PT1S", id="iso - positive seconds"),
        pytest.param(timedelta(seconds=-1), "iso", "-PT1S", id="iso - negative seconds"),
        pytest.param(timedelta(milliseconds=1), "iso", "PT0.001S", id="iso - positive milliseconds"),
        pytest.param(timedelta(milliseconds=-1), "iso", "-PT0.001S", id="iso - negative milliseconds"),
        pytest.param(timedelta(microseconds=1), "iso", "PT0.000001S", id="iso - positive microseconds"),
        pytest.param(timedelta(microseconds=-1), "iso", "-PT0.000001S", id="iso - negative microseconds"),
        pytest.param(
            timedelta(weeks=1, days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1),
            "iso",
            "P8DT1H1M1.001001S",
            id="iso - all positive",
        ),
        pytest.param(
            timedelta(weeks=-1, days=-1, hours=-1, minutes=-1, seconds=-1, milliseconds=-1, microseconds=-1),
            "iso",
            "-P8DT1H1M1.001001S",
            id="iso - all negative",
        ),
        pytest.param(
            timedelta(weeks=1, days=-1, hours=1, minutes=-1, seconds=1, milliseconds=-1, microseconds=1),
            "iso",
            "P6DT59M0.999001S",
            id="iso - mixed",
        ),
        pytest.param(None, "iso", None, id="iso - None"),
        pytest.param(timedelta(weeks=1), "pretty", "7d", id="pretty - positive weeks"),
        pytest.param(timedelta(weeks=-1), "pretty", "-7d", id="pretty - negative weeks"),
        pytest.param(timedelta(days=1), "pretty", "1d", id="pretty - positive days"),
        pytest.param(timedelta(days=-1), "pretty", "-1d", id="pretty - negative days"),
        pytest.param(timedelta(hours=1), "pretty", "1h", id="pretty - positive hours"),
        pytest.param(timedelta(hours=-1), "pretty", "-1h", id="pretty - negative hours"),
        pytest.param(timedelta(minutes=1), "pretty", "1m", id="pretty - positive minutes"),
        pytest.param(timedelta(minutes=-1), "pretty", "-1m", id="pretty - negative minutes"),
        pytest.param(timedelta(seconds=1), "pretty", "1s", id="pretty - positive seconds"),
        pytest.param(timedelta(seconds=-1), "pretty", "-1s", id="pretty - negative seconds"),
        pytest.param(timedelta(milliseconds=1), "pretty", "1ms", id="pretty - positive milliseconds"),
        pytest.param(timedelta(milliseconds=-1), "pretty", "-1ms", id="pretty - negative milliseconds"),
        pytest.param(timedelta(microseconds=1), "pretty", "1µs", id="pretty - positive microseconds"),
        pytest.param(timedelta(microseconds=-1), "pretty", "-1µs", id="pretty - negative microseconds"),
        pytest.param(
            timedelta(weeks=1, days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1),
            "pretty",
            "8d 1h 1m 1s 1001µs",
            id="pretty - all positive",
        ),
        pytest.param(
            timedelta(weeks=-1, days=-1, hours=-1, minutes=-1, seconds=-1, milliseconds=-1, microseconds=-1),
            "pretty",
            "-8d -1h -1m -1s -1001µs",
            id="pretty - all negative",
        ),
        pytest.param(
            timedelta(weeks=1, days=-1, hours=1, minutes=-1, seconds=1, milliseconds=-1, microseconds=1),
            "pretty",
            "6d 59m 999001µs",
            id="pretty - mixed",
        ),
        pytest.param(None, "pretty", None, id="pretty - None"),
    ],
)
def test_should_return_string_representation(
    value: timedelta | None,
    format_: Literal["iso", "pretty"],
    expected: str | None,
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.dur.to_string(format=format_),
        expected,
        type_if_none=DataType.Duration("us"),
    )
