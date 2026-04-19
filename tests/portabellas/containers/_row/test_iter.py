import pytest

from portabellas import Table
from portabellas.containers._row import ExprRow


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({"A": [1]}), ["A"], id="one column"),
        pytest.param(Table({"A": [1], "B": [2]}), ["A", "B"], id="two columns"),
        pytest.param(Table({"A": [1], "B": [2], "C": [3]}), ["A", "B", "C"], id="three columns"),
    ],
)
def test_should_iterate_over_column_names(table: Table, expected: list[str]) -> None:
    row = ExprRow(table)
    assert list(row) == expected
