from collections.abc import Callable, Generator
from unittest.mock import patch

import polars as pl
import pytest

from portabellas import Column, Table
from portabellas.containers import Cell
from portabellas.containers._cell import ExprCell
from portabellas.containers._row import ExprRow
from portabellas.typing import DataType, DataTypes

_UNKNOWN = DataTypes.Unknown()


@pytest.fixture
def captured_expr_cell_types() -> Generator[list[DataType]]:
    captured: list[DataType] = []
    original_init = ExprCell.__init__

    def _capturing_init(self: ExprCell, expression: pl.Expr, *, type: DataType = _UNKNOWN) -> None:  # noqa: A002
        captured.append(type)
        original_init(self, expression, type=type)

    with patch.object(ExprCell, "__init__", _capturing_init):
        yield captured


@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param(
            lambda: ExprRow(Table({"A": [1]})).get_cell("A"),
            id="expr_row_get_cell",
        ),
        pytest.param(
            lambda: Column("a", [1, 2, 3]).map(lambda _: Cell.constant(None)),
            id="column_map",
        ),
        pytest.param(
            lambda: Column("a", [1, 2, 3]).all(lambda _: Cell.constant(1)),
            id="column_all",
        ),
        pytest.param(
            lambda: Column("a", [1, 2, 3]).any(lambda _: Cell.constant(1)),
            id="column_any",
        ),
        pytest.param(
            lambda: Column("a", [1, 2, 3]).count_if(lambda _: Cell.constant(1)),
            id="column_count_if",
        ),
        pytest.param(
            lambda: Column("a", [1, 2, 3]).none(lambda _: Cell.constant(1)),
            id="column_none",
        ),
    ],
)
def test_should_pass_known_type_to_expr_cell(
    scenario: Callable[[], None],
    captured_expr_cell_types: list[DataType],
) -> None:
    scenario()
    assert any(not isinstance(t, DataTypes.Unknown) for t in captured_expr_cell_types)
