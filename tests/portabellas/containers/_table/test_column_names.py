import pytest

from portabellas import Table


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), [], id="empty"),
        pytest.param(Table({"col1": []}), ["col1"], id="no rows"),
        pytest.param(Table({"col1": [1], "col2": [1]}), ["col1", "col2"], id="with data"),
    ],
)
def test_should_return_column_names(table: Table, expected: list[str]) -> None:
    assert table.column_names == expected
