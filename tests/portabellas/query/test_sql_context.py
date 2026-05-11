import pytest

from portabellas import Table
from portabellas.exceptions import SQLQueryError
from portabellas.query import SQLContext
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("tables", "query", "expected"),
    [
        pytest.param(
            {"t1": Table({"a": [1, 2, 3]})},
            "SELECT * FROM t1",
            Table({"a": [1, 2, 3]}),
            id="single table select all",
        ),
        pytest.param(
            {"t1": Table({"a": [1, 2, 3]})},
            "SELECT a FROM t1 WHERE a > 1",
            Table({"a": [2, 3]}),
            id="single table filter",
        ),
        pytest.param(
            {
                "orders": Table({"order_id": [1, 2, 3], "customer_id": [10, 20, 30], "amount": [100, 200, 300]}),
                "customers": Table({"customer_id": [10, 20, 40], "name": ["Alice", "Bob", "Charlie"]}),
            },
            "SELECT o.order_id, c.name "
            "FROM orders AS o JOIN customers AS c ON o.customer_id = c.customer_id "
            "ORDER BY o.order_id",
            Table({"order_id": [1, 2], "name": ["Alice", "Bob"]}),
            id="join two tables",
        ),
    ],
)
class TestSQLContextExecute:
    def test_should_execute_sql_query(
        self,
        tables: dict[str, Table],
        query: str,
        expected: Table,
    ) -> None:
        ctx = SQLContext(tables=tables)
        actual = ctx.execute(query)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_input_tables(
        self,
        tables: dict[str, Table],
        query: str,
        expected: Table,  # noqa: ARG002
    ) -> None:
        originals = {name: Table(table.to_dict()) for name, table in tables.items()}
        ctx = SQLContext(tables=tables)
        ctx.execute(query)
        for name, original in originals.items():
            assert_tables_are_equal(tables[name], original)


@pytest.mark.parametrize(
    ("query", "error_type"),
    [
        pytest.param(
            "",
            SQLQueryError,
            id="empty query",
        ),
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
            "SELECT nonexistent FROM t1",
            SQLQueryError,
            id="missing column",
        ),
    ],
)
def test_should_raise_on_query_planning_error(query: str, error_type: type) -> None:
    ctx = SQLContext(tables={"t1": Table({"a": [1, 2, 3]})})
    with pytest.raises(error_type):
        ctx.execute(query)
