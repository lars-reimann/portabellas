from typing import Any

import polars as pl
import pytest

from portabellas import Table
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="empty"),
        pytest.param({"col1": []}, id="no rows"),
        pytest.param({"col1": [1, 2], "col2": [3, 4]}, id="non-empty"),
    ],
)
def test_should_create_table_from_data_frame(data: dict[str, list[Any]]) -> None:
    actual = Table.from_polars(pl.DataFrame(data))
    expected = Table(data)
    assert_tables_are_equal(actual, expected)


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="empty"),
        pytest.param({"col1": []}, id="no rows"),
        pytest.param({"col1": [1, 2], "col2": [3, 4]}, id="non-empty"),
    ],
)
def test_should_create_table_from_lazy_frame(data: dict[str, list[Any]]) -> None:
    actual = Table.from_polars(pl.LazyFrame(data))
    expected = Table(data)
    assert_tables_are_equal(actual, expected)
