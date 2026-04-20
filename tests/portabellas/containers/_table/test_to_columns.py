import pytest

from portabellas import Column, Table


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), [], id="empty"),
        pytest.param(
            Table({"col1": [], "col2": []}),
            [Column("col1", []), Column("col2", [])],
            id="no rows",
        ),
        pytest.param(
            Table({"col1": [1, 2], "col2": [3, 4]}),
            [Column("col1", [1, 2]), Column("col2", [3, 4])],
            id="with data",
        ),
    ],
)
def test_should_return_list_of_columns(table: Table, expected: list[Column]) -> None:
    assert table.to_columns() == expected
