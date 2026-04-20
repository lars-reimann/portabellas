import re

import pytest

from portabellas import Column


@pytest.mark.parametrize(
    "column",
    [
        pytest.param(Column("col1", []), id="empty"),
        pytest.param(Column("col1", [0]), id="non-empty"),
    ],
)
class TestHtml:
    def test_should_contain_table_element(self, column: Column) -> None:
        pattern = r"<table.*?>.*?</table>"
        assert re.search(pattern, column._repr_html_(), flags=re.DOTALL) is not None

    def test_should_contain_th_element_for_column_name(self, column: Column) -> None:
        assert f"<th>{column.name}</th>" in column._repr_html_()

    def test_should_contain_td_element_for_each_value(self, column: Column) -> None:
        for value in column:
            assert f"<td>{value}</td>" in column._repr_html_()
