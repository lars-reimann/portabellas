from collections.abc import Callable

import pytest

from portabellas import Column


@pytest.mark.parametrize(
    ("column_factory", "new_name", "expected"),
    [
        pytest.param(
            lambda: Column("col1", []),
            "col2",
            Column("col2", []),
            id="empty",
        ),
        pytest.param(
            lambda: Column("col1", [0]),
            "col2",
            Column("col2", [0]),
            id="non-empty",
        ),
    ],
)
def test_should_rename_column(
    column_factory: Callable[[], Column],
    new_name: str,
    expected: Column,
) -> None:
    actual = column_factory().rename(new_name)
    assert actual.name == expected.name
    assert list(actual) == list(expected)


@pytest.mark.parametrize(
    ("column_factory", "new_name"),
    [
        pytest.param(
            lambda: Column("col1", []),
            "col2",
            id="empty",
        ),
        pytest.param(
            lambda: Column("col1", [0]),
            "col2",
            id="non-empty",
        ),
    ],
)
def test_should_not_mutate_receiver(
    column_factory: Callable[[], Column],
    new_name: str,
) -> None:
    original = column_factory()
    original.rename(new_name)
    assert original.name == column_factory().name
    assert list(original) == list(column_factory())
