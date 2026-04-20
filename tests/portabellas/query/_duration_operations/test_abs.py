from datetime import timedelta

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(timedelta(days=1), timedelta(days=1), id="positive days"),
        pytest.param(timedelta(days=1, hours=12), timedelta(days=1, hours=12), id="positive days and hours"),
        pytest.param(timedelta(days=-1), timedelta(days=1), id="negative days"),
        pytest.param(timedelta(days=-1, hours=-12), timedelta(days=1, hours=12), id="negative days and hours"),
        pytest.param(timedelta(days=1, hours=-12), timedelta(hours=12), id="positive days, negative hours"),
        pytest.param(timedelta(days=-1, hours=12), timedelta(hours=12), id="negative days, positive hours"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_absolute_duration(value: timedelta | None, expected: timedelta | None) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(value, lambda cell: cell.dur.abs(), expected, type_if_none=DataType.Duration("us"))
