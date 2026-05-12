import polars as pl

from portabellas import Column


def test_should_return_series() -> None:
    column = Column("col1", [1, 2, 3])
    result = column.to_polars()
    assert isinstance(result, pl.Series)


def test_should_preserve_name() -> None:
    column = Column("col1", [1, 2, 3])
    result = column.to_polars()
    assert result.name == "col1"


def test_should_preserve_data() -> None:
    column = Column("col1", [1, 2, 3])
    result = column.to_polars()
    expected = pl.Series("col1", [1, 2, 3])
    assert result.equals(expected)
