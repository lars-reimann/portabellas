import pytest

from portabellas import Table
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), Table({}), id="empty"),
        pytest.param(Table({"col1": []}), Table({"col1": []}), id="no rows"),
        pytest.param(
            Table({"col1": [0, 1, 2, 1, 3], "col2": [0, -1, -2, -1, -3]}),
            Table({"col1": [0, 1, 2, 3], "col2": [0, -1, -2, -3]}),
            id="duplicate rows",
        ),
    ],
)
def test_should_remove_duplicate_rows(table: Table, expected: Table) -> None:
    actual = table.remove_duplicate_rows()
    assert_tables_are_equal(actual, expected)
