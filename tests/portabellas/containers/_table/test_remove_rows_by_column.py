from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "name", "predicate", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            "col1",
            lambda _: Cell.constant(False),  # noqa: FBT003
            Table({"col1": [], "col2": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [-1, -2]}),
            "col1",
            lambda cell: cell <= 0,
            Table({"col1": [1, 2], "col2": [-1, -2]}),
            id="no matches",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [-1, -2]}),
            "col1",
            lambda cell: cell <= 1,
            Table({"col1": [2], "col2": [-2]}),
            id="some matches",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [-1, -2]}),
            "col1",
            lambda cell: cell <= 2,
            Table({"col1": [], "col2": []}),
            id="only matches",
        ),
        pytest.param(
            lambda: Table({"col1": [None], "col2": [None]}),
            "col1",
            lambda cell: cell <= 2,
            Table({"col1": [None], "col2": [None]}),
            id="None",
        ),
    ],
)
class TestHappyPath:
    def test_should_remove_rows(
        self,
        table_factory: Callable[[], Table],
        name: str,
        predicate: Callable[[Cell], Cell[bool]],
        expected: Table,
    ) -> None:
        actual = table_factory().remove_rows_by_column(name, predicate)
        assert_tables_are_equal(actual, expected, ignore_types=actual.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        name: str,
        predicate: Callable[[Cell], Cell[bool]],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.remove_rows_by_column(name, predicate)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_column_does_not_exist() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({}).remove_rows_by_column("col1", lambda cell: cell <= 0)
