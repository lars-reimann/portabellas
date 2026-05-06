import polars as pl

from portabellas.containers._cell import ExprCell
from portabellas.typing import DataType, DataTypes


def cell_of_type(dtype: DataType) -> ExprCell:
    return ExprCell(pl.col("a"), type=dtype)


def cell_of_unknown_type() -> ExprCell:
    return ExprCell(pl.col("a"), type=DataTypes.Unknown())
