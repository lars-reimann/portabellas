from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import SQLQueryError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "query", "expected"),
    [
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            "SELECT * FROM self",
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            id="select all",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            "SELECT a FROM self",
            Table({"a": [1, 2, 3]}),
            id="select one column",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            "SELECT * FROM self WHERE a > 1",
            Table({"a": [2, 3], "b": [5, 6]}),
            id="filter with WHERE",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3]}),
            "SELECT a + 1 AS a FROM self",
            Table({"a": [2, 3, 4]}),
            id="computed column",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3]}),
            "SELECT a AS a FROM self ORDER BY a DESC",
            Table({"a": [3, 2, 1]}),
            id="order by",
        ),
        pytest.param(
            lambda: Table({"a": [1, 1, 2]}),
            "SELECT DISTINCT a AS a FROM self ORDER BY a",
            Table({"a": [1, 2]}),
            id="select distinct",
        ),
    ],
)
class TestSQLMethod:
    def test_should_execute_sql_query(
        self,
        table_factory: Callable[[], Table],
        query: str,
        expected: Table,
    ) -> None:
        actual = table_factory().sql(query)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        query: str,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sql(query)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    ("query", "error_type"),
    [
        pytest.param(
            "SELECT FROM",
            SQLQueryError,
            id="syntax error",
        ),
        pytest.param(
            "SELECT * FROM nonexistent",
            SQLQueryError,
            id="missing table",
        ),
        pytest.param(
            "SELECT nonexistent FROM self",
            SQLQueryError,
            id="missing column",
        ),
    ],
)
def test_should_raise_on_query_planning_error(query: str, error_type: type) -> None:
    table = Table({"a": [1, 2, 3]})
    with pytest.raises(error_type):
        table.sql(query)


def test_should_raise_on_empty_query() -> None:
    table = Table({"a": [1, 2, 3]})
    with pytest.raises(ValueError, match="empty"):
        table.sql("")
