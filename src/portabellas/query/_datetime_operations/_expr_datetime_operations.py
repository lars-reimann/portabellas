from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from portabellas._validation import check_and_convert_datetime_format
from portabellas.containers._cell._cell import _to_polars_expression
from portabellas.typing import DataType, DataTypes

from ._datetime_operations import DatetimeOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell
    from portabellas.containers._cell import ConvertibleToIntCell


_BOOLEAN = DataTypes.Boolean()
_DATE = DataTypes.Date()
_INT8 = DataTypes.Int8()
_INT16 = DataTypes.Int16()
_INT32 = DataTypes.Int32()
_INT64 = DataTypes.Int64()
_STRING = DataTypes.String()
_TIME = DataTypes.Time()
_UNKNOWN = DataTypes.Unknown()


class ExprDatetimeOperations(DatetimeOperations):
    def __init__(self, expression: pl.Expr, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    def century(self) -> Cell:
        return _expr_cell(self._expression.dt.century(), type=_INT32)

    def date(self) -> Cell:
        return _expr_cell(self._expression.dt.date(), type=_DATE)

    def day(self) -> Cell:
        return _expr_cell(self._expression.dt.day(), type=_INT8)

    def day_of_week(self) -> Cell:
        return _expr_cell(self._expression.dt.weekday(), type=_INT8)

    def day_of_year(self) -> Cell:
        return _expr_cell(self._expression.dt.ordinal_day(), type=_INT16)

    def hour(self) -> Cell:
        return _expr_cell(self._expression.dt.hour(), type=_INT8)

    def microsecond(self) -> Cell:
        return _expr_cell(self._expression.dt.microsecond(), type=_INT32)

    def millennium(self) -> Cell:
        return _expr_cell(self._expression.dt.millennium(), type=_INT32)

    def millisecond(self) -> Cell:
        return _expr_cell(self._expression.dt.millisecond(), type=_INT32)

    def minute(self) -> Cell:
        return _expr_cell(self._expression.dt.minute(), type=_INT8)

    def month(self) -> Cell:
        return _expr_cell(self._expression.dt.month(), type=_INT8)

    def quarter(self) -> Cell:
        return _expr_cell(self._expression.dt.quarter(), type=_INT8)

    def second(self) -> Cell:
        return _expr_cell(self._expression.dt.second(), type=_INT8)

    def time(self) -> Cell:
        return _expr_cell(self._expression.dt.time(), type=_TIME)

    def week(self) -> Cell:
        return _expr_cell(self._expression.dt.week(), type=_INT8)

    def year(self) -> Cell:
        return _expr_cell(self._expression.dt.year(), type=_INT32)

    def is_in_leap_year(self) -> Cell:
        return _expr_cell(self._expression.dt.is_leap_year(), type=_BOOLEAN)

    def replace(
        self,
        *,
        year: ConvertibleToIntCell = None,
        month: ConvertibleToIntCell = None,
        day: ConvertibleToIntCell = None,
        hour: ConvertibleToIntCell = None,
        minute: ConvertibleToIntCell = None,
        second: ConvertibleToIntCell = None,
        microsecond: ConvertibleToIntCell = None,
    ) -> Cell:
        return _expr_cell(
            self._expression.dt.replace(
                year=_to_polars_expression(year),
                month=_to_polars_expression(month),
                day=_to_polars_expression(day),
                hour=_to_polars_expression(hour),
                minute=_to_polars_expression(minute),
                second=_to_polars_expression(second),
                microsecond=_to_polars_expression(microsecond),
            ),
            type=self._type,
        )

    def to_string(self, *, format: str = "iso") -> Cell:  # noqa: A002
        if format == "iso":
            polars_format = "iso:strict"
        else:
            polars_format = check_and_convert_datetime_format(format, type_="datetime", used_for_parsing=False)

        return _expr_cell(self._expression.dt.to_string(format=polars_format), type=_STRING)

    def unix_timestamp(self, *, unit: Literal["s", "ms", "us"] = "s") -> Cell:
        return _expr_cell(self._expression.dt.epoch(time_unit=unit), type=_INT64)


def _expr_cell(expression: pl.Expr, *, type: DataType = _UNKNOWN) -> Cell:  # noqa: A002
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression, type=type)
