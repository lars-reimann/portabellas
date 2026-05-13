from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError, PortabellasError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "fraction", "expected_row_count"),
    [
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            0.5,
            2,
            id="half the rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            1.0,
            4,
            id="all rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4], "col2": [5, 6, 7, 8]}),
            0.5,
            2,
            id="multiple columns",
        ),
    ],
)
class TestHappyPath:
    def test_should_sample_rows_by_fraction(
        self,
        table_factory: Callable[[], Table],
        fraction: float,
        expected_row_count: int,
    ) -> None:
        result = table_factory().sample_rows_by_fraction(fraction)
        assert result.row_count == expected_row_count

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        fraction: float,
        expected_row_count: int,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.sample_rows_by_fraction(fraction)
        assert_tables_are_equal(original, table_factory())


class TestWithReplacement:
    def test_should_allow_fraction_greater_than_one_with_replacement(self) -> None:
        table = Table({"col1": [1, 2, 3, 4]})
        result = table.sample_rows_by_fraction(2.0, with_replacement=True)
        assert result.row_count == 8

    def test_should_oversample_with_replacement(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        result = table.sample_rows_by_fraction(1.5, with_replacement=True)
        assert result.row_count == 4


class TestRandomSeed:
    def test_should_produce_same_result_with_same_seed(self) -> None:
        table = Table({"col1": list(range(20))})
        result1 = table.sample_rows_by_fraction(0.5, random_seed=42)
        result2 = table.sample_rows_by_fraction(0.5, random_seed=42)
        assert_tables_are_equal(result1, result2)

    def test_should_sample_with_none_seed(self) -> None:
        table = Table({"col1": [1, 2, 3, 4]})
        result = table.sample_rows_by_fraction(0.5, random_seed=None)
        assert result.row_count == 2


class TestValidation:
    def test_should_raise_if_fraction_is_zero(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(OutOfBoundsError):
            table.sample_rows_by_fraction(0.0)

    def test_should_raise_if_fraction_is_negative(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(OutOfBoundsError):
            table.sample_rows_by_fraction(-0.5)

    def test_should_raise_if_fraction_exceeds_one_without_replacement(self) -> None:
        table = Table({"col1": [1, 2, 3]})
        with pytest.raises(OutOfBoundsError):
            table.sample_rows_by_fraction(1.5)

    def test_should_raise_on_empty_table(self) -> None:
        table = Table({"col1": []})
        with pytest.raises(PortabellasError):
            table.sample_rows_by_fraction(0.5)
