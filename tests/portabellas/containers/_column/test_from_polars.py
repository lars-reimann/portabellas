import polars as pl
import pytest

from portabellas import Column
from portabellas.typing import DataTypes


@pytest.mark.parametrize(
    ("series", "expected_name", "expected_data"),
    [
        pytest.param(pl.Series("col1", []), "col1", [], id="empty"),
        pytest.param(pl.Series("col1", [1, 2]), "col1", [1, 2], id="non-empty"),
        pytest.param(pl.Series("col1", ["a", "b"]), "col1", ["a", "b"], id="strings"),
    ],
)
def test_should_create_column_from_series(
    series: pl.Series,
    expected_name: str,
    expected_data: list,
) -> None:
    result = Column.from_polars(series)
    assert result.name == expected_name
    assert list(result) == expected_data


def test_should_have_correct_type() -> None:
    series = pl.Series("col1", [1])
    assert Column.from_polars(series).type == DataTypes.Int64()
