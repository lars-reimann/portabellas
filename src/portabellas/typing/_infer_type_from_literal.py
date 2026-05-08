from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portabellas.typing import DataType


def infer_type_from_literal(value: object) -> DataType:
    from portabellas.typing._data_type import DataTypes  # circular import  # noqa: PLC0415

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
