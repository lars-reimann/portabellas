import pytest

from portabellas import Table
from portabellas._validation import check_columns_dont_exist
from portabellas.exceptions import DuplicateColumnError


@pytest.mark.parametrize(
    ("table", "new_names"),
    [
        pytest.param(Table({}), "a", id="empty table, new name"),
        pytest.param(Table({"a": []}), "b", id="non-empty table, new name"),
        pytest.param(Table({"a": []}), ["b", "c"], id="non-empty table, multiple new names"),
    ],
)
def test_should_not_raise_if_columns_dont_exist(table: Table, new_names: str | list[str]) -> None:
    check_columns_dont_exist(table, new_names)


@pytest.mark.parametrize(
    ("table", "new_names"),
    [
        pytest.param(Table({"a": []}), "a", id="duplicate single column"),
        pytest.param(Table({"a": []}), ["a", "b"], id="one duplicate in list"),
    ],
)
def test_should_raise_if_columns_exist(table: Table, new_names: str | list[str]) -> None:
    with pytest.raises(DuplicateColumnError):
        check_columns_dont_exist(table, new_names)


def test_should_exclude_old_name() -> None:
    table = Table({"a": [], "b": []})
    check_columns_dont_exist(table, "a", old_name="a")
