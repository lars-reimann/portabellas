import polars as pl
import pytest

from portabellas import Column, Table
from portabellas.debugging import QueryAnalyzer
from portabellas.exceptions import LazyComputationError


@pytest.mark.parametrize(
    ("data", "optimized"),
    [
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), True, id="trivial table (optimized)"),
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), False, id="trivial table (unoptimized)"),
        pytest.param(Column("a", [1, 2, 3]), True, id="trivial column (optimized)"),
        pytest.param(Column("a", [1, 2, 3]), False, id="trivial column (unoptimized)"),
        pytest.param(
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}).add_computed_column("c", lambda row: row["a"] * 2),
            True,
            id="table with computed column (optimized)",
        ),
        pytest.param(
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}).add_computed_column("c", lambda row: row["a"] * 2),
            False,
            id="table with computed column (unoptimized)",
        ),
        pytest.param(
            Column("a", [1, 2, 3]).map(lambda cell: cell * 2),
            True,
            id="mapped column (optimized)",
        ),
        pytest.param(
            Column("a", [1, 2, 3]).map(lambda cell: cell * 2),
            False,
            id="mapped column (unoptimized)",
        ),
    ],
)
def test_should_return_non_empty_string(data: Table | Column, optimized: bool) -> None:
    analyzer = QueryAnalyzer(data)
    plan = analyzer.explain(optimized=optimized)
    assert isinstance(plan, str)
    assert len(plan) > 0


def test_should_raise_lazy_computation_error_on_polars_error() -> None:
    broken_frame = pl.LazyFrame().select("a")
    table = Table.from_polars(broken_frame)
    analyzer = QueryAnalyzer(table)
    with pytest.raises(LazyComputationError):
        analyzer.explain()
