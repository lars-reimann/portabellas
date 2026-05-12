import polars as pl
import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("series", "expected"),
    [
        pytest.param(pl.Series("col1", []), Column("col1", []), id="empty"),
        pytest.param(pl.Series("col1", [1, 2]), Column("col1", [1, 2]), id="ints"),
        pytest.param(pl.Series("col1", ["a", "b"]), Column("col1", ["a", "b"]), id="strings"),
    ],
)
def test_should_create_column_from_series(series: pl.Series, expected: Column) -> None:
    actual = Column.from_polars(series)
    assert actual == expected
