from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "names", "ignore_unknown_names", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            [],
            False,
            Table({}),
            id="empty table, empty list",
        ),
        pytest.param(
            lambda: Table({}),
            "col1",
            True,
            Table({}),
            id="empty table, single column (ignoring unknown names)",
        ),
        pytest.param(
            lambda: Table({}),
            ["col1", "col2"],
            True,
            Table({}),
            id="empty table, multiple columns (ignoring unknown names)",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            [],
            False,
            Table({"col1": [], "col2": []}),
            id="non-empty table, empty list",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            ["col2"],
            False,
            Table({"col1": []}),
            id="non-empty table, single column",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            ["col1", "col2"],
            False,
            Table({}),
            id="non-empty table, multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_remove_columns(
        self,
        table_factory: Callable[[], Table],
        names: str | list[str],
        ignore_unknown_names: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().remove_columns(names, ignore_unknown_names=ignore_unknown_names)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        names: str | list[str],
        ignore_unknown_names: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.remove_columns(names, ignore_unknown_names=ignore_unknown_names)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_for_unknown_columns() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({}).remove_columns(["col1"])
