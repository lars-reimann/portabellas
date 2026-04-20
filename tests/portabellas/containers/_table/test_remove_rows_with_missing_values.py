from collections.abc import Callable

import pytest

from portabellas import Table
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "column_names", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            None,
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            None,
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            None,
            Table({"col1": [1, 2]}),
            id="no missing values",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, None], "col2": [1, None, 3], "col3": [None, 2, 3]}),
            None,
            Table({"col1": [], "col2": [], "col3": []}),
            id="missing values (all columns selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, None], "col2": [1, None, 3], "col3": [None, 2, 3]}),
            ["col1", "col2"],
            Table({"col1": [1], "col2": [1], "col3": [None]}),
            id="missing values (several columns selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, None], "col2": [1, None, 3], "col3": [None, 2, 3]}),
            "col1",
            Table({"col1": [1, 2], "col2": [1, None], "col3": [None, 2]}),
            id="missing values (one column selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, None], "col2": [1, None, 3], "col3": [None, 2, 3]}),
            [],
            Table({"col1": [1, 2, None], "col2": [1, None, 3], "col3": [None, 2, 3]}),
            id="missing values (no columns selected)",
        ),
    ],
)
class TestHappyPath:
    def test_should_remove_rows_with_missing_values(
        self,
        table_factory: Callable[[], Table],
        column_names: str | list[str] | None,
        expected: Table,
    ) -> None:
        actual = table_factory().remove_rows_with_missing_values(selector=column_names)
        assert_tables_are_equal(actual, expected, ignore_types=True)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        column_names: str | list[str] | None,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.remove_rows_with_missing_values(selector=column_names)
        assert_tables_are_equal(original, table_factory())
