from portabellas import Table
from portabellas.containers._row import ExprRow


def test_should_return_schema() -> None:
    table = Table({"A": [1], "B": ["x"]})
    row = ExprRow(table)
    assert row.schema == table.schema
