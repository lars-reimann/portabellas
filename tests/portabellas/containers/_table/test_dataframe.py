import pytest
from polars import from_dataframe

from portabellas import Table


@pytest.mark.parametrize(
    "table",
    [
        pytest.param(Table({}), id="empty"),
        pytest.param(Table({"col1": []}), id="no rows"),
        pytest.param(Table({"col1": [1, 2], "col2": [3, 4]}), id="non-empty"),
    ],
)
def test_should_be_able_to_restore_table_from_exchange_object(table: Table) -> None:
    exchange_object = table.__dataframe__()
    restored = Table._from_polars_data_frame(from_dataframe(exchange_object))
    assert restored == table
