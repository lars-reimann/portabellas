import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell._expr_cell import ExprCell


@pytest.mark.parametrize(
    ("cell", "expected"),
    [
        (
            Cell.constant(1),
            "ExprCell(dyn int: 1)",
        ),
        (
            ExprCell(pl.col("a")),
            'ExprCell(col("a"))',
        ),
    ],
    ids=[
        "constant",
        "column",
    ],
)
def test_should_return_a_string_representation(cell: Cell, expected: str) -> None:
    assert repr(cell) == expected
