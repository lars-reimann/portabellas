from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.exceptions import DuplicateColumnError
from portabellas.typing import DataTypes
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "name", "mapper", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            "col1",
            lambda _: Cell.constant(None),
            Table({"col1": []}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            "col2",
            lambda _: Cell.constant(None),
            Table({"col1": [], "col2": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            "col2",
            lambda _: Cell.constant(None),
            Table({"col1": [1, 2, 3], "col2": [None, None, None]}),
            id="non-empty, constant value",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            "col2",
            lambda row: 2 * row["col1"],
            Table({"col1": [1, 2, 3], "col2": [2, 4, 6]}),
            id="non-empty, computed value",
        ),
    ],
)
class TestHappyPath:
    def test_should_add_computed_column(
        self,
        table_factory: Callable[[], Table],
        name: str,
        mapper: Callable,
        expected: Table,
    ) -> None:
        actual = table_factory().add_computed_column(name, mapper)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        name: str,
        mapper: Callable,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.add_computed_column(name, mapper)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_duplicate_column_name() -> None:
    with pytest.raises(DuplicateColumnError):
        Table({"col1": []}).add_computed_column("col1", lambda row: row["col1"])


def test_should_propagate_known_type_from_mapper() -> None:
    table = Table({"a": [1, 2, 3]})
    result = table.add_computed_column("b", lambda row: row["a"] < 2)
    assert result.schema.get_column_type("b") == DataTypes.Boolean()


def test_should_fall_back_to_polars_when_mapper_returns_unknown_type() -> None:
    table = Table({"a": [1, 2, 3]})

    def mapper(row: Row) -> Cell:
        cell = row["a"]
        return ExprCell(cell._polars_expression < 2, type=DataTypes.Unknown())

    result = table.add_computed_column("b", mapper)
    assert result.schema.get_column_type("b") == DataTypes.Boolean()
