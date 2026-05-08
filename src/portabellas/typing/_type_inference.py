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


_BINARY_TYPE_CACHE: dict[tuple[Callable, DataType, DataType | object], DataType] = {}


def infer_binary_arithmetic_type(
    operator: Callable[[pl.Expr, pl.Expr], pl.Expr],
    left_type: DataType,
    right_type_or_literal: DataType | object,
) -> DataType:
    if isinstance(right_type_or_literal, DataType):
        right_type = right_type_or_literal
    else:
        right_type = infer_type_from_literal(right_type_or_literal)

    if isinstance(left_type, DataTypes.Unknown) or isinstance(right_type, DataTypes.Unknown):
        return DataTypes.Unknown()

    key = (operator, left_type, right_type_or_literal)
    if key in _BINARY_TYPE_CACHE:
        return _BINARY_TYPE_CACHE[key]

    if isinstance(right_type_or_literal, DataType):
        schema = {
            "a": left_type._polars_data_type,
            "b": right_type_or_literal._polars_data_type,
        }
        args: list[pl.Expr] = [pl.col("a"), pl.col("b")]
    else:
        schema = {"a": left_type._polars_data_type}
        args = [pl.col("a"), pl.lit(right_type_or_literal)]

    result: DataType = DataTypes.Unknown()
    try:
        polars_dtype = (
            pl.DataFrame({name: [None] for name in schema}, schema=schema)
            .lazy()
            .select(result=operator(*args))
            .collect_schema()
            .get("result")
        )
        if polars_dtype is not None:
            result = _from_polars_data_type(polars_dtype)
    except (pl.exceptions.InvalidOperationError, pl.exceptions.ComputeError):
        pass

    _BINARY_TYPE_CACHE[key] = result
    return result
