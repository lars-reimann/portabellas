import pytest

from portabellas import Table


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
    table = Table({"a": values})
    actual = table.count_rows_if(lambda row: row["a"] < 2)
    assert actual == expected


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
    table = Table({"a": values})
    actual = table.count_rows_if(lambda row: row["a"] < 2, ignore_unknown=False)
    assert actual == expected
