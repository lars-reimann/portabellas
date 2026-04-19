import pytest

from portabellas import Table


@pytest.mark.parametrize(
    ("table", "name", "expected"),
    [
        pytest.param(Table({"col1": []}), "col1", True, id="existing column"),
        pytest.param(Table({"col1": []}), "col2", False, id="non-existing column"),
        pytest.param(Table({}), "col1", False, id="empty table"),
    ],
)
def test_should_check_if_column_exists(table: Table, name: str, expected: bool) -> None:
    assert table.has_column(name) == expected
