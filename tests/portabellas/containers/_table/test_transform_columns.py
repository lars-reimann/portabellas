from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.containers import Cell, Row
from portabellas.exceptions import ColumnNotFoundError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "selector", "mapper", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": []}),
            "col1",
            lambda _: Cell.constant(None),
            Table({"col1": []}),
            id="no rows (constant value)",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            "col1",
            lambda cell: 2 * cell,
            Table({"col1": []}),
            id="no rows (computed value)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            "col1",
            lambda _: Cell.constant(None),
            Table({"col1": [None, None]}),
            id="non-empty (constant value)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2]}),
            "col1",
            lambda cell: 2 * cell,
            Table({"col1": [2, 4]}),
            id="non-empty (computed value)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [3, 4]}),
            ["col1", "col2"],
            lambda _: Cell.constant(None),
            Table({"col1": [None, None], "col2": [None, None]}),
            id="multiple columns (constant value)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [3, 4]}),
            ["col1", "col2"],
            lambda cell: 2 * cell,
            Table({"col1": [2, 4], "col2": [6, 8]}),
            id="multiple columns (computed value)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2], "col2": [3, 4]}),
            "col1",
            lambda cell, row: 2 * cell + row["col2"],
            Table({"col1": [5, 8], "col2": [3, 4]}),
            id="lambda takes row parameter",
        ),
    ],
)
class TestHappyPath:
    def test_should_transform_columns(
        self,
        table_factory: Callable[[], Table],
        selector: str | list[str],
        mapper: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell],
        expected: Table,
    ) -> None:
        actual = table_factory().transform_columns(selector, mapper)
        assert_tables_are_equal(actual, expected, ignore_types=True)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        selector: str | list[str],
        mapper: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell],
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.transform_columns(selector, mapper)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    ("table", "selector"),
    [
        pytest.param(
            Table({"col1": [1, 2]}),
            "col2",
            id="one column name",
        ),
        pytest.param(
            Table({"col1": [1, 2]}),
            ["col1", "col2"],
            id="multiple column names",
        ),
    ],
)
def test_should_raise_if_column_not_found(
    table: Table,
    selector: str | list[str],
) -> None:
    with pytest.raises(ColumnNotFoundError):
        table.transform_columns(selector, lambda cell: cell * 2)
