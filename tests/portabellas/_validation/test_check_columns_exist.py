import pytest

from portabellas import Table
from portabellas._validation import check_columns_exist
from portabellas.exceptions import ColumnNotFoundError


@pytest.mark.parametrize(
    ("table", "selector"),
    [
        pytest.param(Table({"a": []}), "a", id="existing single column"),
        pytest.param(Table({"a": [], "b": []}), "a", id="existing column in multi-column table"),
        pytest.param(Table({"a": [], "b": []}), ["a", "b"], id="existing multiple columns"),
    ],
)
def test_should_not_raise_if_columns_exist(table: Table, selector: str | list[str]) -> None:
    check_columns_exist(table, selector)


@pytest.mark.parametrize(
    ("table", "selector"),
    [
        pytest.param(Table({}), "a", id="empty table, single missing column"),
        pytest.param(Table({"a": []}), "b", id="non-empty table, single missing column"),
        pytest.param(Table({"a": []}), ["a", "b"], id="one existing, one missing"),
    ],
)
def test_should_raise_if_columns_do_not_exist(table: Table, selector: str | list[str]) -> None:
    with pytest.raises(ColumnNotFoundError):
        check_columns_exist(table, selector)


def test_should_include_did_you_mean_hint() -> None:
    table = Table({"apple": [], "banana": []})
    with pytest.raises(ColumnNotFoundError, match="Did you mean"):
        check_columns_exist(table, "aple")
