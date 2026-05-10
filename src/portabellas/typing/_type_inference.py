from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, cast

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


_TYPE_CACHE: dict[tuple[Callable, tuple[DataType, ...]], DataType] = {}


def infer_operation_type(
    operator: Callable[..., pl.Expr],
    *input_types_or_literals: DataType | object,
) -> DataType:
    if _has_unknown(input_types_or_literals):
        return DataTypes.Unknown()

    if not _has_literals(input_types_or_literals):
        return _infer_operation_type_with_cache(operator, cast("tuple[DataType, ...]", input_types_or_literals))

    return _compute_operation_type_with_polars(operator, input_types_or_literals)


def _has_unknown(args: tuple[DataType | object, ...]) -> bool:
    return any(isinstance(arg, DataTypes.Unknown) for arg in args)


def _has_literals(args: tuple[DataType | object, ...]) -> bool:
    return any(not isinstance(arg, DataType) for arg in args)


def _infer_operation_type_with_cache(
    operator: Callable[..., pl.Expr],
    input_types: tuple[DataType, ...],
) -> DataType:
    key = (operator, input_types)
    if key in _TYPE_CACHE:
        return _TYPE_CACHE[key]

    result = _compute_operation_type_with_polars(operator, input_types)

    _TYPE_CACHE[key] = result
    return result


def _compute_operation_type_with_polars(
    operator: Callable[..., pl.Expr],
    input_types_or_literals: tuple[DataType | object, ...],
) -> DataType:
    try:
        polars_dtype = _build_test_lazy_frame(operator, input_types_or_literals).collect_schema()["result"]
        result = _from_polars_data_type(polars_dtype)
    except (pl.exceptions.InvalidOperationError, pl.exceptions.ComputeError):
        return DataTypes.Unknown()

    # Polars schema inference for pow returns the base type even for non-numeric bases, but execution fails
    if operator is pl.Expr.__pow__ and not _is_numeric_base(input_types_or_literals):
        return DataTypes.Unknown()

    return result


def _is_numeric_base(args: tuple[DataType | object, ...]) -> bool:
    if not args:
        return False
    base = args[0]
    if not isinstance(base, DataType):
        base = infer_type_from_literal(base)
    return base.is_numeric


def _build_test_lazy_frame(
    operator: Callable[..., pl.Expr],
    input_types_or_literals: tuple[DataType | object, ...],
) -> pl.LazyFrame:
    column_names = iter("abcdefghijklmnopqrstuvwxyz")
    schema: dict[str, pl.DataType] = {}
    args: list[pl.Expr] = []

    for arg in input_types_or_literals:
        if isinstance(arg, DataType):
            name = next(column_names)
            schema[name] = arg._polars_data_type
            args.append(pl.col(name))
        else:
            args.append(pl.lit(arg))

    return pl.DataFrame({name: [None] for name in schema}, schema=schema).lazy().select(result=operator(*args))
