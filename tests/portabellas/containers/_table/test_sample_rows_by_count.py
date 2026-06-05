from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "count", "with_replacement", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": []}),
            0,
            False,
            Table({"col1": []}),
            id="empty table",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            0,
            False,
            Table({"col1": []}),
            id="sample no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            2,
            False,
            Table({"col1": [1, 2]}),
            id="sample some rows without replacement",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            3,
            False,
            Table({"col1": [1, 2, 3]}),
            id="sample all rows without replacement",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            5,
            True,
            Table({"col1": [1, 2, 2, 1, 2]}),
            id="oversample with replacement",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            2,
            False,
            Table({"col1": [1, 2], "col2": [4, 5]}),
            id="multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_sample_rows_by_count(
        self,
        table_factory: Callable[[], Table],
        count: int,
        with_replacement: bool,
        expected: Table,
    ) -> None:
        actual = table_factory().sample_rows_by_count(count, with_replacement=with_replacement)
        assert_tables_are_equal(actual, expected, ignore_types=actual.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        count: int,
        with_replacement: bool,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sample_rows_by_count(count, with_replacement=with_replacement)
        assert_tables_are_equal(original, table_factory())


def test_should_produce_same_result_with_same_seed() -> None:
    table = Table({"col1": [1, 2, 3, 4, 5]})
    result1 = table.sample_rows_by_count(3, random_seed=42)
    result2 = table.sample_rows_by_count(3, random_seed=42)
    assert_tables_are_equal(result1, result2)


def test_should_sample_with_none_seed() -> None:
    table = Table({"col1": [1, 2, 3]})
    result = table.sample_rows_by_count(2, random_seed=None)
    assert result.row_count == 2


def test_should_raise_if_count_is_negative() -> None:
    table = Table({"col1": [1, 2, 3]})
    with pytest.raises(OutOfBoundsError):
        table.sample_rows_by_count(-1)


def test_should_raise_if_count_exceeds_row_count_without_replacement() -> None:
    table = Table({"col1": [1, 2, 3]})
    with pytest.raises(OutOfBoundsError):
        table.sample_rows_by_count(4)
