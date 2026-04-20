from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from portabellas import Column

if TYPE_CHECKING:
    from typing import Any


@pytest.mark.parametrize(
    ("values", "ignore_missing_values", "expected"),
    [
        pytest.param([], True, [], id="empty"),
        pytest.param([1, 2, 3], True, [1, 2, 3], id="no duplicates"),
        pytest.param([1, 2, 1], True, [1, 2], id="some duplicate"),
        pytest.param([1, 2, 3, None], True, [1, 2, 3], id="with missing values (ignored)"),
        pytest.param([1, 2, 3, None], False, [1, 2, 3, None], id="with missing values (not ignored)"),
        pytest.param([None], True, [], id="only missing values (ignored)"),
        pytest.param([None], False, [None], id="only missing values (not ignored)"),
    ],
)
def test_should_return_distinct_values(
    values: list[Any],
    ignore_missing_values: bool,
    expected: list[Any],
) -> None:
    column: Column = Column("col1", values)
    assert column.distinct_values(ignore_missing_values=ignore_missing_values) == expected
