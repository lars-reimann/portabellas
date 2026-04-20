import datetime

import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], None, id="empty"),
        pytest.param([None, None], None, id="null column"),
        pytest.param([1, 2, None], 1, id="numeric column"),
        pytest.param(
            [datetime.time(1, 2, 3), datetime.time(4, 5, 6), None], datetime.time(1, 2, 3), id="temporal column"
        ),
        pytest.param(["a", "b", None], "a", id="string column"),
        pytest.param([True, False, None], False, id="boolean column"),
    ],
)
def test_should_return_minimum(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.min() == expected
