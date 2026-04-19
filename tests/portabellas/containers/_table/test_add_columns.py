from collections.abc import Callable

import pytest

from portabellas import Column, Table
from portabellas.exceptions import DuplicateColumnError, LengthMismatchError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "columns", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            [],
            Table({}),
            id="empty table, empty list",
        ),
        pytest.param(
            lambda: Table({}),
            Column("col1", [1]),
            Table({"col1": [1]}),
            id="empty table, single column",
        ),
        pytest.param(
            lambda: Table({}),
            [Column("col1", [1]), Column("col2", [2])],
            Table({"col1": [1], "col2": [2]}),
            id="empty table, multiple columns",
        ),
        pytest.param(
            lambda: Table({"col0": [0]}),
            [],
            Table({"col0": [0]}),
            id="non-empty table, empty list",
        ),
        pytest.param(
            lambda: Table({"col0": [0]}),
            Column("col1", [1]),
            Table({"col0": [0], "col1": [1]}),
            id="non-empty table, single column",
        ),
        pytest.param(
            lambda: Table({"col0": [0]}),
            [Column("col1", [1]), Column("col2", [2])],
            Table({"col0": [0], "col1": [1], "col2": [2]}),
            id="non-empty table, multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_add_columns(
        self,
        table_factory: Callable[[], Table],
        columns: Column | list[Column],
        expected: Table,
    ) -> None:
        actual = table_factory().add_columns(columns)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        columns: Column | list[Column],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.add_columns(columns)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    ("table", "columns"),
    [
        pytest.param(
            Table({"col1": [1]}),
            Column("col2", [1, 2]),
            id="single new column",
        ),
        pytest.param(
            Table({"col1": [1]}),
            [Column("col2", [1, 2])],
            id="list of new columns",
        ),
    ],
)
def test_should_raise_if_row_counts_differ(table: Table, columns: Column | list[Column]) -> None:
    with pytest.raises(LengthMismatchError):
        table.add_columns(columns)


@pytest.mark.parametrize(
    ("table", "columns"),
    [
        pytest.param(
            Table({"col1": [1]}),
            Column("col1", [1]),
            id="single new column clashes with existing column",
        ),
        pytest.param(
            Table({"col1": [1]}),
            [Column("col1", [1])],
            id="list of new columns clashes with existing column",
        ),
        pytest.param(
            Table({}),
            [Column("col1", [1]), Column("col1", [2])],
            id="new columns clash with each other",
        ),
    ],
)
def test_should_raise_if_duplicate_column_name(table: Table, columns: Column | list[Column]) -> None:
    with pytest.raises(DuplicateColumnError):
        table.add_columns(columns)
