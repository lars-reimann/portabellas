import polars as pl
import pytest

from portabellas import Column, Table
from portabellas.debugging import QueryAnalyzer
from portabellas.exceptions import LazyComputationError


def test_should_return_string_for_table() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    analyzer = QueryAnalyzer(table)
    plan = analyzer.explain()
    assert isinstance(plan, str)
    assert len(plan) > 0


def test_should_return_string_for_column() -> None:
    column = Column("a", [1, 2, 3])
    analyzer = QueryAnalyzer(column)
    plan = analyzer.explain()
    assert isinstance(plan, str)
    assert len(plan) > 0


def test_should_accept_optimized_false() -> None:
    table = Table({"a": [1, 2, 3]})
    analyzer = QueryAnalyzer(table)
    plan = analyzer.explain(optimized=False)
    assert isinstance(plan, str)
    assert len(plan) > 0


def test_should_raise_lazy_computation_error_on_polars_error() -> None:
    broken_frame = pl.LazyFrame({"a": [1, 2, 3]}).with_columns(
        invalid=pl.lit("x").cast(pl.Int64),
    )
    table = Table._from_polars_lazy_frame(broken_frame)
    analyzer = QueryAnalyzer(table)
    with pytest.raises(LazyComputationError):
        analyzer.explain()
