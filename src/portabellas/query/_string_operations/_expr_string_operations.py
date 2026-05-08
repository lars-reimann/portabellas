from __future__ import annotations

import re
from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_and_convert_datetime_format, check_bounds
from portabellas.containers._cell._cell import Cell
from portabellas.typing import DataType, DataTypes

from ._string_operations import StringOperations

if TYPE_CHECKING:
    from portabellas.containers._cell import ConvertibleToIntCell, ConvertibleToStringCell


_BOOLEAN = DataTypes.Boolean()
_DATE = DataTypes.Date()
_DATETIME = DataTypes.Datetime(time_unit="us")
_DATETIME_UTC = DataTypes.Datetime(time_unit="us", time_zone="UTC")
_FLOAT64 = DataTypes.Float64()
_INT64 = DataTypes.Int64()
_STRING = DataTypes.String()
_TIME = DataTypes.Time()
_UINT32 = DataTypes.UInt32()
_UNKNOWN = DataTypes.Unknown()


class ExprStringOperations(StringOperations):
    def __init__(self, expression: pl.Expr, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    def contains(self, substring: ConvertibleToStringCell) -> Cell:
        substring_expr = _to_string_expression(substring)

        return _expr_cell(self._expression.str.contains(substring_expr, literal=True), type=_BOOLEAN)

    def ends_with(self, suffix: ConvertibleToStringCell) -> Cell:
        suffix_expr = _to_polars_expression(suffix)

        return _expr_cell(self._expression.str.ends_with(suffix_expr), type=_BOOLEAN)

    def index_of(self, substring: ConvertibleToStringCell) -> Cell:
        substring_expr = _to_string_expression(substring)

        return _expr_cell(self._expression.str.find(substring_expr, literal=True), type=_UINT32)

    def length(self, *, optimize_for_ascii: bool = False) -> Cell:
        if optimize_for_ascii:
            return _expr_cell(self._expression.str.len_bytes(), type=_UINT32)

        return _expr_cell(self._expression.str.len_chars(), type=_UINT32)

    def pad_end(self, length: int, *, character: str = " ") -> Cell:
        check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")
        if len(character) != 1:
            msg = "Can only pad with a single character."
            raise ValueError(msg)

        return _expr_cell(self._expression.str.pad_end(length, character), type=_STRING)

    def pad_start(self, length: int, *, character: str = " ") -> Cell:
        check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")
        if len(character) != 1:
            msg = "Can only pad with a single character."
            raise ValueError(msg)

        return _expr_cell(self._expression.str.pad_start(length, character), type=_STRING)

    def repeat(self, count: ConvertibleToIntCell) -> Cell:
        if isinstance(count, int):
            check_bounds("count", count, lower_bound=0, lower_bound_mode="closed")

        count_expr = _to_polars_expression(count)

        return _expr_cell(self._expression.repeat_by(count_expr).list.join("", ignore_nulls=False), type=_STRING)

    def remove_prefix(self, prefix: ConvertibleToStringCell) -> Cell:
        prefix_expr = _to_string_expression(prefix)

        return _expr_cell(self._expression.str.strip_prefix(prefix_expr), type=_STRING)

    def remove_suffix(self, suffix: ConvertibleToStringCell) -> Cell:
        suffix_expr = _to_string_expression(suffix)

        return _expr_cell(self._expression.str.strip_suffix(suffix_expr), type=_STRING)

    def replace_all(self, old: ConvertibleToStringCell, new: ConvertibleToStringCell) -> Cell:
        old_expr = _to_string_expression(old)
        new_expr = _to_string_expression(new)

        return _expr_cell(self._expression.str.replace_all(old_expr, new_expr, literal=True), type=_STRING)

    def reverse(self) -> Cell:
        return _expr_cell(self._expression.str.reverse(), type=_STRING)

    def slice(
        self,
        *,
        start: ConvertibleToIntCell = 0,
        length: ConvertibleToIntCell = None,
    ) -> Cell:
        if isinstance(length, int):
            check_bounds("length", length, lower_bound=0, lower_bound_mode="closed")

        start_expr = _to_polars_expression(start)
        length_expr = _to_polars_expression(length)

        return _expr_cell(self._expression.str.slice(start_expr, length_expr), type=_STRING)

    def starts_with(self, prefix: ConvertibleToStringCell) -> Cell:
        prefix_expr = _to_polars_expression(prefix)

        return _expr_cell(self._expression.str.starts_with(prefix_expr), type=_BOOLEAN)

    def strip(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars(characters_expr), type=_STRING)

    def strip_end(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars_end(characters_expr), type=_STRING)

    def strip_start(self, *, characters: ConvertibleToStringCell = None) -> Cell:
        characters_expr = _to_polars_expression(characters)

        return _expr_cell(self._expression.str.strip_chars_start(characters_expr), type=_STRING)

    def to_date(self, *, format: str = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%F"
        elif format == "auto":
            polars_format = None
        else:
            polars_format = check_and_convert_datetime_format(format, type_="date", used_for_parsing=True)

        return _expr_cell(self._expression.str.to_date(format=polars_format, strict=False), type=_DATE)

    def to_datetime(self, *, format: str = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%+"
            type_: DataType = _DATETIME_UTC
        elif format == "auto":
            polars_format = None
            type_ = _UNKNOWN
        else:
            polars_format = check_and_convert_datetime_format(format, type_="datetime", used_for_parsing=True)
            type_ = _DATETIME_UTC if _has_timezone_specifier(polars_format) else _DATETIME

        return _expr_cell(self._expression.str.to_datetime(format=polars_format, strict=False), type=type_)

    def to_float(self) -> Cell:
        return _expr_cell(self._expression.cast(pl.Float64, strict=False), type=_FLOAT64)

    def to_int(self, *, base: ConvertibleToIntCell = 10) -> Cell:
        base_expr = _to_polars_expression(base)

        return _expr_cell(self._expression.str.to_integer(base=base_expr, strict=False), type=_INT64)

    def to_lowercase(self) -> Cell:
        return _expr_cell(self._expression.str.to_lowercase(), type=_STRING)

    def to_time(self, *, format: str = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "%T%.f"
        elif format == "auto":
            polars_format = None
        else:
            polars_format = check_and_convert_datetime_format(format, type_="time", used_for_parsing=True)

        return _expr_cell(self._expression.str.to_time(format=polars_format, strict=False), type=_TIME)

    def to_uppercase(self) -> Cell:
        return _expr_cell(self._expression.str.to_uppercase(), type=_STRING)


def _expr_cell(expression: pl.Expr, *, type: DataType = _UNKNOWN) -> Cell:  # noqa: A002
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression, type=type)


def _to_polars_expression(cell_proxy: object) -> pl.Expr:
    if isinstance(cell_proxy, Cell):
        return cell_proxy._polars_expression

    return pl.lit(cell_proxy)


def _to_string_expression(value: ConvertibleToStringCell) -> pl.Expr:
    if isinstance(value, Cell):
        return value._polars_expression

    if value is None:
        return pl.lit(value, dtype=pl.Utf8)

    return pl.lit(value)


_PERCENT_RUN_RE = re.compile(r"(%+)#z")


def _has_timezone_specifier(polars_format: str) -> bool:
    return any(len(m) % 2 == 1 for m in _PERCENT_RUN_RE.findall(polars_format))
