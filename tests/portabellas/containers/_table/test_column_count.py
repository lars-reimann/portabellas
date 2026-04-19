import pytest

from portabellas import Table


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), 0, id="empty"),
        pytest.param(Table({"col1": []}), 1, id="no rows"),
        pytest.param(Table({"col1": [1], "col2": [1]}), 2, id="with data"),
    ],
)
def test_should_return_number_of_columns(table: Table, expected: int) -> None:
    assert table.column_count == expected
