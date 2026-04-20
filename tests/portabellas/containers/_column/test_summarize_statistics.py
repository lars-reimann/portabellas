import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("column", "expected_statistic_names"),
    [
        pytest.param(
            Column("col1", []),
            ["min", "max", "mean", "median", "standard deviation", "missing value count"],
            id="empty",
        ),
        pytest.param(
            Column("col1", [1, 2, 1, None]),
            ["min", "max", "mean", "median", "standard deviation", "missing value count"],
            id="numeric",
        ),
    ],
)
def test_should_return_table_with_statistic_rows(column: Column, expected_statistic_names: list[str]) -> None:
    result = column.summarize_statistics()
    assert result.column_names[0] == "statistic"
    assert result["statistic"].to_list() == expected_statistic_names


def test_should_delegate_to_table_summarize_statistics() -> None:
    column = Column("a", [1, 3])
    result = column.summarize_statistics()
    assert result.row_count == 6
    assert result.column_count == 2
