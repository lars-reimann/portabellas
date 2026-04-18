import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell._expr_cell import ExprCell


@pytest.mark.parametrize(
    ("cell", "expected"),
    [
        pytest.param(
            Cell.constant(1),
            "dyn int: 1",
            id="constant",
        ),
        pytest.param(
            ExprCell(pl.col("a")),
            'col("a")',
            id="column",
        ),
    ],
)
def test_should_return_a_string_representation(cell: Cell, expected: str) -> None:
    assert str(cell) == expected
