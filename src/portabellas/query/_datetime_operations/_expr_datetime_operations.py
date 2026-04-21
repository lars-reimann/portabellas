from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from portabellas._validation import check_and_convert_datetime_format
from portabellas.containers._cell._cell import _to_polars_expression

from ._datetime_operations import DatetimeOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell
    from portabellas.containers._cell import ConvertibleToIntCell


class ExprDatetimeOperations(DatetimeOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    def century(self) -> Cell:
        return _expr_cell(self._expression.dt.century())

    def date(self) -> Cell:
        return _expr_cell(self._expression.dt.date())

    def day(self) -> Cell:
        return _expr_cell(self._expression.dt.day())

    def day_of_week(self) -> Cell:
        return _expr_cell(self._expression.dt.weekday())

    def day_of_year(self) -> Cell:
        return _expr_cell(self._expression.dt.ordinal_day())

    def hour(self) -> Cell:
        return _expr_cell(self._expression.dt.hour())

    def microsecond(self) -> Cell:
        return _expr_cell(self._expression.dt.microsecond())

    def millennium(self) -> Cell:
        return _expr_cell(self._expression.dt.millennium())

    def millisecond(self) -> Cell:
        return _expr_cell(self._expression.dt.millisecond())

    def minute(self) -> Cell:
        return _expr_cell(self._expression.dt.minute())

    def month(self) -> Cell:
        return _expr_cell(self._expression.dt.month())

    def quarter(self) -> Cell:
        return _expr_cell(self._expression.dt.quarter())

    def second(self) -> Cell:
        return _expr_cell(self._expression.dt.second())

    def time(self) -> Cell:
        return _expr_cell(self._expression.dt.time())

    def week(self) -> Cell:
        return _expr_cell(self._expression.dt.week())

    def year(self) -> Cell:
        return _expr_cell(self._expression.dt.year())

    def is_in_leap_year(self) -> Cell:
        return _expr_cell(self._expression.dt.is_leap_year())

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
        )

    def to_string(self, *, format: str = "iso") -> Cell[str | None]:  # noqa: A002
        if format == "iso":
            polars_format = "iso:strict"
        else:
            polars_format = check_and_convert_datetime_format(format, type_="datetime", used_for_parsing=False)

        return _expr_cell(self._expression.dt.to_string(format=polars_format))

    def unix_timestamp(self, *, unit: Literal["s", "ms", "us"] = "s") -> Cell[int | None]:
        return _expr_cell(self._expression.dt.epoch(time_unit=unit))


def _expr_cell(expression: pl.Expr) -> Cell:
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression)
