import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], True, id="empty"),
        pytest.param([1], False, id="always true"),
        pytest.param([2], True, id="always false"),
        pytest.param([None], True, id="always unknown"),
        pytest.param([1, None], False, id="true and unknown"),
        pytest.param([2, None], True, id="false and unknown"),
        pytest.param([1, 2], False, id="true and false"),
        pytest.param([1, 2, None], False, id="true and false and unknown"),
    ],
)
def test_should_handle_boolean_logic(values: list, expected: bool) -> None:
    column = Column("col1", values)
    assert column.none(lambda value: value < 2) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], True, id="empty"),
        pytest.param([1], False, id="always true"),
        pytest.param([2], True, id="always false"),
        pytest.param([None], None, id="always unknown"),
        pytest.param([1, None], False, id="true and unknown"),
        pytest.param([2, None], None, id="false and unknown"),
        pytest.param([1, 2], False, id="true and false"),
        pytest.param([1, 2, None], False, id="true and false and unknown"),
    ],
)
def test_should_handle_kleene_logic(values: list, expected: bool | None) -> None:
    column = Column("col1", values)
    assert column.none(lambda value: value < 2, ignore_unknown=False) == expected
