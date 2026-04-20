import pytest

from portabellas import Table
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, Schema


@pytest.mark.parametrize(
    ("table_or_schema", "selector", "operation"),
    [
        pytest.param(
            Table({"col1": [1, 2], "col2": ["a", "b"]}),
            "col2",
            "do a numeric operation",
            id="single non-numeric column (table)",
        ),
        pytest.param(
            Table({"col1": [1, 2], "col2": ["a", "b"]}),
            ["col2"],
            "do a numeric operation",
            id="list with non-numeric column (table)",
        ),
        pytest.param(
            Schema({"col1": DataType.Int64(), "col2": DataType.String()}),
            "col2",
            "do a numeric operation",
            id="single non-numeric column (schema)",
        ),
    ],
)
def test_should_raise_if_columns_are_not_numeric(
    table_or_schema: Table | Schema,
    selector: str | list[str],
    operation: str,
) -> None:
    from portabellas._validation import check_columns_are_numeric

    with pytest.raises(ColumnTypeError):
        check_columns_are_numeric(table_or_schema, selector, operation=operation)


@pytest.mark.parametrize(
    ("table_or_schema", "selector"),
    [
        pytest.param(
            Table({"col1": [1, 2], "col2": ["a", "b"]}),
            "col1",
            id="single numeric column (table)",
        ),
        pytest.param(
            Table({"col1": [1, 2], "col2": ["a", "b"]}),
            ["col1"],
            id="list with numeric column (table)",
        ),
        pytest.param(
            Table({"col1": [1, 2], "col2": ["a", "b"]}),
            "unknown",
            id="unknown column (ignored)",
        ),
        pytest.param(
            Schema({"col1": DataType.Int64(), "col2": DataType.String()}),
            "col1",
            id="single numeric column (schema)",
        ),
    ],
)
def test_should_not_raise_if_columns_are_numeric(
    table_or_schema: Table | Schema,
    selector: str | list[str],
) -> None:
    from portabellas._validation import check_columns_are_numeric

    check_columns_are_numeric(table_or_schema, selector)
