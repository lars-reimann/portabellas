from typing import Any

import pytest

from portabellas import Column
from portabellas.containers import Cell


@pytest.mark.parametrize(
    ("column_1", "column_2", "expected"),
    [
        pytest.param(
            Column("col1", []),
            Column("col1", []),
            True,
            id="equal (no rows)",
        ),
        pytest.param(
            Column("col1", [1]),
            Column("col1", [1]),
            True,
            id="equal (with data)",
        ),
        pytest.param(
            Column("col1", [1]),
            Column("col2", [1]),
            False,
            id="not equal (different names)",
        ),
        pytest.param(
            Column("col1", [1]),
            Column("col1", ["1"]),
            False,
            id="not equal (different types)",
        ),
        pytest.param(
            Column("col1", [1, 2]),
            Column("col1", [1]),
            False,
            id="not equal (too few rows)",
        ),
        pytest.param(
            Column("col1", [1]),
            Column("col1", [1, 2]),
            False,
            id="not equal (too many rows)",
        ),
        pytest.param(
            Column("col1", [1, 2]),
            Column("col1", [2, 1]),
            False,
            id="not equal (different row order)",
        ),
        pytest.param(
            Column("col1", [1, 2]),
            Column("col1", [1, 3]),
            False,
            id="not equal (different values)",
        ),
    ],
)
def test_should_return_whether_objects_are_equal(column_1: Column, column_2: Column, expected: bool) -> None:
    assert (column_1.__eq__(column_2)) == expected


@pytest.mark.parametrize(
    "column",
    [
        pytest.param(Column("col1", []), id="no rows"),
        pytest.param(Column("col1", [1]), id="non-empty"),
    ],
)
def test_should_return_true_if_objects_are_identical(column: Column) -> None:
    assert (column.__eq__(column)) is True


@pytest.mark.parametrize(
    ("column", "other"),
    [
        pytest.param(Column("col1", []), None, id="Column vs. None"),
        pytest.param(Column("col1", []), Cell.constant(1), id="Column vs. Cell"),
    ],
)
def test_should_return_not_implemented_if_other_has_different_type(column: Column, other: Any) -> None:
    assert (column.__eq__(other)) is NotImplemented
