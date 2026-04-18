from __future__ import annotations

from typing import TYPE_CHECKING

from ._cell import Cell, _to_polars_expression

if TYPE_CHECKING:
    import polars as pl


class ExprCell[T](Cell[T]):
    """
    A single value in a table.

    This implementation only builds an expression that will be evaluated when needed.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    # Comparison ---------------------------------------------------------------

    def __eq__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__eq__(other))

    def __ge__(self, other: object) -> Cell[bool | None]:
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__ge__(other))

    def __gt__(self, other: object) -> Cell[bool | None]:
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__gt__(other))

    def __le__(self, other: object) -> Cell[bool | None]:
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__le__(other))

    def __lt__(self, other: object) -> Cell[bool | None]:
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__lt__(other))

    def __ne__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        other = _to_polars_expression(other)
        return ExprCell(self._expression.__ne__(other))

    # Other --------------------------------------------------------------------

    __hash__ = None

    def __repr__(self) -> str:
        return f"ExprCell({self._expression})"

    def __str__(self) -> str:
        return self._expression.__str__()

    # ------------------------------------------------------------------------------------------------------------------
    # Comparison operations
    # ------------------------------------------------------------------------------------------------------------------

    def eq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]:
        other = _to_polars_expression(other)

        if propagate_missing_values:
            return ExprCell(self._expression.eq(other))
        else:
            return ExprCell(self._expression.eq_missing(other))

    def neq(self, other: object, *, propagate_missing_values: bool = True) -> Cell[bool | None]:
        other = _to_polars_expression(other)

        if propagate_missing_values:
            return ExprCell(self._expression.ne(other))
        else:
            return ExprCell(self._expression.ne_missing(other))

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _polars_expression(self) -> pl.Expr:
        return self._expression
