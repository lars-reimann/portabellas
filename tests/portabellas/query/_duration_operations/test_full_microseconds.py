from datetime import timedelta

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(timedelta(microseconds=1), 1, id="positive, exact"),
        pytest.param(timedelta(microseconds=-1), -1, id="negative, exact"),
        pytest.param(timedelta(milliseconds=1, microseconds=-500), 500, id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_full_microseconds(value: timedelta | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.dur.full_microseconds(),
        expected,
        type_if_none=DataTypes.Duration("us"),
    )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Duration("us")).dur.full_microseconds()
    assert_cell_has_type(result, DataTypes.Int64())
