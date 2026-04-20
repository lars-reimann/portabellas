import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "decimal_places", "expected"),
    [
        pytest.param(0.0, 1, 0, id="0.0"),
        pytest.param(0.1, 0, 0, id="0.1 (0 decimal places)"),
        pytest.param(1.0, 0, 1, id="1.0 (0 decimal places)"),
        pytest.param(1.1, 0, 1, id="1.1 (0 decimal places)"),
        pytest.param(0.14, 1, 0.1, id="0.14 (1 decimal places)"),
        pytest.param(0.104, 2, 0.1, id="0.104 (2 decimal places)"),
        pytest.param(0.15, 1, 0.2, id="0.15 (1 decimal places)"),
        pytest.param(0.105, 2, 0.11, id="0.105 (2 decimal places)"),
        pytest.param(9.99, 1, 10, id="9.99 (1 decimal places)"),
        pytest.param(9.99, 2, 9.99, id="9.99 (2 decimal places)"),
        pytest.param(None, 1, None, id="None"),
    ],
)
def test_should_round_to_decimal_places(
    value: float | None,
    decimal_places: int,
    expected: float | None,
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.round_to_decimal_places(decimal_places),
        expected,
        type_if_none=DataType.Float64(),
    )


def test_should_raise_if_decimal_places_is_out_of_bounds() -> None:
    column = Column("a", [1])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.math.round_to_decimal_places(-1))
