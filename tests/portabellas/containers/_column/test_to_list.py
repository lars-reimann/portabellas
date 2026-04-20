import pytest

from portabellas import Column


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([], id="empty"),
        pytest.param([0], id="non-empty"),
    ],
)
def test_should_return_list_of_column_values(values: list) -> None:
    column = Column("col1", values)
    assert column.to_list() == values
