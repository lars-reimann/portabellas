from datetime import timedelta

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(timedelta(minutes=1), 1, id="positive, exact"),
        pytest.param(timedelta(minutes=1, seconds=30), 1, id="positive, rounded"),
        pytest.param(timedelta(minutes=-1), -1, id="negative, exact"),
        pytest.param(timedelta(minutes=-1, seconds=-30), -1, id="negative, rounded"),
        pytest.param(timedelta(minutes=1, seconds=-30), 0, id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_full_minutes(value: timedelta | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value, lambda cell: cell.dur.full_minutes(), expected, type_if_none=DataTypes.Duration("us")
    )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Duration("us")).dur.full_minutes()
    assert_cell_has_type(result, DataTypes.Int64())
