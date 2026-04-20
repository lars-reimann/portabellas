from collections.abc import Callable

import pytest

from portabellas import Table


@pytest.mark.parametrize(
    "table_factory",
    [
        pytest.param(lambda: Table({}), id="empty"),
        pytest.param(lambda: Table({"col1": []}), id="no rows"),
        pytest.param(lambda: Table({"col1": [1, 2]}), id="with data"),
    ],
)
class TestContract:
    def test_should_return_same_hash_for_equal_objects(self, table_factory: Callable[[], Table]) -> None:
        table_1 = table_factory()
        table_2 = table_factory()
        assert hash(table_1) == hash(table_2)


@pytest.mark.parametrize(
    ("table_1", "table_2"),
    [
        pytest.param(
            Table({"col1": [1]}),
            Table({}),
            id="too few columns",
        ),
        pytest.param(
            Table({}),
            Table({"col1": [1]}),
            id="too many columns",
        ),
        pytest.param(
            Table({"col1": [1], "col2": [2]}),
            Table({"col2": [2], "col1": [1]}),
            id="different column order",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col2": [1]}),
            id="different column names",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": ["1"]}),
            id="different types",
        ),
        pytest.param(
            Table({"col1": [1, 2]}),
            Table({"col1": [1]}),
            id="too few rows",
        ),
        pytest.param(
            Table({"col1": [1]}),
            Table({"col1": [1, 2]}),
            id="too many rows",
        ),
    ],
)
def test_should_return_different_hash_for_unequal_objects(table_1: Table, table_2: Table) -> None:
    assert hash(table_1) != hash(table_2)
