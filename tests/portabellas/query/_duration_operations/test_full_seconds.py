from datetime import timedelta

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(timedelta(seconds=1), 1, id="positive, exact"),
        pytest.param(timedelta(seconds=1, milliseconds=500), 1, id="positive, rounded"),
        pytest.param(timedelta(seconds=-1), -1, id="negative, exact"),
        pytest.param(timedelta(seconds=-1, milliseconds=-500), -1, id="negative, rounded"),
        pytest.param(timedelta(seconds=1, milliseconds=-500), 0, id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_full_seconds(value: timedelta | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value, lambda cell: cell.dur.full_seconds(), expected, type_if_none=DataType.Duration("us")
    )
