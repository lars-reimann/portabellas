from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import SchemaError
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
            lambda: Table({"col1": []}),
            lambda: Table({"col1": []}),
            Table({"col1": []}),
            id="no rows, no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1]}),
            lambda: Table({"col1": [2]}),
            Table({"col1": [1, 2]}),
            id="with data, with data",
        ),
        pytest.param(
            lambda: Table({"col1": [1]}),
            lambda: [
                Table({"col1": [2]}),
                Table({"col1": [3]}),
            ],
            Table({"col1": [1, 2, 3]}),
            id="multiple tables",
        ),
    ],
)
class TestHappyPath:
    def test_should_add_rows(
        self,
        table_factory: Callable[[], Table],
        others_factory: Callable[[], Table | list[Table]],
        expected: Table,
    ) -> None:
        actual = table_factory().add_tables_as_rows(others_factory())
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        others_factory: Callable[[], Table | list[Table]],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.add_tables_as_rows(others_factory())
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
        table_factory().add_tables_as_rows(original)
        for table, snapshot in zip(original_tables, snapshots, strict=True):
            assert_tables_are_equal(table, snapshot)


@pytest.mark.parametrize(
    ("table", "others"),
    [
        pytest.param(
            Table({}),
            Table({"col1": [1]}),
            id="empty table, non-empty table",
        ),
        pytest.param(
            Table({"col1": [], "col2": []}),
            Table({"col1": []}),
            id="too few columns",
        ),
        pytest.param(
            Table({"col1": []}),
            Table({"col1": [], "col2": []}),
            id="too many columns",
        ),
        pytest.param(
            Table({"col1": []}),
            Table({"col2": []}),
            id="different column names",
        ),
        pytest.param(
            Table({"col1": [], "col2": []}),
            Table({"col2": [], "col1": []}),
            id="swapped columns",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": ["a"]}),
            id="different column types",
        ),
        pytest.param(
            Table({"col1": []}),
            [
                Table({"col1": []}),
                Table({"col2": []}),
            ],
            id="multiple tables",
        ),
    ],
)
def test_should_raise_if_schemas_differ(table: Table, others: Table | list[Table]) -> None:
    with pytest.raises(SchemaError):
        table.add_tables_as_rows(others)
