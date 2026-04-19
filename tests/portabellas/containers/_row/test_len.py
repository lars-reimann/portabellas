import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({"A": [1]}), 1, id="one column"),
        pytest.param(Table({"A": [1], "B": [2]}), 2, id="two columns"),
        pytest.param(Table({"A": [1], "B": [2], "C": [3]}), 3, id="three columns"),
    ],
)
def test_should_return_column_count(table: Table, expected: int) -> None:
    row = ExprRow(table)
    assert len(row) == expected
