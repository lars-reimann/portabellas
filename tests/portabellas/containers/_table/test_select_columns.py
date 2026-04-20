from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "names", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            [],
            Table({}),
            id="empty table, empty list",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            [],
            Table({}),
            id="non-empty table, empty list",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            "col2",
            Table({"col2": []}),
            id="non-empty table, single column",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            ["col1", "col2"],
            Table({"col1": [], "col2": []}),
            id="non-empty table, multiple columns",
        ),
        pytest.param(
            lambda: Table({"A": [1], "B": [2], "C": [3]}),
            ["C", "A"],
            Table({"C": [3], "A": [1]}),
            id="swapped order",
        ),
    ],
)
class TestHappyPath:
    def test_should_select_columns(
        self,
        table_factory: Callable[[], Table],
        names: str | list[str],
        expected: Table,
    ) -> None:
        actual = table_factory().select_columns(names)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        names: str | list[str],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.select_columns(names)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_for_unknown_columns() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({}).select_columns(["col1"])
