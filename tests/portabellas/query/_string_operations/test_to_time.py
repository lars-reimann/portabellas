from datetime import time

import pytest

from portabellas import Column
from portabellas.typing import DataType

NO_FRACTIONAL = time(4, 5, 6)
WITH_MILLISECOND = time(4, 5, 6, 7000)
WITH_MICROSECOND = time(4, 5, 6, 7)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("04:05:06", NO_FRACTIONAL, id="time without fractional seconds"),
        pytest.param("04:05:06.007", WITH_MILLISECOND, id="time with milliseconds"),
        pytest.param("04:05:06.000007", WITH_MICROSECOND, id="time with microseconds"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_handle_iso_8601(value: str | None, expected: str | None) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_time(format="iso"),
        expected,
        type_if_none=DataType.String(),
    )


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param("04:05:06", "{h}:{m}:{s}", NO_FRACTIONAL, id="{h}:{m}:{s}"),
        pytest.param(" 4: 5: 6", "{_h}:{_m}:{_s}", NO_FRACTIONAL, id="{_h}:{_m}:{_s}"),
        pytest.param("4:5:6", "{^h}:{^m}:{^s}", NO_FRACTIONAL, id="{^h}:{^m}:{^s}"),
        pytest.param("04:05:06 am", "{h12}:{m}:{s} {am/pm}", NO_FRACTIONAL, id="{h12}:{m}:{s} {am/pm}"),
        pytest.param(" 4: 5: 6 AM", "{_h12}:{m}:{s} {AM/PM}", NO_FRACTIONAL, id="{_h12}:{m}:{s} {AM/PM}"),
        pytest.param("4:5:6 AM", "{^h12}:{m}:{s} {AM/PM}", NO_FRACTIONAL, id="{^h12}:{m}:{s} {AM/PM}"),
        pytest.param("04:05:06 .000007", "{h}:{m}:{s} {.f}", WITH_MICROSECOND, id="{.f}"),
        pytest.param("04:05:06 007", "{h}:{m}:{s} {ms}", WITH_MILLISECOND, id="{ms}"),
        pytest.param("04:05:06 000007", "{h}:{m}:{s} {us}", WITH_MICROSECOND, id="{us}"),
        pytest.param("04:05:06 000007000", "{h}:{m}:{s} {ns}", WITH_MICROSECOND, id="{ns}"),
        pytest.param("04", "{h}", None, id="no minute"),
        pytest.param("05", "{m}", None, id="no hour"),
        pytest.param("04:05:06 04", "{h}:{m}:{s} {h}", NO_FRACTIONAL, id="duplicate field, same value"),
        pytest.param("04:05:06 07", "{h}:{m}:{s} {h}", None, id="duplicate field, different value"),
        pytest.param("04:05:06 04", "{h}:{m}:{s} {h12}", NO_FRACTIONAL, id="similar field, same value"),
        pytest.param("04:05:06 07", "{h}:{m}:{s} {h12}", None, id="similar field, different value"),
        pytest.param("24:00:00", "{h}:{m}:{s}", None, id="out of bounds"),
        pytest.param("invalid", "{h}:{m}:{s}", None, id="no match"),
    ],
)
def test_should_handle_custom_format_string(value: str, format_: str, expected: time) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_time(format=format_),
        expected,
    )


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param("04:05\\", "{h}:{m}\\", time(4, 5), id="backslash at end"),
        pytest.param("04:05\\", "{h}:{m}\\\\", time(4, 5), id="escaped backslash"),
        pytest.param("04:05{", "{h}:{m}\\{", time(4, 5), id="escaped open curly brace"),
        pytest.param("04:05%", "{h}:{m}%", time(4, 5), id="percent"),
        pytest.param("04:05\n", "{h}:{m}\n", time(4, 5), id="newline"),
        pytest.param("04:05\t", "{h}:{m}\t", time(4, 5), id="tab"),
    ],
)
def test_should_handle_escape_sequences(value: str, format_: str, expected: time) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_time(format=format_),
        expected,
    )


def test_should_raise_for_unclosed_specifier() -> None:
    column = Column("a", ["04:05:06"])
    with pytest.raises(ValueError, match="Unclosed specifier"):
        column.map(lambda cell: cell.str.to_time(format="{m"))


@pytest.mark.parametrize(
    "format_",
    [
        pytest.param("{invalid}", id="globally invalid"),
        pytest.param("{Y}", id="invalid for time"),
    ],
)
def test_should_raise_for_invalid_specifier(format_: str) -> None:
    column = Column("a", ["04:05:06"])
    with pytest.raises(ValueError, match="Invalid specifier"):
        column.map(lambda cell: cell.str.to_time(format=format_))
