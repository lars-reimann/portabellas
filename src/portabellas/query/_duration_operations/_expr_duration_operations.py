from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ._duration_operations import DurationOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell


class ExprDurationOperations(DurationOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    def abs(self) -> Cell:
        return _expr_cell(self._expression.abs())

    def full_weeks(self) -> Cell:
        import polars as pl

        return _expr_cell((self._expression.dt.total_days() / 7).cast(pl.Int64))

    def full_days(self) -> Cell:
        return _expr_cell(self._expression.dt.total_days())

    def full_hours(self) -> Cell:
        return _expr_cell(self._expression.dt.total_hours())

    def full_minutes(self) -> Cell:
        return _expr_cell(self._expression.dt.total_minutes())

    def full_seconds(self) -> Cell:
        return _expr_cell(self._expression.dt.total_seconds())

    def full_milliseconds(self) -> Cell:
        return _expr_cell(self._expression.dt.total_milliseconds())

    def full_microseconds(self) -> Cell:
        return _expr_cell(self._expression.dt.total_microseconds())

    def to_string(
        self,
        *,
        format: Literal["iso", "pretty"] = "iso",  # noqa: A002
    ) -> Cell:
        polars_format = "iso" if format == "iso" else "polars"

        return _expr_cell(self._expression.dt.to_string(polars_format))


def _expr_cell(expression: pl.Expr) -> Cell:
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import

    return ExprCell(expression)
