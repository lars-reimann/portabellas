import pytest

from portabellas import Table


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        pytest.param(Table({}), Table({}), id="empty"),
    ],
)
def test_should_summarize_statistics(table: Table, expected: Table) -> None:
    from tests.helpers import assert_tables_are_equal

    actual = table.summarize_statistics()
    assert_tables_are_equal(actual, expected)
