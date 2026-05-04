import polars as pl
import pytest

from portabellas import Column
from portabellas.typing import DataTypes


def test_should_store_the_name() -> None:
    frame = pl.LazyFrame({"col1": []})
    assert Column._from_polars_lazy_frame("col1", frame).name == "col1"


@pytest.mark.parametrize(
    ("frame", "expected"),
    [
        pytest.param(
            pl.LazyFrame({"col1": []}),
            [],
            id="empty",
        ),
        pytest.param(
            pl.LazyFrame({"col1": [True]}),
            [True],
            id="non-empty",
        ),
    ],
)
def test_should_store_the_data(frame: pl.LazyFrame, expected: list) -> None:
    assert list(Column._from_polars_lazy_frame("col1", frame)) == expected


def test_should_have_correct_type() -> None:
    frame = pl.LazyFrame({"col1": [1]})
    assert Column._from_polars_lazy_frame("col1", frame).type == DataTypes.Int64()
