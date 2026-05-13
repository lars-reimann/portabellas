from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError, PortabellasError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "count", "expected"),
    [
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            2,
            Table({"col1": [1, 2]}),
            id="sample fewer rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            3,
            Table({"col1": [1, 2, 3]}),
            id="sample all rows without replacement",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3], "col2": [4, 5, 6]}),
            2,
            Table({"col1": [1, 2], "col2": [4, 5]}),
            id="multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_sample_rows(
        self,
        table_factory: Callable[[], Table],
        count: int,
        expected: Table,
    ) -> None:
        actual = table_factory().sample_rows(count)
        assert_tables_are_equal(actual, expected)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        count: int,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sample_rows(count)
        assert_tables_are_equal(original, table_factory())


class TestWithReplacement:
    @pytest.mark.parametrize(
        ("table_factory", "count", "expected"),
        [
            pytest.param(
                lambda: Table({"col1": [1, 2, 3]}),
                5,
                Table({"col1": [1, 2, 2, 1, 2]}),
                id="count exceeds row count",
            ),
        ],
    )
    def test_should_sample_rows_with_replacement(
        self,
        table_factory: Callable[[], Table],
        count: int,
        expected: Table,
    ) -> None:
        actual = table_factory().sample_rows(count, with_replacement=True)
        assert_tables_are_equal(actual, expected)

    def test_should_allow_count_exceeding_row_count_with_replacement(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        result = table.sample_rows(10, with_replacement=True)
        assert result.row_count == 10


class TestRandomSeed:
    def test_should_produce_same_result_with_same_seed(self) -> None:
        table = Table({"col1": [1, 2, 3, 4, 5]})
        result1 = table.sample_rows(3, random_seed=42)
        result2 = table.sample_rows(3, random_seed=42)
        assert_tables_are_equal(result1, result2)

    def test_should_produce_different_result_with_different_seed(self) -> None:
        table = Table({"col1": list(range(100))})
        result1 = table.sample_rows(50, random_seed=1)
        result2 = table.sample_rows(50, random_seed=2)
        assert result1.row_count == 50
        assert result2.row_count == 50

    def test_should_sample_with_none_seed(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        result = table.sample_rows(2, random_seed=None)
        assert result.row_count == 2


class TestValidation:
    def test_should_raise_if_count_is_zero(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(OutOfBoundsError):
            table.sample_rows(0)

    def test_should_raise_if_count_is_negative(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(OutOfBoundsError):
            table.sample_rows(-1)

    def test_should_raise_if_count_exceeds_row_count_without_replacement(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(PortabellasError):
            table.sample_rows(4)

    def test_should_raise_on_empty_table(self) -> None:
        table = Table({"col1": []})
        with pytest.raises(PortabellasError):
            table.sample_rows(1)
