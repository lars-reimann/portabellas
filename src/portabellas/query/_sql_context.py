from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl
import polars.exceptions as pl_exceptions

from portabellas.exceptions import SQLQueryError

if TYPE_CHECKING:
    from portabellas import Table


class SQLContext:
    """
    Execute SQL queries against one or more tables.

    Parameters
    ----------
    tables:
        A mapping from table names to `Table` objects. The table names are used as table identifiers in SQL queries.

    Examples
    --------
    >>> from portabellas import Table
    >>> from portabellas.query import SQLContext
    >>> orders = Table({"order_id": [1, 2], "amount": [100, 200]})
    >>> ctx = SQLContext(tables={"orders": orders})
    >>> ctx.execute("SELECT * FROM orders WHERE amount > 100")
    +----------+--------+
    | order_id | amount |
    | ---      | ---    |
    | i64      | i64    |
    +===================+
    |        2 |    200 |
    +----------+--------+
    """

    def __init__(self, tables: dict[str, Table]) -> None:
        from portabellas.containers._table import Table  # circular import  # noqa: PLC0415

        if not isinstance(tables, dict):
            msg = f"Expected a dict, got {type(tables).__name__}"
            raise TypeError(msg) from None

        self._polars_context = pl.SQLContext()

        for name, table in tables.items():
            if not isinstance(table, Table):
                msg = f"Expected a Table, got {type(table).__name__}"
                raise TypeError(msg) from None

            self._polars_context.register(name, table._lazy_frame)

    def execute(self, query: str) -> Table:
        """
        Execute an SQL query against the registered tables and return the result as a new table.

        Parameters
        ----------
        query:
            The SQL query to execute.

        Returns
        -------
        result:
            The table with the query results.

        Raises
        ------
        SQLQueryError
            If the query fails during query planning (e.g. syntax errors, missing table or column references).
        ValueError
            If the query is an empty string.

        Examples
        --------
        >>> from portabellas import Table
        >>> from portabellas.query import SQLContext
        >>> table = Table({"a": [1, 2, 3]})
        >>> ctx = SQLContext(tables={"t": table})
        >>> ctx.execute("SELECT * FROM t WHERE a > 1")
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   2 |
        |   3 |
        +-----+
        """
        from portabellas.containers._table import Table  # circular import  # noqa: PLC0415

        if not query:
            msg = "The query must not be empty."
            raise ValueError(msg) from None

        try:
            lazy_frame = self._polars_context.execute(query)
        except pl_exceptions.PolarsError as e:
            raise SQLQueryError(str(e)) from None

        return Table._from_polars_lazy_frame(lazy_frame)
