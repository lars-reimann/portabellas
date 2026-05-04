import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table", "null_ratio_threshold", "expected"),
    [
        pytest.param(
            Table({}),
            0,
            Table({}),
            id="empty",
        ),
        pytest.param(
            Table({"col1": []}),
            0,
            Table({}),
            id="no rows",
        ),
        pytest.param(
            Table({"col1": [1, 2], "col2": [3, 4]}),
            0,
            Table({"col1": [1, 2], "col2": [3, 4]}),
            id="no nulls",
        ),
        pytest.param(
            Table({"col1": [1, 2, 3], "col2": [1, 2, None], "col3": [1, None, None]}),
            0,
            Table({"col1": [1, 2, 3]}),
            id="some nulls (threshold=0)",
        ),
        pytest.param(
            Table({"col1": [1, 2, 3], "col2": [1, 2, None], "col3": [1, None, None]}),
            0.5,
            Table({"col1": [1, 2, 3], "col2": [1, 2, None]}),
            id="some nulls (threshold=0.5)",
        ),
        pytest.param(
            Table({"col1": [1, 2, 3], "col2": [1, 2, None], "col3": [1, None, None]}),
            1,
            Table({"col1": [1, 2, 3], "col2": [1, 2, None], "col3": [1, None, None]}),
            id="some nulls (threshold=1)",
        ),
    ],
)
def test_should_remove_columns_with_nulls(
    table: Table,
    null_ratio_threshold: int,
    expected: Table,
) -> None:
    actual = table.remove_columns_with_nulls(
        null_ratio_threshold=null_ratio_threshold,
    )
    assert_tables_are_equal(actual, expected)


@pytest.mark.parametrize(
    "null_ratio_threshold",
    [
        pytest.param(-1, id="too low"),
        pytest.param(2, id="too high"),
    ],
)
def test_should_raise_if_null_ratio_threshold_out_of_bounds(null_ratio_threshold: float) -> None:
    with pytest.raises(OutOfBoundsError):
        Table({}).remove_columns_with_nulls(null_ratio_threshold=null_ratio_threshold)
