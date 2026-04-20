import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1], 1, id="always true"),
        pytest.param([2], 0, id="always false"),
        pytest.param([None], 0, id="always unknown"),
        pytest.param([1, None], 1, id="true and unknown"),
        pytest.param([2, None], 0, id="false and unknown"),
        pytest.param([1, 2], 1, id="true and false"),
        pytest.param([1, 2, None], 1, id="true and false and unknown"),
    ],
)
def test_should_handle_boolean_logic(values: list, expected: int) -> None:
    column = Column("col1", values)
    assert column.count_if(lambda value: value < 2) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1], 1, id="always true"),
        pytest.param([2], 0, id="always false"),
        pytest.param([None], None, id="always unknown"),
        pytest.param([1, None], None, id="true and unknown"),
        pytest.param([2, None], None, id="false and unknown"),
        pytest.param([1, 2], 1, id="true and false"),
        pytest.param([1, 2, None], None, id="true and false and unknown"),
    ],
)
def test_should_handle_kleene_logic(values: list, expected: int | None) -> None:
    column = Column("col1", values)
    assert column.count_if(lambda value: value < 2, ignore_unknown=False) == expected
