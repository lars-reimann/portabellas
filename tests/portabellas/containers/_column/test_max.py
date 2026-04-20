import datetime

import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], None, id="empty"),
        pytest.param([None, None], None, id="null column"),
        pytest.param([1, 2, None], 2, id="numeric column"),
        pytest.param(
            [datetime.time(1, 2, 3), datetime.time(4, 5, 6), None], datetime.time(4, 5, 6), id="temporal column"
        ),
        pytest.param(["a", "b", None], "b", id="string column"),
        pytest.param([True, False, None], True, id="boolean column"),
    ],
)
def test_should_return_maximum(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.max() == expected
