from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, DuplicateColumnError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "mapper", "expected"),
    [
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            {"A": "C", "B": "D"},
            Table({"C": [1], "D": [2]}),
            id="dict: multiple columns renamed",
        ),
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            {"A": "C"},
            Table({"C": [1], "B": [2]}),
            id="dict: single column renamed",
        ),
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            {"A": "B", "B": "A"},
            Table({"B": [1], "A": [2]}),
            id="dict: swap two column names",
        ),
        pytest.param(
            lambda: Table({"A": [1], "B": [2]}),
            {"A": "A"},
            Table({"A": [1], "B": [2]}),
            id="dict: name unchanged",
        ),
    ],
)
class TestDictHappyPath:
    def test_should_rename_columns(
        self,
        table_factory: Callable[[], Table],
        mapper: dict[str, str],
        expected: Table,
    ) -> None:
        actual = table_factory().rename_columns(mapper)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        mapper: dict[str, str],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.rename_columns(mapper)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    ("table_factory", "mapper", "expected"),
    [
        pytest.param(
            lambda: Table({"a": [1], "b": [2]}),
            lambda name: name.upper(),
            Table({"A": [1], "B": [2]}),
            id="callable: uppercase all names",
        ),
        pytest.param(
            lambda: Table({"a": [1], "b": [2]}),
            lambda name: "prefix_" + name,
            Table({"prefix_a": [1], "prefix_b": [2]}),
            id="callable: add prefix",
        ),
        pytest.param(
            lambda: Table({"a": [1], "b": [2]}),
            lambda name: name,
            Table({"a": [1], "b": [2]}),
            id="callable: identity",
        ),
    ],
)
class TestCallableHappyPath:
    def test_should_rename_columns(
        self,
        table_factory: Callable[[], Table],
        mapper: Callable[[str], str],
        expected: Table,
    ) -> None:
        actual = table_factory().rename_columns(mapper)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        mapper: Callable[[str], str],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.rename_columns(mapper)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_old_column_does_not_exist() -> None:
    with pytest.raises(ColumnNotFoundError):
        Table({"A": [1]}).rename_columns({"X": "Y"})


def test_should_raise_if_new_column_collides_with_existing() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"A": [1], "B": [2]}).rename_columns({"A": "B"})


def test_should_raise_if_new_names_are_duplicates_in_dict() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"A": [1], "B": [2]}).rename_columns({"A": "C", "B": "C"})


def test_should_raise_if_callable_produces_duplicate_names() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"A": [1], "B": [2]}).rename_columns(lambda _name: "same")
