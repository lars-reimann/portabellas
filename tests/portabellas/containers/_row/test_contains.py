import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow


@pytest.mark.parametrize(
    ("table", "key", "expected"),
    [
        pytest.param(Table({"A": [1]}), "A", True, id="existing column"),
        pytest.param(Table({"A": [1]}), "B", False, id="missing column"),
        pytest.param(Table({"A": [1], "B": [2]}), "B", True, id="existing column in multi-column table"),
        pytest.param(Table({"A": [1]}), 1, False, id="non-string key"),
    ],
)
def test_should_check_if_column_exists(table: Table, key: object, expected: bool) -> None:
    row = ExprRow(table)
    assert (key in row) == expected
