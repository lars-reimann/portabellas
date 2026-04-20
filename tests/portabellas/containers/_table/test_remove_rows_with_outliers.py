from collections.abc import Callable

import pytest

from portabellas import Table
from portabellas.exceptions import OutOfBoundsError
from tests.helpers import assert_tables_are_equal


@pytest.mark.parametrize(
    ("table_factory", "column_names", "z_score_threshold", "expected"),
    [
        pytest.param(
            lambda: Table({}),
            None,
            1,
            Table({}),
            id="empty",
        ),
        pytest.param(
            lambda: Table({"col1": []}),
            None,
            1,
            Table({"col1": []}),
            id="no rows",
        ),
        pytest.param(
            lambda: Table({"col1": [None, None]}),
            None,
            1,
            Table({"col1": [None, None]}),
            id="only missing values",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 1]}),
            None,
            1,
            Table({"col1": [1, 1, 1]}),
            id="no outliers (low threshold)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1000]}),
            None,
            3,
            Table({"col1": [1, 1000]}),
            id="no outliers (high threshold)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 1000], "col2": [1, 1000, 1], "col3": [1000, 1, 1]}),
            None,
            1,
            Table({"col1": [], "col2": [], "col3": []}),
            id="outliers (all columns selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 1000], "col2": [1, 1000, 1], "col3": [1000, 1, 1]}),
            ["col1", "col2"],
            1,
            Table({"col1": [1], "col2": [1], "col3": [1000]}),
            id="outliers (several columns selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 1000], "col2": [1, 1000, 1], "col3": [1000, 1, 1]}),
            "col1",
            1,
            Table({"col1": [1, 1], "col2": [1, 1000], "col3": [1000, 1]}),
            id="outliers (one column selected)",
        ),
        pytest.param(
            lambda: Table({"col1": [1, 1, 1000], "col2": [1, 1000, 1], "col3": [1000, 1, 1]}),
            [],
            1,
            Table({"col1": [1, 1, 1000], "col2": [1, 1000, 1], "col3": [1000, 1, 1]}),
            id="outliers (no columns selected)",
        ),
    ],
)
class TestHappyPath:
    def test_should_remove_rows_with_outliers(
        self,
        table_factory: Callable[[], Table],
        column_names: str | list[str] | None,
        z_score_threshold: float,
        expected: Table,
    ) -> None:
        actual = table_factory().remove_rows_with_outliers(
            selector=column_names,
            z_score_threshold=z_score_threshold,
        )
        assert_tables_are_equal(actual, expected, ignore_types=actual.row_count == 0)

    def test_should_not_mutate_receiver(
        self,
        table_factory: Callable[[], Table],
        column_names: str | list[str] | None,
        z_score_threshold: float,
        expected: Table,  # noqa: ARG002
    ) -> None:
        original = table_factory()
        original.remove_rows_with_outliers(
            selector=column_names,
            z_score_threshold=z_score_threshold,
        )
        assert_tables_are_equal(original, table_factory())


def test_should_raise_if_z_score_threshold_is_negative() -> None:
    with pytest.raises(OutOfBoundsError):
        Table({}).remove_rows_with_outliers(z_score_threshold=-1.0)
