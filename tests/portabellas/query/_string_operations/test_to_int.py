import pytest

from portabellas.containers import Cell
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "base", "expected"),
    [
        pytest.param("", 10, None, id="empty"),
        pytest.param("abc", 10, None, id="invalid"),
        pytest.param("10", 10, 10, id="base 10"),
        pytest.param("10", 2, 2, id="base 2"),
        pytest.param(None, 10, None, id="None as value"),
        pytest.param("0", None, None, id="None as base"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldConvertStringToInteger:
    def test_plain_arguments(self, value: str | None, base: int | None, expected: float | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.to_int(base=base),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, base: int | None, expected: float | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.to_int(
                base=Cell.constant(base),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.String()).str.to_int()
    assert_cell_has_type(result, DataTypes.Int64())
