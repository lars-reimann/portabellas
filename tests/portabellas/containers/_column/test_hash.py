from collections.abc import Callable

import pytest

from portabellas import Column


@pytest.mark.parametrize(
    "column_factory",
    [
        pytest.param(lambda: Column("col1", []), id="no rows"),
        pytest.param(lambda: Column("col1", [1, 2]), id="with data"),
    ],
)
class TestContract:
    def test_should_return_same_hash_for_equal_objects(self, column_factory: Callable[[], Column]) -> None:
        column_1 = column_factory()
        column_2 = column_factory()
        assert hash(column_1) == hash(column_2)


@pytest.mark.parametrize(
    ("column_1", "column_2"),
    [
        pytest.param(Column("col1", [1]), Column("col2", [1]), id="different names"),
        pytest.param(Column("col1", [1]), Column("col1", ["1"]), id="different types"),
        pytest.param(Column("col1", [1, 2]), Column("col1", [1]), id="too few rows"),
        pytest.param(Column("col1", [1]), Column("col1", [1, 2]), id="too many rows"),
    ],
)
def test_should_return_different_hash_for_unequal_objects(column_1: Column, column_2: Column) -> None:
    assert hash(column_1) != hash(column_2)
