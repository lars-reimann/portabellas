import polars as pl

from portabellas import Table


def test_should_return_lazy_frame() -> None:
    table = Table({"col1": [1, 2], "col2": [3, 4]})
    result = table.to_polars()
    assert isinstance(result, pl.LazyFrame)


def test_should_preserve_data() -> None:
    table = Table({"col1": [1, 2], "col2": [3, 4]})
    result = table.to_polars().collect()
    expected = pl.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    assert result.equals(expected)


def test_should_return_same_lazy_frame_as_internal() -> None:
    table = Table({"col1": [1, 2]})
    assert table.to_polars() is table._lazy_frame
