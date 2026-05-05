from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, DuplicateColumnError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "column_names", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            [],
            Table({}),
            id="empty table",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            ["b", "a"],
            Table({"b": [4, 5, 6], "a": [1, 2, 3]}),
            id="swap two columns",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}),
            ["c", "a", "b"],
            Table({"c": [7, 8, 9], "a": [1, 2, 3], "b": [4, 5, 6]}),
            id="reorder three columns",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            ["a", "b"],
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            id="same order",
        ),
    ],
)
class TestHappyPath:
    def test_should_reorder_columns(
        self,
        table_factory: Callable[[], Table],
        column_names: list[str],
        expected: Table,
    ) -> None:
        actual = table_factory().reorder_columns(column_names)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        column_names: list[str],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.reorder_columns(column_names)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_column_does_not_exist() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({"a": [1], "b": [2]}).reorder_columns(["a", "c"])


def test_should_raise_if_column_is_missing_from_list() -> None:
    with pytest.raises(ValueError, match="exist in the table but were not listed"):
        Table({"a": [1], "b": [2], "c": [3]}).reorder_columns(["a", "b"])


def test_should_raise_if_column_name_is_duplicated() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"a": [1], "b": [2]}).reorder_columns(["a", "a", "b"])
