from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "start", "length", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            0,
            None,
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            0,
            None,
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            0,
            None,
            Table({"col1": [1, 2, 3]}),
            id="full table",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            1,
            None,
            Table({"col1": [2, 3]}),
            id="non-negative start in bounds",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            10,
            None,
            Table({"col1": []}),
            id="non-negative start out of bounds",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            -1,
            None,
            Table({"col1": [3]}),
            id="negative start in bounds",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            -10,
            None,
            Table({"col1": [1, 2, 3]}),
            id="negative start out of bounds",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            0,
            1,
            Table({"col1": [1]}),
            id="non-negative length in bounds",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 2, 3]}),
            0,
            10,
            Table({"col1": [1, 2, 3]}),
            id="non-negative length out of bounds",
        ),
    ],
)
class TestHappyPath:
    def test_should_slice_rows(
        self,
        table_factory: Callable[[], Table],
        start: int,
        length: int | None,
        expected: Table,
    ) -> None:
        actual = table_factory().slice_rows(start=start, length=length)
        assert_tables_are_equal(actual, expected, ignore_types=actual.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        start: int,
        length: int | None,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.slice_rows(start=start, length=length)
        assert_tables_are_equal(original, table_factory())


def test_should_raise_for_negative_length() -> None:
    with pytest.raises(OutOfBoundsError):
        Table({}).slice_rows(length=-1)
