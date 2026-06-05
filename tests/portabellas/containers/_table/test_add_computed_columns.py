from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.exceptions import DuplicateColumnError
from portabellas.typing import DataTypes
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "mappers", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [1]}),
            {},
            Table({"col1": [1]}),
            id="empty mappers dict",
        ),
        pytest.param(
            lambda: Table({}),
            {"col1": lambda _: Cell.constant(None)},
            Table({"col1": []}),
            id="empty table, single mapper",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            {"col2": lambda _: Cell.constant(None)},
            Table({"col1": [], "col2": []}),
            id="no rows, single mapper",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            {"col2": lambda row: 2 * row["col1"]},
            Table({"col1": [1, 2, 3], "col2": [2, 4, 6]}),
            id="single mapper, computed value",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            {
                "c": lambda row: row["a"] + row["b"],
                "d": lambda row: row["a"] * row["b"],
            },
            Table({"a": [1, 2, 3], "b": [4, 5, 6], "c": [5, 7, 9], "d": [4, 10, 18]}),
            id="multiple mappers, computed values",
        ),
        pytest.param(
            lambda: Table({"a": [1, 2, 3]}),
            {
                "b": lambda _: Cell.constant(None),
                "c": lambda row: row["a"] * 10,
            },
            Table({"a": [1, 2, 3], "b": [None, None, None], "c": [10, 20, 30]}),
            id="mix of constant and computed mappers",
        ),
    ],
)
class TestHappyPath:
    def test_should_add_computed_columns(
        self,
        table_factory: Callable[[], Table],
        mappers: dict[str, Callable],
        expected: Table,
    ) -> None:
        actual = table_factory().add_computed_columns(mappers)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        mappers: dict[str, Callable],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.add_computed_columns(mappers)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_duplicate_column_name() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"col1": []}).add_computed_columns({"col1": lambda row: row["col1"]})


def test_should_raise_if_new_name_clashes_with_existing() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"a": [1], "b": [2]}).add_computed_columns(
            {"a": lambda row: row["b"], "c": lambda row: row["a"]},
        )


def test_should_propagate_known_types_from_mappers() -> None:
    table = Table({"a": [1, 2, 3]})
    result = table.add_computed_columns(
        {"b": lambda row: row["a"] < 2, "c": lambda row: row["a"] + 10},
    )
    assert result.schema.get_column_type("b") == DataTypes.Boolean()
    assert result.schema.get_column_type("c") == DataTypes.Int64()


def test_should_fall_back_to_polars_when_mapper_returns_unknown_type() -> None:
    table = Table({"a": [1, 2, 3]})

    def mapper(row: Row) -> Cell:
        cell = row["a"]
        return ExprCell(cell._polars_expression < 2, type=DataTypes.Unknown())

    result = table.add_computed_columns({"b": mapper})
    assert result.schema.get_column_type("b") == DataTypes.Boolean()
