from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "percentage_in_first", "shuffle", "expected_1", "expected_2"),
    [
        pytest.param(
            lambda: Table({}),
            0.0,
            False,
            Table({}),
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            0.0,
            False,
            Table({"col1": []}),
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            1.0,
            False,
            Table({"col1": [1, 2, 3, 4]}),
            Table({"col1": []}),
            id="all in first, no shuffle",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            1.0,
            True,
            Table({"col1": [4, 1, 2, 3]}),
            Table({"col1": []}),
            id="all in first, shuffle",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            0.0,
            False,
            Table({"col1": []}),
            Table({"col1": [1, 2, 3, 4]}),
            id="all in second, no shuffle",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            0.0,
            True,
            Table({"col1": []}),
            Table({"col1": [4, 1, 2, 3]}),
            id="all in second, shuffle",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            0.5,
            False,
            Table({"col1": [1, 2]}),
            Table({"col1": [3, 4]}),
            id="even split, no shuffle",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3, 4]}),
            0.5,
            True,
            Table({"col1": [4, 1]}),
            Table({"col1": [2, 3]}),
            id="even split, shuffle",
        ),
    ],
)
class TestHappyPath:
    def test_should_split_rows(
        self,
        table_factory: Callable[[], Table],
        percentage_in_first: float,
        shuffle: bool,
        expected_1: Table,
        expected_2: Table,
    ) -> None:
        actual_1, actual_2 = table_factory().split_rows(percentage_in_first, shuffle=shuffle)
        assert_tables_are_equal(actual_1, expected_1, ignore_types=actual_1.row_count == 0)
        assert_tables_are_equal(actual_2, expected_2, ignore_types=actual_2.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        percentage_in_first: float,
        shuffle: bool,
        expected_1: Table,  # noqa: ARG002
        expected_2: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.split_rows(percentage_in_first, shuffle=shuffle)
        assert_tables_are_equal(original, table_factory())


@pytest.mark.parametrize(
    "percentage_in_first",
    [
        pytest.param(-1.0, id="too low"),
        pytest.param(2.0, id="too high"),
    ],
)
def test_should_raise_if_percentage_in_first_is_out_of_bounds(percentage_in_first: float) -> None:
    with pytest.raises(OutOfBoundsError):
        Table({}).split_rows(percentage_in_first)
