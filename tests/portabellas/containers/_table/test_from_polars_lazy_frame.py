from typing import Any

import polars as pl
import pytest

from portabellas import Table
from portabellas.typing import DataTypes, Schema
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="empty"),
        pytest.param({"col1": []}, id="no rows"),
        pytest.param({"col1": [1, 2], "col2": [3, 4]}, id="non-empty"),
    ],
)
def test_should_create_table(data: dict[str, list[Any]]) -> None:
    actual = Table._from_polars_lazy_frame(pl.LazyFrame(data))
    expected = Table(data)
    assert_tables_are_equal(actual, expected)


def test_should_seed_schema_cache_from_schema_parameter() -> None:
    data = pl.LazyFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    schema = Schema({"a": DataTypes.Int64(), "b": DataTypes.Int64()})
    result = Table._from_polars_lazy_frame(data, schema=schema)
    assert result.schema == schema


def test_should_raise_on_schema_mismatch_in_pytest() -> None:
    data = pl.LazyFrame({"a": [1, 2, 3]})
    wrong_schema = Schema({"a": DataTypes.String()})
    with pytest.raises(AssertionError, match="schema"):
        Table._from_polars_lazy_frame(data, schema=wrong_schema)
