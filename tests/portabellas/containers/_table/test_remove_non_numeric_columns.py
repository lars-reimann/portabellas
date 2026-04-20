from collections.abc import Callable

import pytest

from portabellas import Table
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            Table({}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [4, 5]}),
            Table({"col1": [1, 2], "col2": [4, 5]}),
            id="only numeric columns",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": ["a", "b"]}),
            Table({"col1": [1, 2]}),
            id="some non-numeric columns",
        ),
        pytest.param(
            lambda: Table({"col1": ["a", "b"], "col2": ["a", "b"]}),
            Table({}),
            id="only non-numeric columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_remove_non_numeric_columns(
        self,
        table_factory: Callable[[], Table],
        expected: Table,
    ) -> None:
        actual = table_factory().remove_non_numeric_columns()
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.remove_non_numeric_columns()
        assert_tables_are_equal(original, table_factory())
