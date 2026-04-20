from typing import Any

import pytest

from portabellas import Column, Table


@pytest.mark.parametrize(
    ("table_1", "table_2", "expected"),
    [
        pytest.param(
            Table({}),
            Table({}),
            True,
            id="equal (empty)",
        ),
        pytest.param(
            Table({"col1": []}),
            Table({"col1": []}),
            True,
            id="equal (no rows)",
        ),
        pytest.param(
            Table({"col1": [1], "col2": [2]}),
            Table({"col1": [1], "col2": [2]}),
            True,
            id="equal (with data)",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({}),
            False,
            id="not equal (too few columns)",
        ),
        pytest.param(
            Table({}),
            Table({"col1": [1]}),
            False,
            id="not equal (too many columns)",
        ),
        pytest.param(
            Table({"col1": [1], "col2": [2]}),
            Table({"col2": [2], "col1": [1]}),
            False,
            id="not equal (different column order)",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col2": [1]}),
            False,
            id="not equal (different column names)",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": ["1"]}),
            False,
            id="not equal (different types)",
        ),
        pytest.param(
            Table({"col1": [1, 2]}),
            Table({"col1": [1]}),
            False,
            id="not equal (too few rows)",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": [1, 2]}),
            False,
            id="not equal (too many rows)",
        ),
        pytest.param(
            Table({"col1": [1, 2]}),
            Table({"col1": [2, 1]}),
            False,
            id="not equal (different row order)",
        ),
        pytest.param(
            Table({"col1": [1, 2]}),
            Table({"col1": [1, 3]}),
            False,
            id="not equal (different values)",
        ),
    ],
)
def test_should_return_whether_objects_are_equal(table_1: Table, table_2: Table, expected: bool) -> None:
    assert (table_1.__eq__(table_2)) == expected


@pytest.mark.parametrize(
    "table",
    [
        pytest.param(Table({}), id="empty"),
        pytest.param(Table({"col1": []}), id="no rows"),
        pytest.param(Table({"col1": [1]}), id="non-empty"),
    ],
)
def test_should_return_true_if_objects_are_identical(table: Table) -> None:
    assert (table.__eq__(table)) is True


@pytest.mark.parametrize(
    ("table", "other"),
    [
        pytest.param(Table({}), None, id="Table vs. None"),
        pytest.param(Table({}), Column("col1", []), id="Table vs. Column"),
    ],
)
def test_should_return_not_implemented_if_other_has_different_type(table: Table, other: Any) -> None:
    assert (table.__eq__(other)) is NotImplemented
