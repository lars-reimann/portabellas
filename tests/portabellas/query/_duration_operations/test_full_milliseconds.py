from datetime import timedelta

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(timedelta(milliseconds=1), 1, id="positive, exact"),
        pytest.param(timedelta(milliseconds=1, microseconds=500), 1, id="positive, rounded"),
        pytest.param(timedelta(milliseconds=-1), -1, id="negative, exact"),
        pytest.param(timedelta(milliseconds=-1, microseconds=-500), -1, id="negative, rounded"),
        pytest.param(timedelta(milliseconds=1, microseconds=-500), 0, id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_full_milliseconds(value: timedelta | None, expected: int | None) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(
        value,
        lambda cell: cell.dur.full_milliseconds(),
        expected,
        type_if_none=DataType.Duration("us"),
    )
