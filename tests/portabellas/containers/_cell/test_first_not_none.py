from typing import Any

import pytest

from portabellas import Column
from portabellas.containers import Cell

_none_cell = Cell.constant(None)


@pytest.mark.parametrize(
    ("cells", "expected"),
    [
        pytest.param([], None, id="empty"),
        pytest.param([_none_cell], None, id="all None"),
        pytest.param([_none_cell, Cell.constant(1)], 1, id="one not None"),
        pytest.param([Cell.constant(1), _none_cell, Cell.constant(2)], 1, id="multiple not None"),
    ],
)
def test_should_return_first_non_none_value(cells: list[Cell], expected: Any) -> None:
    column = Column("a", [None])
    transformed = column.transform(lambda _: Cell.first_not_none(cells))
    assert transformed.get_value(0) == expected
