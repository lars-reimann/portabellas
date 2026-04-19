from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell


@pytest.mark.parametrize(
    ("column_factory", "mapper", "expected"),
    [
        pytest.param(
            lambda: Column("col1", []),
            lambda _: Cell.constant(None),
            Column("col1", []),
            id="empty (constant value)",
        ),
        pytest.param(
            lambda: Column("col1", [1, 2, 3]),
            lambda _: Cell.constant(None),
            Column("col1", [None, None, None]),
            id="non-empty (constant value)",
        ),
        pytest.param(
            lambda: Column("col1", [1, 2, None]),
            lambda cell: cell.eq(2),
            Column("col1", [False, True, None]),
            id="non-empty (computed value)",
        ),
    ],
)
class TestHappyPath:
    def test_should_map_column(
        self,
        column_factory: Callable[[], Column],
        mapper: Callable[[Cell], Cell],
        expected: Column,
    ) -> None:
        actual = column_factory().map(mapper)
        assert actual.name == expected.name
        assert list(actual) == list(expected)

    def test_should_not_mutate_receiver(
        self,
        column_factory: Callable[[], Column],
        mapper: Callable[[Cell], Cell],
        expected: Column,  # noqa: ARG002
    ) -> None:
        original = column_factory()
        original.map(mapper)
        assert original.name == column_factory().name
        assert list(original) == list(column_factory())
