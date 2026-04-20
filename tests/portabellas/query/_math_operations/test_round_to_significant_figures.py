import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "significant_figures", "expected"),
    [
        pytest.param(0, 1, 0, id="0"),
        pytest.param(0.0, 1, 0, id="0.0"),
        pytest.param(0.05, 1, 0.05, id="0.05 (1 sig fig)"),
        pytest.param(0.05, 2, 0.05, id="0.05 (2 sig fig)"),
        pytest.param(0.054, 1, 0.05, id="0.054 (1 sig fig)"),
        pytest.param(0.054, 2, 0.054, id="0.054 (2 sig fig)"),
        pytest.param(0.055, 1, 0.06, id="0.055 (1 sig fig)"),
        pytest.param(0.055, 2, 0.055, id="0.055 (2 sig fig)"),
        pytest.param(0.5, 1, 0.5, id="0.5 (1 sig fig)"),
        pytest.param(0.5, 2, 0.5, id="0.5 (2 sig fig)"),
        pytest.param(0.54, 1, 0.5, id="0.54 (1 sig fig)"),
        pytest.param(0.54, 2, 0.54, id="0.54 (2 sig fig)"),
        pytest.param(0.55, 1, 0.6, id="0.55 (1 sig fig)"),
        pytest.param(0.55, 2, 0.55, id="0.55 (2 sig fig)"),
        pytest.param(5, 1, 5, id="5 (1 sig fig)"),
        pytest.param(5, 2, 5, id="5 (2 sig fig)"),
        pytest.param(5.4, 1, 5, id="5.4 (1 sig fig)"),
        pytest.param(5.4, 2, 5.4, id="5.4 (2 sig fig)"),
        pytest.param(5.5, 1, 6, id="5.5 (1 sig fig)"),
        pytest.param(5.5, 2, 5.5, id="5.5 (2 sig fig)"),
        pytest.param(50, 1, 50, id="50 (1 sig fig)"),
        pytest.param(50, 2, 50, id="50 (2 sig fig)"),
        pytest.param(54, 1, 50, id="54 (1 sig fig)"),
        pytest.param(54, 2, 54, id="54 (2 sig fig)"),
        pytest.param(55, 1, 60, id="55 (1 sig fig)"),
        pytest.param(55, 2, 55, id="55 (2 sig fig)"),
        pytest.param(9.99, 1, 10, id="9.99 (1 sig fig)"),
        pytest.param(9.99, 2, 10, id="9.99 (2 sig fig)"),
        pytest.param(None, 1, None, id="None"),
    ],
)
def test_should_round_to_significant_figures(
    value: float | None,
    significant_figures: int,
    expected: float | None,
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.round_to_significant_figures(significant_figures),
        expected,
        type_if_none=DataType.Float64(),
    )


@pytest.mark.parametrize(
    "significant_figures",
    [
        pytest.param(-1, id="negative"),
        pytest.param(0, id="zero"),
    ],
)
def test_should_raise_if_significant_figures_is_out_of_bounds(significant_figures: int) -> None:
    column = Column("a", [1])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.math.round_to_significant_figures(significant_figures))
