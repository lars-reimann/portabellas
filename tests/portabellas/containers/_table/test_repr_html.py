import re

import pytest

from portabellas import Table


@pytest.mark.parametrize(
    "table",
    [
        pytest.param(Table({}), id="empty"),
        pytest.param(Table({"col1": []}), id="no rows"),
        pytest.param(Table({"col1": [1, 2], "col2": [3, 4]}), id="with data"),
    ],
)
class TestHtml:
    def test_should_contain_table_element(self, table: Table) -> None:
        pattern = r"<table.*?>.*?</table>"
        assert re.search(pattern, table._repr_html_(), flags=re.DOTALL) is not None

    def test_should_contain_th_element_for_each_column_name(self, table: Table) -> None:
        for column_name in table.column_names:
            assert f"<th>{column_name}</th>" in table._repr_html_()

    def test_should_contain_td_element_for_each_value(self, table: Table) -> None:
        for column_name in table.column_names:
            column = table[column_name]
            for value in column:
                assert f"<td>{value}</td>" in table._repr_html_()
