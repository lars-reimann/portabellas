import polars as pl
import pytest

from portabellas import Column, Table
from portabellas.debugging import QueryAnalyzer
from portabellas.exceptions import LazyComputationError


def test_should_return_profiling_table_for_table() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    analyzer = QueryAnalyzer(table)
    timing = analyzer.profile()
    assert isinstance(timing, Table)
    assert timing.row_count > 0


def test_should_return_profiling_table_for_column() -> None:
    column = Column("a", [1, 2, 3])
    analyzer = QueryAnalyzer(column)
    timing = analyzer.profile()
    assert isinstance(timing, Table)
    assert timing.row_count > 0


def test_should_contain_profiling_columns() -> None:
    table = Table({"a": [1, 2, 3]})
    analyzer = QueryAnalyzer(table)
    timing = analyzer.profile()
    assert "node" in timing.column_names
    assert "start" in timing.column_names
    assert "end" in timing.column_names


def test_should_return_dummy_profile_for_trivial_query() -> None:
    table = Table({"a": [1, 2, 3]})
    analyzer = QueryAnalyzer(table)
    timing = analyzer.profile()
    assert timing.row_count == 1
    assert timing["node"].to_list() == ["optimization"]
    assert timing["start"].to_list() == [0]
    assert timing["end"].to_list() == [0]


def test_should_raise_lazy_computation_error_on_polars_error() -> None:
    broken_frame = pl.LazyFrame({"a": [1, 2, 3]}).with_columns(
        invalid=pl.lit("x").cast(pl.Int64),
    )
    table = Table._from_polars_lazy_frame(broken_frame)
    analyzer = QueryAnalyzer(table)
    with pytest.raises(LazyComputationError):
        analyzer.profile()
