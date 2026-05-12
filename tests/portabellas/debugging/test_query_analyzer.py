from __future__ import annotations

import pytest

from portabellas import Column, Table
from portabellas.debugging import QueryAnalyzer


class TestQueryAnalyzerInit:
    @pytest.mark.parametrize(
        ("data", "id"),
        [
            pytest.param(Table({"a": [1, 2, 3]}), "table", id="table"),
            pytest.param(Column("a", [1, 2, 3]), "column", id="column"),
        ],
    )
    def test_should_accept_table_and_column(self, data: Table | Column, id: str) -> None:  # noqa: A002, ARG002
        analyzer = QueryAnalyzer(data)
        assert analyzer is not None

    def test_should_reject_invalid_type(self) -> None:
        with pytest.raises(TypeError, match="QueryAnalyzer requires a Table or Column"):
            QueryAnalyzer("not a table")  # type: ignore[arg-type]


class TestExplain:
    def test_should_return_string_for_table(self) -> None:
        table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        analyzer = QueryAnalyzer(table)
        plan = analyzer.explain()
        assert isinstance(plan, str)
        assert len(plan) > 0

    def test_should_return_string_for_column(self) -> None:
        column = Column("a", [1, 2, 3])
        analyzer = QueryAnalyzer(column)
        plan = analyzer.explain()
        assert isinstance(plan, str)
        assert len(plan) > 0

    def test_should_accept_optimized_false(self) -> None:
        table = Table({"a": [1, 2, 3]})
        analyzer = QueryAnalyzer(table)
        plan = analyzer.explain(optimized=False)
        assert isinstance(plan, str)
        assert len(plan) > 0


class TestProfile:
    def test_should_return_profiling_table_for_table(self) -> None:
        table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        analyzer = QueryAnalyzer(table)
        timing = analyzer.profile()
        assert isinstance(timing, Table)
        assert timing.row_count > 0

    def test_should_return_profiling_table_for_column(self) -> None:
        column = Column("a", [1, 2, 3])
        analyzer = QueryAnalyzer(column)
        timing = analyzer.profile()
        assert isinstance(timing, Table)
        assert timing.row_count > 0

    def test_should_contain_profiling_columns(self) -> None:
        table = Table({"a": [1, 2, 3]})
        analyzer = QueryAnalyzer(table)
        timing = analyzer.profile()
        assert "node" in timing.column_names
        assert "start" in timing.column_names
        assert "end" in timing.column_names
