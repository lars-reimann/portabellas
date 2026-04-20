from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import DuplicateColumnError, LengthMismatchError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "others_factory", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            lambda: Table({}),
            Table({}),
            id="empty, empty",
        ),
        pytest.param(
            lambda: Table({}),
            lambda: Table({"col1": [1]}),
            Table({"col1": [1]}),
            id="empty, non-empty",
        ),
        pytest.param(
            lambda: Table({"col1": [1]}),
            lambda: Table({}),
            Table({"col1": [1]}),
            id="non-empty, empty",
        ),
        pytest.param(
            lambda: Table({"col1": [1]}),
            lambda: Table({"col2": [2]}),
            Table({"col1": [1], "col2": [2]}),
            id="non-empty, non-empty",
        ),
        pytest.param(
            lambda: Table({"col1": [1]}),
            lambda: [
                Table({"col2": [2]}),
                Table({"col3": [3]}),
            ],
            Table({"col1": [1], "col2": [2], "col3": [3]}),
            id="multiple tables",
        ),
    ],
)
class TestHappyPath:
    def test_should_add_columns(
        self,
        table_factory: Callable[[], Table],
        others_factory: Callable[[], Table | list[Table]],
        expected: Table,
    ) -> None:
        actual = table_factory().add_tables_as_columns(others_factory())
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        others_factory: Callable[[], Table | list[Table]],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.add_tables_as_columns(others_factory())
        assert_tables_are_equal(original, table_factory())

    def test_should_not_mutate_others(
        self,
        table_factory: Callable[[], Table],
        others_factory: Callable[[], Table | list[Table]],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = others_factory()
        original_tables = [original] if isinstance(original, Table) else original
        snapshots = [Table.from_columns(t.to_columns()) for t in original_tables]
        table_factory().add_tables_as_columns(original)
        for table, snapshot in zip(original_tables, snapshots, strict=True):
            assert_tables_are_equal(table, snapshot)


@pytest.mark.parametrize(
    ("table", "others"),
    [
        pytest.param(
            Table({"col1": [1]}),
            Table({"col2": [1, 2]}),
            id="one table",
        ),
        pytest.param(
            Table({"col1": [1]}),
            [
                Table({"col2": [1]}),
                Table({"col3": [1, 2]}),
            ],
            id="multiple tables",
        ),
    ],
)
def test_should_raise_if_row_counts_differ(table: Table, others: Table | list[Table]) -> None:
    with pytest.raises(LengthMismatchError):
        table.add_tables_as_columns(others)


@pytest.mark.parametrize(
    ("table", "others"),
    [
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": [1]}),
            id="one table",
        ),
        pytest.param(
            Table({"col1": [1]}),
            [
                Table({"col2": [1]}),
                Table({"col1": [1]}),
            ],
            id="multiple tables, clash with receiver",
        ),
        pytest.param(
            Table({"col1": [1]}),
            [
                Table({"col2": [1]}),
                Table({"col2": [1]}),
            ],
            id="multiple tables, clash with other table",
        ),
    ],
)
def test_should_raise_if_duplicate_column_name(table: Table, others: Table | list[Table]) -> None:
    with pytest.raises(DuplicateColumnError):
        table.add_tables_as_columns(others)
