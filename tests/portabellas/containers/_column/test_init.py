from typing import Any

import pytest

from portabellas import Column
from portabellas.typing import DataType, DataTypes


def test_should_store_the_name() -> None:
    column = Column("col1", [1])
    assert column.name == "col1"


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        pytest.param(
            Column("col1", []),
            [],
            id="empty",
        ),
        pytest.param(
            Column("col1", [1]),
            [1],
            id="non-empty (inferred type)",
        ),
        pytest.param(
            Column("col1", [1], type=DataTypes.String()),
            ["1"],
            id="non-empty (manifest type)",
        ),
    ],
)
def test_should_store_the_data(column: Column, expected: list[Any]) -> None:
    assert list(column) == expected


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        pytest.param(
            Column("col1", []),
            DataTypes.Null(),
            id="empty",
        ),
        pytest.param(
            Column("col1", [1]),
            DataTypes.Int64(),
            id="non-empty (inferred type)",
        ),
        pytest.param(
            Column("col1", [1], type=DataTypes.String()),
            DataTypes.String(),
            id="non-empty (manifest type)",
        ),
    ],
)
def test_should_have_correct_type(column: Column, expected: DataType) -> None:
    assert column.type == expected
