from collections.abc import Callable
from typing import Literal

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, DuplicateColumnError, LengthMismatchError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("left_table_factory", "right_table_factory", "left_names", "right_names", "mode", "expected"),
    [
        pytest.param(
            lambda: Table({"a": [], "b": []}),
            lambda: Table({"c": [], "d": []}),
            "a",
            "c",
            "inner",
            Table({"a": [], "b": [], "d": []}),
            id="inner join (empty)",
        ),
        pytest.param(
            lambda: Table({"a": [None], "b": [None]}),
            lambda: Table({"c": [None], "d": [None]}),
            "a",
            "c",
            "inner",
            Table({"a": [], "b": [], "d": []}),
            id="inner join (missing values only)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            "a",
            "c",
            "inner",
            Table({"a": [1], "b": [True], "d": [True]}),
            id="inner join (with data)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            ["a", "b"],
            ["c", "d"],
            "inner",
            Table({"a": [1], "b": [True]}),
            id="inner join (two columns to join on)",
        ),
        pytest.param(
            lambda: Table({"a": [], "b": []}),
            lambda: Table({"c": [], "d": []}),
            "a",
            "c",
            "left",
            Table({"a": [], "b": [], "d": []}),
            id="left join (empty)",
        ),
        pytest.param(
            lambda: Table({"a": [None], "b": [None]}),
            lambda: Table({"c": [None], "d": [None]}),
            "a",
            "c",
            "left",
            Table({"a": [None], "b": [None], "d": [None]}),
            id="left join (missing values only)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            "a",
            "c",
            "left",
            Table({"a": [1, 2], "b": [True, False], "d": [True, None]}),
            id="left join (with data)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            ["a", "b"],
            ["c", "d"],
            "left",
            Table({"a": [1, 2], "b": [True, False]}),
            id="left join (two columns to join on)",
        ),
        pytest.param(
            lambda: Table({"a": [], "b": []}),
            lambda: Table({"c": [], "d": []}),
            "a",
            "c",
            "right",
            Table({"b": [], "c": [], "d": []}),
            id="right join (empty)",
        ),
        pytest.param(
            lambda: Table({"a": [None], "b": [None]}),
            lambda: Table({"c": [None], "d": [None]}),
            "a",
            "c",
            "right",
            Table({"b": [None], "c": [None], "d": [None]}),
            id="right join (missing values only)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            "a",
            "c",
            "right",
            Table({"b": [True, None], "c": [1, 3], "d": [True, True]}),
            id="right join (with data)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            ["a", "b"],
            ["c", "d"],
            "right",
            Table({"c": [1, 3], "d": [True, True]}),
            id="right join (two columns to join on)",
        ),
        pytest.param(
            lambda: Table({"a": [], "b": []}),
            lambda: Table({"c": [], "d": []}),
            "a",
            "c",
            "full",
            Table({"a": [], "b": [], "d": []}),
            id="full join (empty)",
        ),
        pytest.param(
            lambda: Table({"a": [None], "b": [None]}),
            lambda: Table({"c": [None], "d": [None]}),
            "a",
            "c",
            "full",
            Table({"a": [None, None], "b": [None, None], "d": [None, None]}),
            id="full join (missing values only)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            "a",
            "c",
            "full",
            Table({"a": [1, 2, 3], "b": [True, False, None], "d": [True, None, True]}),
            id="full join (with data)",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2], "b": [True, False]}),
            lambda: Table({"c": [1, 3], "d": [True, True]}),
            ["a", "b"],
            ["c", "d"],
            "full",
            Table({"a": [1, 2, 3], "b": [True, False, True]}),
            id="full join (two columns to join on)",
        ),
    ],
)
class TestHappyPath:
    def test_should_join_two_tables(
        self,
        left_table_factory: Callable[[], Table],
        right_table_factory: Callable[[], Table],
        left_names: str | list[str],
        right_names: str | list[str],
        mode: Literal["inner", "left", "right", "full"],
        expected: Table,
    ) -> None:
        actual = left_table_factory().join(right_table_factory(), left_names, right_names, mode=mode)
        assert_tables_are_equal(actual, expected, ignore_row_order=True)

    def test_should_not_mutate_receiver(
        self,
        left_table_factory: Callable[[], Table],
        right_table_factory: Callable[[], Table],
        left_names: str | list[str],
        right_names: str | list[str],
        mode: Literal["inner", "left", "right", "full"],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = left_table_factory()
        original.join(right_table_factory(), left_names, right_names, mode=mode)
        assert_tables_are_equal(original, left_table_factory())

    def test_should_not_mutate_right_table(
        self,
        left_table_factory: Callable[[], Table],
        right_table_factory: Callable[[], Table],
        left_names: str | list[str],
        right_names: str | list[str],
        mode: Literal["inner", "left", "right", "full"],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = right_table_factory()
        left_table_factory().join(original, left_names, right_names, mode=mode)
        assert_tables_are_equal(original, right_table_factory())


@pytest.mark.parametrize(
    ("left_table", "right_table", "left_names", "right_names"),
    [
        pytest.param(
            Table({"a": [], "b": []}),
            Table({"c": [], "d": []}),
            "unknown",
            "c",
            id="wrong left name",
        ),
        pytest.param(
            Table({"a": [], "b": []}),
            Table({"c": [], "d": []}),
            "a",
            "unknown",
            id="wrong right name",
        ),
    ],
)
def test_should_raise_if_columns_do_not_exist(
    left_table: Table,
    right_table: Table,
    left_names: str | list[str],
    right_names: str | list[str],
) -> None:
    with pytest.raises(ColumnNotFoundError):
        left_table.join(right_table, left_names=left_names, right_names=right_names)


@pytest.mark.parametrize(
    ("left_table", "right_table", "left_names", "right_names"),
    [
        pytest.param(
            Table({"a": [], "b": []}),
            Table({"c": [], "d": []}),
            ["a", "a"],
            ["c", "d"],
            id="duplicate left name",
        ),
        pytest.param(
            Table({"a": [], "b": []}),
            Table({"c": [], "d": []}),
            ["a", "b"],
            ["c", "c"],
            id="duplicate right name",
        ),
    ],
)
def test_should_raise_if_columns_are_not_unique(
    left_table: Table,
    right_table: Table,
    left_names: list[str],
    right_names: list[str],
) -> None:
    with pytest.raises(DuplicateColumnError):
        left_table.join(right_table, left_names=left_names, right_names=right_names)


def test_should_raise_if_number_of_columns_to_join_on_differs() -> None:
    left_table = Table({"a": [], "b": []})
    right_table = Table({"c": [], "d": []})
    with pytest.raises(LengthMismatchError, match=r"The number of columns to join on must be the same in both tables."):
        left_table.join(right_table, ["a"], ["c", "d"])


def test_should_raise_if_columns_to_join_on_are_empty() -> None:
    left_table = Table({"a": []})
    right_table = Table({"b": []})
    with pytest.raises(ValueError, match=r"The columns to join on must not be empty."):
        left_table.join(right_table, [], [])
