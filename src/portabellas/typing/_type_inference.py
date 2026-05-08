from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

import polars as pl

from portabellas.typing._data_type import DataType, DataTypes, _from_polars_data_type

if TYPE_CHECKING:
    from collections.abc import Callable


def infer_type_from_literal(value: object) -> DataType:
    match value:
        case bool():
            return DataTypes.Boolean()
        case int():
            return DataTypes.Int32()
        case float():
            return DataTypes.Float64()
        case str():
            return DataTypes.String()
        case datetime():
            return DataTypes.Datetime(time_unit="us")
        case date():
            return DataTypes.Date()
        case time():
            return DataTypes.Time()
        case timedelta():
            return DataTypes.Duration(time_unit="us")
        case bytes():
            return DataTypes.Binary()
        case None:
            return DataTypes.Null()
        case _:
            return DataTypes.Unknown()


_BINARY_TYPE_CACHE: dict[tuple[Callable, DataType, DataType], DataType] = {}


def infer_binary_arithmetic_type(
    operator: Callable[[pl.Expr, pl.Expr], pl.Expr],
    left_type: DataType,
    right_type: DataType,
) -> DataType:
    if isinstance(left_type, DataTypes.Unknown) or isinstance(right_type, DataTypes.Unknown):
        return DataTypes.Unknown()

    key = (operator, left_type, right_type)
    if key in _BINARY_TYPE_CACHE:
        return _BINARY_TYPE_CACHE[key]

    try:
        schema = (
            pl.DataFrame(
                {"a": [None], "b": [None]},
                schema={"a": left_type._polars_data_type, "b": right_type._polars_data_type},
            )
            .lazy()
            .select(c=operator(pl.col("a"), pl.col("b")))
            .collect_schema()
        )
        result = _from_polars_data_type(schema["c"])
    except (pl.exceptions.InvalidOperationError, pl.exceptions.ComputeError):
        result = DataTypes.Unknown()

    _BINARY_TYPE_CACHE[key] = result
    return result
