from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal

# ----------------------------------------------------------------------------------------------------------------------
# by=str
# ----------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("table_factory", "by", "descending", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            "col1",
            False,
            Table({"col1": [], "col2": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            "col1",
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="non-empty, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            "col1",
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="non-empty, descending",
        ),
    ],
)
class TestByStr:
    def test_should_return_sorted_table(
        self,
        table_factory: Callable[[], Table],
        by: str,
        descending: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sort_rows(by, descending=descending)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        by: str,
        descending: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sort_rows(by, descending=descending)
        assert_tables_are_equal(original, table_factory())


def test_by_str_should_raise_if_column_not_found() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({"col1": [1, 2, 3]}).sort_rows("unknown")


# ----------------------------------------------------------------------------------------------------------------------
# by=list[str]
# ----------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("table_factory", "by", "descending", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            ["col1"],
            False,
            Table({"col1": [], "col2": []}),
            id="no rows, single column",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            ["col1"],
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="single column, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            ["col1"],
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="single column, descending",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 2], "col2": [2, 1, 1]}),
            ["col1", "col2"],
            False,
            Table({"col1": [1, 1, 2], "col2": [1, 2, 1]}),
            id="multiple columns, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 2], "col2": [2, 1, 1]}),
            ["col1", "col2"],
            True,
            Table({"col1": [2, 1, 1], "col2": [1, 2, 1]}),
            id="multiple columns, descending",
        ),
    ],
)
class TestByListStr:
    def test_should_return_sorted_table(
        self,
        table_factory: Callable[[], Table],
        by: list[str],
        descending: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sort_rows(by, descending=descending)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        by: list[str],
        descending: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sort_rows(by, descending=descending)
        assert_tables_are_equal(original, table_factory())


def test_by_list_str_should_raise_if_column_not_found() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({"col1": [1, 2, 3]}).sort_rows(["col1", "unknown"])


# ----------------------------------------------------------------------------------------------------------------------
# by=Callable
# ----------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("table_factory", "by", "descending", "expected"),
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
class TestByCallable:
    def test_should_return_sorted_table(
        self,
        table_factory: Callable[[], Table],
        by: Callable[[Row], Cell],
        descending: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sort_rows(by, descending=descending)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        by: Callable[[Row], Cell],
        descending: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sort_rows(by, descending=descending)
        assert_tables_are_equal(original, table_factory())
