from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl
from polars.exceptions import PanicException, PolarsError

from portabellas.containers._table import Table
from portabellas.exceptions import LazyComputationError

if TYPE_CHECKING:
    from portabellas.containers._column import Column


class QueryAnalyzer:
    """
    Analysis tool for inspecting query plans and profiling execution of a `Table` or `Column`.

    Parameters
    ----------
    data:
        The `Table` or `Column` to analyze.

    Examples
    --------
    >>> from portabellas import Table
    >>> from portabellas.debugging import QueryAnalyzer
    >>> table = Table({"a": [1, 2, 3]})
    >>> analyzer = QueryAnalyzer(table)
    >>> plan = analyzer.explain()
    """

    def __init__(self, data: Table | Column) -> None:
        self._lazy_frame = data._lazy_frame

    def explain(self, *, optimized: bool = True) -> str:
        """
        Return the query plan.

        Parameters
        ----------
        optimized:
            If `True` (default), return the optimized query plan. If `False`, return the unoptimized plan.

        Returns
        -------
        str
            The query plan as a string.

        Raises
        ------
        LazyComputationError
            If an error occurs during the computation.

        Examples
        --------
        >>> from portabellas import Table
        >>> from portabellas.debugging import QueryAnalyzer
        >>> table = Table({"a": [1, 2, 3]})
        >>> analyzer = QueryAnalyzer(table)
        >>> analyzer.explain()
        'DF ["a"]; PROJECT */1 COLUMNS'
        """
        try:
            return self._lazy_frame.explain(optimized=optimized)
        except PolarsError as e:
            raise LazyComputationError(str(e)) from None

    def profile(self) -> Table:
        """
        Execute the query and return profiling information.

        Returns
        -------
        Table
            A profiling table containing timing information for each step of the query.

        Raises
        ------
        LazyComputationError
            If an error occurs during the computation.

        Examples
        --------
        >>> from portabellas import Table
        >>> from portabellas.debugging import QueryAnalyzer
        >>> table = Table({"a": [1, 2, 3]})
        >>> analyzer = QueryAnalyzer(table)
        >>> analyzer.profile()
        +--------------+-------+-----+
        | node         | start | end |
        | ---          |   --- | --- |
        | str          |   u64 | u64 |
        +============================+
        | optimization |     0 |   0 |
        +--------------+-------+-----+
        """
        try:
            try:
                _, profile_df = self._lazy_frame.profile(engine="streaming")
            except PanicException:
                _, profile_df = self._lazy_frame.profile()
        except PolarsError as e:
            if "no data to time" in str(e):
                profile_df = pl.DataFrame(
                    {
                        "node": pl.Series(["optimization"], dtype=pl.Utf8),
                        "start": pl.Series([0], dtype=pl.UInt64),
                        "end": pl.Series([0], dtype=pl.UInt64),
                    },
                )
            else:
                raise LazyComputationError(str(e)) from None

        return Table._from_polars_data_frame(profile_df)
