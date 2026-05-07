from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

import pytest

from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    ("value", "unit", "expected"),
    [
        pytest.param(datetime(1970, 1, 1), "s", 0, id="epoch in seconds"),  # noqa: DTZ001
        pytest.param(datetime(1970, 1, 2), "s", 86400, id="day after epoch in seconds"),  # noqa: DTZ001
        pytest.param(None, "s", None, id="None in seconds"),
        pytest.param(datetime(1970, 1, 1), "ms", 0, id="epoch in milliseconds"),  # noqa: DTZ001
        pytest.param(datetime(1970, 1, 2), "ms", 86400000, id="day after epoch in milliseconds"),  # noqa: DTZ001
        pytest.param(None, "ms", None, id="None in milliseconds"),
        pytest.param(datetime(1970, 1, 1), "us", 0, id="epoch in microseconds"),  # noqa: DTZ001
        pytest.param(datetime(1970, 1, 2), "us", 86400000000, id="day after epoch in microseconds"),  # noqa: DTZ001
        pytest.param(None, "us", None, id="None in microseconds"),
    ],
)
def test_should_return_unix_timestamp(
    value: datetime | None, unit: Literal["s", "ms", "us"], expected: int | None
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.dt.unix_timestamp(unit=unit),
        expected,
        type_if_none=DataTypes.Datetime(),
    )


@pytest.mark.parametrize(
    ("operation", "expected_type"),
    [
        pytest.param(lambda cell: cell.dt.unix_timestamp(unit="s"), DataTypes.Int64(), id="s"),
        pytest.param(lambda cell: cell.dt.unix_timestamp(unit="ms"), DataTypes.Int64(), id="ms"),
        pytest.param(lambda cell: cell.dt.unix_timestamp(unit="us"), DataTypes.Int64(), id="us"),
    ],
)
def test_should_infer_type(operation: Callable, expected_type: DataType) -> None:
    result = operation(cell_of_type(DataTypes.Datetime()))
    assert_cell_has_type(result, expected_type)
