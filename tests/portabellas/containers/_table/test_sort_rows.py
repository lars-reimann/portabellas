from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "by", "descending", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            "col1",
            False,
            Table({"col1": [], "col2": []}),
            id="by str, no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            "col1",
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="by str, non-empty, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            "col1",
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="by str, non-empty, descending",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            ["col1"],
            False,
            Table({"col1": [], "col2": []}),
            id="by list[str], no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            ["col1"],
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="by list[str], single column, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            ["col1"],
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="by list[str], single column, descending",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 2], "col2": [2, 1, 1]}),
            ["col1", "col2"],
            False,
            Table({"col1": [1, 1, 2], "col2": [1, 2, 1]}),
            id="by list[str], multiple columns, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 2], "col2": [2, 1, 1]}),
            ["col1", "col2"],
            True,
            Table({"col1": [2, 1, 1], "col2": [1, 2, 1]}),
            id="by list[str], multiple columns, descending",
        ),
        pytest.param(
            lambda: Table({"col1": [], "col2": []}),
            lambda row: row["col1"],
            False,
            Table({"col1": [], "col2": []}),
            id="by callable, no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            lambda row: row["col1"],
            False,
            Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            id="by callable, non-empty, ascending",
        ),
        pytest.param(
            lambda: Table({"col1": [2, 3, 1], "col2": [5, 6, 4]}),
            lambda row: row["col1"],
            True,
            Table({"col1": [3, 2, 1], "col2": [6, 5, 4]}),
            id="by callable, non-empty, descending",
        ),
    ],
)
class TestHappyPath:
    def test_should_return_sorted_table(
        self,
        table_factory: Callable[[], Table],
        by: str | list[str] | Callable[[Row], Cell],
        descending: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sort_rows(by, descending=descending)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        by: str | list[str] | Callable[[Row], Cell],
        descending: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sort_rows(by, descending=descending)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    "by",
    [
        pytest.param("unknown", id="by str"),
        pytest.param(["col1", "unknown"], id="by list[str]"),
    ],
)
def test_should_raise_if_column_not_found(by: str | list[str]) -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({"col1": [1, 2, 3]}).sort_rows(by)
