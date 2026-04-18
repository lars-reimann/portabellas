import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell._expr_cell import ExprCell


@pytest.mark.parametrize(
    ("cell", "expected"),
    [
        pytest.param(
            Cell.constant(1),
            "ExprCell(dyn int: 1)",
            id="constant",
        ),
        pytest.param(
            ExprCell(pl.col("a")),
            'ExprCell(col("a"))',
            id="column",
        ),
    ],
)
def test_should_return_a_string_representation(cell: Cell, expected: str) -> None:
    assert repr(cell) == expected
