from __future__ import annotations

from portabellas._validation._check_type import CellTypeRequirement, InstanceOf
from portabellas.typing import DataTypes


class CellTypeRequirements:
    BOOLEAN = InstanceOf(DataTypes.Boolean)
    DATE_OR_DATETIME = InstanceOf(DataTypes.Date, DataTypes.Datetime)
    DATETIME = InstanceOf(DataTypes.Datetime)
    DATETIME_OR_TIME = InstanceOf(DataTypes.Datetime, DataTypes.Time)
    DT = InstanceOf(DataTypes.Date, DataTypes.Datetime, DataTypes.Time)
    DURATION = InstanceOf(DataTypes.Duration)
    LIST = CellTypeRequirement("list", lambda t: t.is_list)
    NUMERIC = CellTypeRequirement("numeric", lambda t: t.is_numeric)
    STRING = InstanceOf(DataTypes.String)
    STRUCT = CellTypeRequirement("struct", lambda t: t.is_struct)
