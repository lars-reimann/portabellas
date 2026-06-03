import polars as pl
import pytest

from portabellas import Column, DataTypes, Table
from portabellas.debugging import QueryAnalyzer
from portabellas.exceptions import LazyComputationError
from portabellas.typing import Schema


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), id="trivial table"),
        pytest.param(Column("a", [1, 2, 3]), id="trivial column"),
        pytest.param(
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}).add_computed_column("c", lambda row: row["a"] * 2),
            id="table with computed column",
        ),
        pytest.param(Column("a", [1, 2, 3]).map(lambda cell: cell * 2), id="mapped column"),
    ],
)
class TestProfilingResult:
    def test_should_have_correct_schema(self, data: Table | Column) -> None:
        analyzer = QueryAnalyzer(data)
        timing = analyzer.profile()
        assert timing.schema == Schema(
            {
                "node": DataTypes.String(),
                "start": DataTypes.UInt64(),
                "end": DataTypes.UInt64(),
            }
        )

    def test_should_have_positive_row_count(self, data: Table | Column) -> None:
        analyzer = QueryAnalyzer(data)
        timing = analyzer.profile()
        assert timing.row_count > 0

    def test_should_have_optimization_as_first_row(self, data: Table | Column) -> None:
        analyzer = QueryAnalyzer(data)
        timing = analyzer.profile()
        assert timing["node"].get_value(0) == "optimization"
        assert timing["start"].get_value(0) == 0


def test_should_raise_lazy_computation_error_on_polars_error() -> None:
    broken_frame = pl.LazyFrame().select("a")
    table = Table.from_polars(broken_frame)
    analyzer = QueryAnalyzer(table)
    with pytest.raises(LazyComputationError):
        analyzer.profile()
