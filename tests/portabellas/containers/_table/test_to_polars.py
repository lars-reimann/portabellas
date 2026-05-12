from typing import Any

import polars as pl
import pytest

from portabellas import Table


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="empty"),
        pytest.param({"col1": []}, id="no rows"),
        pytest.param({"col1": [1, 2], "col2": [3, 4]}, id="non-empty"),
    ],
)
def test_should_return_lazy_frame_with_preserved_data(data: dict[str, list[Any]]) -> None:
    table = Table(data)
    result = table.to_polars()
    assert isinstance(result, pl.LazyFrame)
    assert result.collect().equals(pl.DataFrame(data))
