from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "key_selector", "descending", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            lambda row: row["col1"],
            False,
            Table({"col1": [], "col2": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            lambda row: row["col1"],
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="non-empty, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            lambda row: row["col1"],
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="non-empty, descending",
        ),
    ],
)
class TestHappyPath:
    def test_should_return_sorted_table(
        self,
        table_factory: Callable[[], Table],
        key_selector: Callable[[Row], Cell],
        descending: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sort_rows(key_selector, descending=descending)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        key_selector: Callable[[Row], Cell],
        descending: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sort_rows(key_selector, descending=descending)
        assert_tables_are_equal(original, table_factory())
