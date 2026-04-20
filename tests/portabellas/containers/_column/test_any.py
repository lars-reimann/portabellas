import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], False, id="empty"),
        pytest.param([1], True, id="always true"),
        pytest.param([2], False, id="always false"),
        pytest.param([None], False, id="always unknown"),
        pytest.param([1, None], True, id="true and unknown"),
        pytest.param([2, None], False, id="false and unknown"),
        pytest.param([1, 2], True, id="true and false"),
        pytest.param([1, 2, None], True, id="true and false and unknown"),
    ],
)
def test_should_handle_boolean_logic(values: list, expected: bool) -> None:
    column = Column("col1", values)
    assert column.any(lambda value: value < 2) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], False, id="empty"),
        pytest.param([1], True, id="always true"),
        pytest.param([2], False, id="always false"),
        pytest.param([None], None, id="always unknown"),
        pytest.param([1, None], True, id="true and unknown"),
        pytest.param([2, None], None, id="false and unknown"),
        pytest.param([1, 2], True, id="true and false"),
        pytest.param([1, 2, None], True, id="true and false and unknown"),
    ],
)
def test_should_handle_kleene_logic(values: list, expected: bool | None) -> None:
    column = Column("col1", values)
    assert column.any(lambda value: value < 2, ignore_unknown=False) == expected
