from datetime import UTC, date, datetime, time

import pytest

from portabellas import Column
from portabellas.exceptions import LazyComputationError
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type

DATETIME = datetime(1, 2, 3, 4, 5, 6, 7, tzinfo=UTC)
DATE = date(1, 2, 3)
TIME = time(4, 5, 6, 7)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1, 2, 3, 4, 5, 6, 7), "0001-02-03T04:05:06.000007", id="datetime without time zone"),  # noqa: DTZ001
        pytest.param(DATETIME, "0001-02-03T04:05:06.000007+00:00", id="datetime with time zone"),
        pytest.param(DATE, "0001-02-03", id="date"),
        pytest.param(TIME, "04:05:06.000007", id="time"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_handle_iso_8601(value: datetime | date | time | None, expected: str | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.dt.to_string(format="iso"),
        expected,
        type_if_none=DataTypes.Datetime(),
    )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(DATETIME, id="datetime"),
        pytest.param(DATE, id="date"),
    ],
)
class TestDateSpecifiers:
    @pytest.mark.parametrize(
        ("format_", "expected"),
        [
            pytest.param("{Y}", "0001", id="{Y}"),
            pytest.param("{_Y}", "   1", id="{_Y}"),
            pytest.param("{^Y}", "1", id="{^Y}"),
            pytest.param("{Y99}", "01", id="{Y99}"),
            pytest.param("{_Y99}", " 1", id="{_Y99}"),
            pytest.param("{^Y99}", "1", id="{^Y99}"),
            pytest.param("{M}", "02", id="{M}"),
            pytest.param("{_M}", " 2", id="{_M}"),
            pytest.param("{^M}", "2", id="{^M}"),
            pytest.param("{M-full}", "February", id="{M-full}"),
            pytest.param("{M-short}", "Feb", id="{M-short}"),
            pytest.param("{W}", "05", id="{W}"),
            pytest.param("{_W}", " 5", id="{_W}"),
            pytest.param("{^W}", "5", id="{^W}"),
            pytest.param("{D}", "03", id="{D}"),
            pytest.param("{_D}", " 3", id="{_D}"),
            pytest.param("{^D}", "3", id="{^D}"),
            pytest.param("{DOW}", "6", id="{DOW}"),
            pytest.param("{DOW-full}", "Saturday", id="{DOW-full}"),
            pytest.param("{DOW-short}", "Sat", id="{DOW-short}"),
            pytest.param("{DOY}", "034", id="{DOY}"),
            pytest.param("{_DOY}", " 34", id="{_DOY}"),
            pytest.param("{^DOY}", "34", id="{^DOY}"),
        ],
    )
    def test_should_be_replaced_with_correct_string(self, value: datetime | date, format_: str, expected: str) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.dt.to_string(format=format_),
            expected,
        )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(DATETIME, id="datetime"),
        pytest.param(TIME, id="time"),
    ],
)
class TestTimeSpecifiers:
    @pytest.mark.parametrize(
        ("format_", "expected"),
        [
            pytest.param("{h}", "04", id="{h}"),
            pytest.param("{_h}", " 4", id="{_h}"),
            pytest.param("{^h}", "4", id="{^h}"),
            pytest.param("{h12}", "04", id="{h12}"),
            pytest.param("{_h12}", " 4", id="{_h12}"),
            pytest.param("{^h12}", "4", id="{^h12}"),
            pytest.param("{m}", "05", id="{m}"),
            pytest.param("{_m}", " 5", id="{_m}"),
            pytest.param("{^m}", "5", id="{^m}"),
            pytest.param("{s}", "06", id="{s}"),
            pytest.param("{_s}", " 6", id="{_s}"),
            pytest.param("{^s}", "6", id="{^s}"),
            pytest.param("{.f}", ".000007", id="{.f}"),
            pytest.param("{ms}", "000", id="{ms}"),
            pytest.param("{us}", "000007", id="{us}"),
            pytest.param("{ns}", "000007000", id="{ns}"),
            pytest.param("{AM/PM}", "AM", id="{AM/PM}"),
            pytest.param("{am/pm}", "am", id="{am/pm}"),
        ],
    )
    def test_should_be_replaced_with_correct_string(self, value: datetime | time, format_: str, expected: str) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.dt.to_string(format=format_),
            expected,
        )


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(DATETIME, id="datetime"),
    ],
)
class TestDatetimeSpecifiers:
    @pytest.mark.parametrize(
        ("format_", "expected"),
        [
            pytest.param("{z}", "+0000", id="{z}"),
            pytest.param("{:z}", "+00:00", id="{:z}"),
            pytest.param("{u}", "-62132730894", id="{u}"),
        ],
    )
    def test_should_be_replaced_with_correct_string(self, value: datetime, format_: str, expected: str) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.dt.to_string(format=format_),
            expected,
        )


@pytest.mark.parametrize(
    ("format_", "expected"),
    [
        pytest.param("\\", "\\", id="backslash at end"),
        pytest.param("\\\\", "\\", id="escaped backslash"),
        pytest.param("\\{", "{", id="escaped open curly brace"),
        pytest.param("%", "%", id="percent"),
        pytest.param("\n", "\n", id="newline"),
        pytest.param("\t", "\t", id="tab"),
    ],
)
def test_should_handle_escape_sequences(format_: str, expected: str) -> None:
    assert_cell_operation_works(
        DATETIME,
        lambda cell: cell.dt.to_string(format=format_),
        expected,
    )


def test_should_raise_for_unclosed_specifier() -> None:
    column = Column("a", [DATETIME])
    with pytest.raises(ValueError, match="Unclosed specifier"):
        column.map(lambda cell: cell.dt.to_string(format="{Y"))


def test_should_raise_for_invalid_specifier() -> None:
    column = Column("a", [DATETIME])
    with pytest.raises(ValueError, match="Invalid specifier"):
        column.map(lambda cell: cell.dt.to_string(format="{invalid}"))


@pytest.mark.parametrize(
    ("value", "format_"),
    [
        pytest.param(DATE, "{h}", id="invalid for date"),
        pytest.param(
            TIME,
            "{Y}",
            marks=pytest.mark.skip("polars panics in this case (https://github.com/pola-rs/polars/issues/19853)."),
            id="invalid for time",
        ),
    ],
)
def test_should_raise_for_specifier_that_is_invalid_for_type(value: date | time, format_: str) -> None:
    column = Column("a", [value])
    lazy_result = column.map(lambda cell: cell.dt.to_string(format=format_))
    with pytest.raises(LazyComputationError):
        lazy_result[0]


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Datetime()).dt.to_string()
    assert_cell_has_type(result, DataTypes.String())
