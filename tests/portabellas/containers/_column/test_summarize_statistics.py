import datetime
from statistics import stdev

import pytest

from portabellas import Column, Table
from tests.helpers import assert_tables_are_equal

_HEADERS = ["min", "max", "mean", "median", "standard deviation", "missing value count"]
_EMPTY_COLUMN_RESULT = [None, None, None, None, None, 0]


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        pytest.param(
            Column("col1", []),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": _EMPTY_COLUMN_RESULT,
                },
            ),
            id="no rows",
        ),
        pytest.param(
            Column("col1", [None, None, None]),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": [None, None, None, None, None, 3],
                },
            ),
            id="null column",
        ),
        pytest.param(
            Column("col1", [1, 2, 1, None]),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": [1, 2, 4 / 3, 1, stdev([1, 2, 1]), 1],
                },
            ),
            id="numeric column",
        ),
        pytest.param(
            Column(
                "col1",
                [
                    datetime.time(1, 2, 3),
                    datetime.time(4, 5, 6),
                    datetime.time(7, 8, 9),
                    None,
                ],
            ),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": ["01:02:03", "07:08:09", None, None, None, "1"],
                },
            ),
            id="temporal column",
        ),
        pytest.param(
            Column("col1", ["a", "b", "c", None]),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": ["a", "c", None, None, None, "1"],
                },
            ),
            id="string column",
        ),
        pytest.param(
            Column("col1", [True, False, True, None]),
            Table(
                {
                    "statistic": _HEADERS,
                    "col1": ["false", "true", None, None, None, "1"],
                },
            ),
            id="boolean column",
        ),
    ],
)
def test_should_summarize_statistics(column: Column, expected: Table) -> None:
    actual = column.summarize_statistics()
    assert_tables_are_equal(actual, expected, ignore_types=True, ignore_float_imprecision=True)


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        pytest.param(
            Column("statistic", []),
            Table(
                {
                    "statistic_": _HEADERS,
                    "statistic": _EMPTY_COLUMN_RESULT,
                },
            ),
            id="statistic column",
        ),
    ],
)
def test_should_ensure_new_column_has_unique_name(column: Column, expected: Table) -> None:
    actual = column.summarize_statistics()
    assert_tables_are_equal(actual, expected, ignore_types=True)
