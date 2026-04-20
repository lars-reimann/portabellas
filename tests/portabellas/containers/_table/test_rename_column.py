from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, DuplicateColumnError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "old_name", "new_name", "expected"),
    [
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            "A",
            "C",
            Table({"C": [1], "B": [2]}),
            id="name changed",
        ),
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            "A",
            "A",
            Table({"A": [1], "B": [2]}),
            id="name unchanged",
        ),
    ],
)
class TestHappyPath:
    def test_should_rename_column(
        self,
        table_factory: Callable[[], Table],
        old_name: str,
        new_name: str,
        expected: Table,
    ) -> None:
        actual = table_factory().rename_column(old_name, new_name)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        old_name: str,
        new_name: str,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.rename_column(old_name, new_name)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_old_column_does_not_exist() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({}).rename_column("A", "B")


def test_should_raise_if_new_column_exists_already() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"A": [1], "B": [2]}).rename_column("A", "B")
