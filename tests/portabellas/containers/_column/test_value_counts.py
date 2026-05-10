from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from portabellas import Column, Table
from portabellas.typing import DataTypes
from tests.helpers import assert_tables_are_equal

if TYPE_CHECKING:
    from typing import Any


def _expected_table(col_values: list[Any], count_values: list[int]) -> Table:
    return Table.from_columns(
        [
            Column("col", col_values),
            Column("count", count_values, type=DataTypes.UInt32()),
        ],
    )


@pytest.mark.parametrize(
    ("values", "ignore_nulls", "expected"),
    [
        pytest.param(
            [],
            True,
            _expected_table([], []),
            id="empty",
        ),
        pytest.param(
            [1, 2, 3],
            True,
            _expected_table([1, 2, 3], [1, 1, 1]),
            id="no duplicates",
        ),
        pytest.param(
            [1, 2, 1],
            True,
            _expected_table([1, 2], [2, 1]),
            id="some duplicates",
        ),
        pytest.param(
            [1, 2, 3, None],
            True,
            _expected_table([1, 2, 3], [1, 1, 1]),
            id="with nulls (ignored)",
        ),
        pytest.param(
            [1, 2, 3, None],
            False,
            _expected_table([1, 2, 3, None], [1, 1, 1, 1]),
            id="with nulls (not ignored)",
        ),
        pytest.param(
            [None],
            True,
            _expected_table([], []),
            id="only nulls (ignored)",
        ),
        pytest.param(
            [None],
            False,
            _expected_table([None], [1]),
            id="only nulls (not ignored)",
        ),
        pytest.param(
            ["a", "b", "a"],
            True,
            _expected_table(["a", "b"], [2, 1]),
            id="string column",
        ),
    ],
)
def test_should_return_value_counts(
    values: list[Any],
    ignore_nulls: bool,
    expected: Table,
) -> None:
    column = Column("col", values)
    actual = column.value_counts(ignore_nulls=ignore_nulls)
    assert_tables_are_equal(actual, expected)
