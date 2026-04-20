from typing import Any

import pytest

from portabellas import Table


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), {}, id="empty"),
        pytest.param(Table({"col1": [], "col2": []}), {"col1": [], "col2": []}, id="no rows"),
        pytest.param(Table({"col1": [1, 2], "col2": [3, 4]}), {"col1": [1, 2], "col2": [3, 4]}, id="with data"),
    ],
)
def test_should_return_dictionary(table: Table, expected: dict[str, list[Any]]) -> None:
    assert table.to_dict() == expected
