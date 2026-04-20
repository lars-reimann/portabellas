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
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            Table({"col1": [3, 1, 2]}),
            id="one column",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            Table({"col1": [3, 1, 2], "col2": [6, 4, 5]}),
            id="multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_shuffle_rows(
        self,
        table_factory: Callable[[], Table],
        expected: Table,
    ) -> None:
        actual = table_factory().shuffle_rows()
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.shuffle_rows()
        assert_tables_are_equal(original, table_factory())
