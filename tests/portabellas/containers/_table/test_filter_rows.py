from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "predicate", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            lambda _: Cell.constant(False),  # noqa: FBT003
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            lambda _: Cell.constant(False),  # noqa: FBT003
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            lambda row: row["col1"] <= 0,
            Table({"col1": []}),
            id="no matches",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            lambda row: row["col1"] <= 1,
            Table({"col1": [1]}),
            id="some matches",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            lambda row: row["col1"] <= 2,
            Table({"col1": [1, 2]}),
            id="only matches",
        ),
        pytest.param(
            lambda: Table({"col1": [None]}),
            lambda row: row["col1"] <= 2,
            Table({"col1": []}),
            id="None",
        ),
    ],
)
class TestHappyPath:
    def test_should_filter_rows(
        self,
        table_factory: Callable[[], Table],
        predicate: Callable[[Row], Cell[bool]],
        expected: Table,
    ) -> None:
        actual = table_factory().filter_rows(predicate)
        assert_tables_are_equal(actual, expected, ignore_types=actual.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        predicate: Callable[[Row], Cell[bool]],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.filter_rows(predicate)
        assert_tables_are_equal(original, table_factory())
