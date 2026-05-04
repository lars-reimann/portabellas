from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from portabellas import Column

if TYPE_CHECKING:
    from typing import Any


@pytest.mark.parametrize(
    ("values", "ignore_nulls", "expected"),
    [
        pytest.param([], True, [], id="empty"),
        pytest.param([1, 2, 3], True, [1, 2, 3], id="no duplicates"),
        pytest.param([1, 2, 1], True, [1, 2], id="some duplicate"),
        pytest.param([1, 2, 3, None], True, [1, 2, 3], id="with nulls (ignored)"),
        pytest.param([1, 2, 3, None], False, [1, 2, 3, None], id="with nulls (not ignored)"),
        pytest.param([None], True, [], id="only nulls (ignored)"),
        pytest.param([None], False, [None], id="only nulls (not ignored)"),
    ],
)
def test_should_return_distinct_values(
    values: list[Any],
    ignore_nulls: bool,
    expected: list[Any],
) -> None:
    column: Column = Column("col1", values)
    assert column.distinct_values(ignore_nulls=ignore_nulls) == expected
