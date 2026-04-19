import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow


@pytest.mark.parametrize(
    ("table", "name", "expected"),
    [
        pytest.param(Table({"A": [1]}), "A", True, id="existing column"),
        pytest.param(Table({"A": [1]}), "B", False, id="missing column"),
        pytest.param(Table({"A": [1], "B": [2]}), "B", True, id="existing column in multi-column table"),
        pytest.param(Table({"A": [1], "B": [2]}), "C", False, id="missing column in multi-column table"),
    ],
)
def test_should_check_if_column_exists(table: Table, name: str, expected: bool) -> None:
    row = ExprRow(table)
    assert row.has_column(name) == expected
