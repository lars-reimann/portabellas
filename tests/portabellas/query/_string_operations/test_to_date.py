from datetime import date

import pytest

from portabellas import Column
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works

DATE = date(1, 2, 3)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("0001-02-03", DATE, id="date"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_handle_iso_8601(value: str | None, expected: str | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_date(format="iso"),
        expected,
        type_if_none=DataType.String(),
    )


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param("0001-02-03", "{Y}-{M}-{D}", DATE, id="{Y}-{M}-{D}"),
        pytest.param("   1- 2- 3", "{_Y}-{_M}-{_D}", DATE, id="{_Y}-{_M}-{_D}"),
        pytest.param("1-2-3", "{^Y}-{^M}-{^D}", DATE, id="{^Y}-{^M}-{^D}"),
        pytest.param("01", "{Y99}", date(2001, 1, 1), id="{Y99}"),
        pytest.param(" 1", "{_Y99}", None, id="{_Y99}"),
        pytest.param("1", "{^Y99}", None, id="{^Y99}"),
        pytest.param("0001-February-03", "{Y}-{M-full}-{D}", DATE, id="{Y}-{M-full}-{D}"),
        pytest.param("0001-Feb-03", "{Y}-{M-short}-{D}", DATE, id="{Y}-{M-short}-{D}"),
        pytest.param("0001-02-03 05| 5|5", "{Y}-{M}-{D} {W}|{_W}|{^W}", DATE, id="week number"),
        pytest.param(
            "0001-02-03 6|Saturday|Sat", "{Y}-{M}-{D} {DOW}|{DOW-full}|{DOW-short}", DATE, id="day of the week"
        ),
        pytest.param("0001/034", "{Y}/{DOY}", DATE, id="{Y}/{DOY}"),
        pytest.param("   1/ 34", "{Y}/{_DOY}", DATE, id="{Y}/{_DOY}"),
        pytest.param("   1/034", "{Y}/{^DOY}", DATE, id="{Y}/{^DOY}"),
        pytest.param("0001-02-03 0001", "{Y}-{M}-{D} {Y}", DATE, id="duplicate field, same value"),
        pytest.param("0001-02-03 0004", "{Y}-{M}-{D} {Y}", date(4, 2, 3), id="duplicate field, different value"),
        pytest.param("0001-02-03 01", "{Y}-{M}-{D} {Y99}", date(2001, 2, 3), id="similar field, same value"),
        pytest.param("0001-02-03 04", "{Y}-{M}-{D} {Y99}", date(2004, 2, 3), id="similar field, different value"),
        pytest.param("24:00:00", "{Y}-{M}-{D}", None, id="out of bounds"),
        pytest.param("invalid", "{Y}-{M}-{D}", None, id="no match"),
    ],
)
def test_should_handle_custom_format_string(value: str, format_: str, expected: date) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_date(format=format_),
        expected,
    )


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param("0001-02-03\\", "{Y}-{M}-{D}\\", DATE, id="backslash at end"),
        pytest.param("0001-02-03\\", "{Y}-{M}-{D}\\\\", DATE, id="escaped backslash"),
        pytest.param("0001-02-03{", "{Y}-{M}-{D}\\{", DATE, id="escaped open curly brace"),
        pytest.param("0001-02-03%", "{Y}-{M}-{D}%", DATE, id="percent"),
        pytest.param("0001-02-03\n", "{Y}-{M}-{D}\n", DATE, id="newline"),
        pytest.param("0001-02-03\t", "{Y}-{M}-{D}\t", DATE, id="tab"),
    ],
)
def test_should_handle_escape_sequences(value: str, format_: str, expected: date) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_date(format=format_),
        expected,
    )


def test_should_raise_for_unclosed_specifier() -> None:
    column = Column("a", ["0001-02-03"])
    with pytest.raises(ValueError, match="Unclosed specifier"):
        column.map(lambda cell: cell.str.to_date(format="{Y"))


@pytest.mark.parametrize(
    "format_",
    [
        pytest.param("{invalid}", id="globally invalid"),
        pytest.param("{m}", id="invalid for date"),
    ],
)
def test_should_raise_for_invalid_specifier(format_: str) -> None:
    column = Column("a", ["0001-02-03"])
    with pytest.raises(ValueError, match="Invalid specifier"):
        column.map(lambda cell: cell.str.to_date(format=format_))
