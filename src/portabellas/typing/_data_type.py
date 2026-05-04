from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal, cast

import polars as pl

from portabellas._validation import check_time_zone


class DataType(ABC):
    """
    The type of a cell or column in a table.

    Use the static factory methods to create instances of this class.
    """

    # Type annotations for IDE completion + type checking (assigned after class definitions)
    Int8: type[Int8Type]
    Int16: type[Int16Type]
    Int32: type[Int32Type]
    Int64: type[Int64Type]
    experimental_Int128: type[ExperimentalInt128Type]  # noqa: N815
    UInt8: type[UInt8Type]
    UInt16: type[UInt16Type]
    UInt32: type[UInt32Type]
    UInt64: type[UInt64Type]
    Float32: type[Float32Type]
    Float64: type[Float64Type]
    Date: type[DateType]
    Datetime: type[DatetimeType]
    Duration: type[DurationType]
    Time: type[TimeType]
    String: type[StringType]
    Binary: type[BinaryType]
    Boolean: type[BooleanType]
    Null: type[NullType]
    List: type[ListType]
    Struct: type[StructType]

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def is_float(self) -> bool:
        """
        Whether this is a floating point type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Float32().is_float
        True

        >>> DataType.Int8().is_float
        False
        """

    @property
    @abstractmethod
    def is_int(self) -> bool:
        """
        Whether this is an integer type (signed or unsigned).

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Int8().is_int
        True

        >>> DataType.Float32().is_int
        False
        """

    @property
    @abstractmethod
    def is_numeric(self) -> bool:
        """
        Whether this is a numeric type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Float32().is_numeric
        True

        >>> DataType.String().is_numeric
        False
        """

    @property
    @abstractmethod
    def is_signed_int(self) -> bool:
        """
        Whether this is a signed integer type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Int8().is_signed_int
        True

        >>> DataType.UInt8().is_signed_int
        False
        """

    @property
    @abstractmethod
    def is_temporal(self) -> bool:
        """
        Whether this is a temporal type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Date().is_temporal
        True

        >>> DataType.String().is_temporal
        False
        """

    @property
    @abstractmethod
    def is_unsigned_int(self) -> bool:
        """
        Whether this is an unsigned integer type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.UInt8().is_unsigned_int
        True

        >>> DataType.Int8().is_unsigned_int
        False
        """

    @property
    @abstractmethod
    def is_list(self) -> bool:
        """
        Whether this is a list type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.List(DataType.Int64()).is_list
        True

        >>> DataType.Int64().is_list
        False
        """

    @property
    @abstractmethod
    def is_struct(self) -> bool:
        """
        Whether this is a struct type.

        Examples
        --------
        >>> from portabellas.typing import DataType
        >>> DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}).is_struct
        True

        >>> DataType.String().is_struct
        False
        """

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def _polars_data_type(self) -> pl.DataType:
        """The corresponding Polars type."""


class PolarsDataType(DataType):
    def __init__(self, dtype: pl.DataType) -> None:
        self._dtype: pl.DataType = dtype

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PolarsDataType):
            return NotImplemented
        if self is other:
            return True
        return self._dtype.is_(other._dtype)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return self._dtype._string_repr()

    def __str__(self) -> str:
        return repr(self)

    @property
    def is_float(self) -> bool:
        return self._dtype.is_float()

    @property
    def is_int(self) -> bool:
        return self._dtype.is_integer()

    @property
    def is_list(self) -> bool:
        return isinstance(self._dtype, pl.List)

    @property
    def is_numeric(self) -> bool:
        return self._dtype.is_numeric()

    @property
    def is_signed_int(self) -> bool:
        return self._dtype.is_signed_integer()

    @property
    def is_struct(self) -> bool:
        return isinstance(self._dtype, pl.Struct)

    @property
    def is_temporal(self) -> bool:
        return self._dtype.is_temporal()

    @property
    def is_unsigned_int(self) -> bool:
        return self._dtype.is_unsigned_integer()

    @property
    def _polars_data_type(self) -> pl.DataType:
        return self._dtype


# ----------------------------------------------------------------------------------------------------------------------
# Float
# ----------------------------------------------------------------------------------------------------------------------


class Float32Type(PolarsDataType):
    """A `Float32` type (32-bit floating point number)."""

    def __init__(self) -> None:
        super().__init__(pl.Float32())


class Float64Type(PolarsDataType):
    """A `Float64` type (64-bit floating point number)."""

    def __init__(self) -> None:
        super().__init__(pl.Float64())


# ----------------------------------------------------------------------------------------------------------------------
# Signed int
# ----------------------------------------------------------------------------------------------------------------------


class Int8Type(PolarsDataType):
    """An `Int8` type (8-bit signed integer)."""

    def __init__(self) -> None:
        super().__init__(pl.Int8())


class Int16Type(PolarsDataType):
    """An `Int16` type (16-bit signed integer)."""

    def __init__(self) -> None:
        super().__init__(pl.Int16())


class Int32Type(PolarsDataType):
    """An `Int32` type (32-bit signed integer)."""

    def __init__(self) -> None:
        super().__init__(pl.Int32())


class Int64Type(PolarsDataType):
    """An `Int64` type (64-bit signed integer)."""

    def __init__(self) -> None:
        super().__init__(pl.Int64())


class ExperimentalInt128Type(PolarsDataType):
    """
    An `Int128` type (128-bit signed integer).

    **Notes:**

    - This API element is experimental and will change without notice.
    """

    def __init__(self) -> None:
        super().__init__(pl.Int128())


# ----------------------------------------------------------------------------------------------------------------------
# Unsigned int
# ----------------------------------------------------------------------------------------------------------------------


class UInt8Type(PolarsDataType):
    """A `UInt8` type (8-bit unsigned integer)."""

    def __init__(self) -> None:
        super().__init__(pl.UInt8())


class UInt16Type(PolarsDataType):
    """A `UInt16` type (16-bit unsigned integer)."""

    def __init__(self) -> None:
        super().__init__(pl.UInt16())


class UInt32Type(PolarsDataType):
    """A `UInt32` type (32-bit unsigned integer)."""

    def __init__(self) -> None:
        super().__init__(pl.UInt32())


class UInt64Type(PolarsDataType):
    """A `UInt64` type (64-bit unsigned integer)."""

    def __init__(self) -> None:
        super().__init__(pl.UInt64())


# ----------------------------------------------------------------------------------------------------------------------
# Temporal
# ----------------------------------------------------------------------------------------------------------------------


class DateType(PolarsDataType):
    """A `Date` type, which represents a calendar date."""

    def __init__(self) -> None:
        super().__init__(pl.Date())


class DatetimeType(PolarsDataType):
    """
    A `Datetime` type, which combines a calendar date and a time of day.

    An integer cast to this type is treated as microseconds since the Unix epoch (1970-01-01 00:00:00). This value
    may be negative to represent datetimes before the Unix epoch.

    Parameters
    ----------
    time_zone:
        The time zone. If None, values are assumed to be in local time. This is different from setting the time zone
        to `"UTC"`. Any TZ identifier defined in the
        [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is valid.
    """

    def __init__(self, *, time_zone: str | None = None) -> None:
        check_time_zone(time_zone)
        super().__init__(pl.Datetime(time_unit="us", time_zone=time_zone))
        self._time_zone: str | None = time_zone

    @property
    def time_zone(self) -> str | None:
        """The time zone of the datetime type."""
        return self._time_zone


class DurationType(PolarsDataType):
    """
    A `Duration` type.

    An integer cast to this type is treated as a duration in the specified time unit. This value may be negative
    to go back in time.

    Parameters
    ----------
    time_unit:
        The time unit when casting integers and also the minimum unit of time that can be represented (precision).
        Choosing a smaller time unit reduces the minimum and maximum absolute duration that can be represented.
    """

    def __init__(self, time_unit: Literal["ms", "us", "ns"]) -> None:
        super().__init__(pl.Duration(time_unit=time_unit))
        self._time_unit: str = time_unit

    @property
    def time_unit(self) -> str:
        """The time unit of the duration type."""
        return self._time_unit


class TimeType(PolarsDataType):
    """
    A `Time` type, which represents a time of day.

    An integer cast to this type is treated as nanoseconds since midnight. This value may be negative.
    """

    def __init__(self) -> None:
        super().__init__(pl.Time())


# ----------------------------------------------------------------------------------------------------------------------
# String
# ----------------------------------------------------------------------------------------------------------------------


class StringType(PolarsDataType):
    """A `String` type."""

    def __init__(self) -> None:
        super().__init__(pl.String())


# ----------------------------------------------------------------------------------------------------------------------
# Nested
# ----------------------------------------------------------------------------------------------------------------------


class ListType(PolarsDataType):
    """
    A `List` type with the specified inner type.

    Parameters
    ----------
    inner:
        The type of the elements in the list.

    Examples
    --------
    >>> from portabellas.typing import DataType
    >>> DataType.List(DataType.Int64())
    list[i64]
    """

    def __init__(self, inner: DataType) -> None:
        super().__init__(pl.List(inner._polars_data_type))
        self._inner: DataType = inner

    @property
    def inner(self) -> DataType:
        """The type of the elements in the list."""
        return self._inner


class StructType(PolarsDataType):
    """
    A `Struct` type, which represents a collection of named fields.

    Parameters
    ----------
    fields:
        A mapping of field names to their types. The order of fields is preserved.
    """

    def __init__(self, fields: dict[str, DataType]) -> None:
        polars_fields = [pl.Field(name=name, dtype=dtype._polars_data_type) for name, dtype in fields.items()]
        super().__init__(pl.Struct(polars_fields))
        self._fields: dict[str, DataType] = fields

    @property
    def fields(self) -> dict[str, DataType]:
        """The fields of the struct type."""
        return self._fields


# ----------------------------------------------------------------------------------------------------------------------
# Other
# ----------------------------------------------------------------------------------------------------------------------


class BinaryType(PolarsDataType):
    """A `Binary` type."""

    def __init__(self) -> None:
        super().__init__(pl.Binary())


class BooleanType(PolarsDataType):
    """A `Boolean` type."""

    def __init__(self) -> None:
        super().__init__(pl.Boolean())


class NullType(PolarsDataType):
    """A `Null` type."""

    def __init__(self) -> None:
        super().__init__(pl.Null())


# ----------------------------------------------------------------------------------------------------------------------
# Assign type aliases on DataType
# ----------------------------------------------------------------------------------------------------------------------

# Float
DataType.Float32 = Float32Type
DataType.Float64 = Float64Type
# Signed int
DataType.Int8 = Int8Type
DataType.Int16 = Int16Type
DataType.Int32 = Int32Type
DataType.Int64 = Int64Type
DataType.experimental_Int128 = ExperimentalInt128Type
# Unsigned int
DataType.UInt8 = UInt8Type
DataType.UInt16 = UInt16Type
DataType.UInt32 = UInt32Type
DataType.UInt64 = UInt64Type
# Temporal
DataType.Date = DateType
DataType.Datetime = DatetimeType
DataType.Duration = DurationType
DataType.Time = TimeType
# String
DataType.String = StringType
# Nested
DataType.List = ListType
DataType.Struct = StructType
# Other
DataType.Binary = BinaryType
DataType.Boolean = BooleanType
DataType.Null = NullType


# ----------------------------------------------------------------------------------------------------------------------
# Internal: reconstruct DataType from Polars dtype
# ----------------------------------------------------------------------------------------------------------------------


def _from_polars_data_type(dtype: pl.DataType) -> DataType:
    match dtype:
        # Float
        case pl.Float32():
            return Float32Type()
        case pl.Float64():
            return Float64Type()
        # Signed int
        case pl.Int8():
            return Int8Type()
        case pl.Int16():
            return Int16Type()
        case pl.Int32():
            return Int32Type()
        case pl.Int64():
            return Int64Type()
        case pl.Int128():
            return ExperimentalInt128Type()
        # Unsigned int
        case pl.UInt8():
            return UInt8Type()
        case pl.UInt16():
            return UInt16Type()
        case pl.UInt32():
            return UInt32Type()
        case pl.UInt64():
            return UInt64Type()
        # Temporal
        case pl.Date():
            return DateType()
        case pl.Datetime():
            return DatetimeType(time_zone=dtype.time_zone)
        case pl.Duration():
            return DurationType(time_unit=dtype.time_unit)
        case pl.Time():
            return TimeType()
        # String
        case pl.String():
            return StringType()
        # Nested
        case pl.List():
            return ListType(_from_polars_data_type(cast("pl.DataType", dtype.inner)))
        case pl.Struct():
            return StructType(
                fields={field.name: _from_polars_data_type(cast("pl.DataType", field.dtype)) for field in dtype.fields}
            )
        # Other
        case pl.Binary():
            return BinaryType()
        case pl.Boolean():
            return BooleanType()
        case pl.Null():
            return NullType()

    msg = f"Unsupported Polars data type: {dtype}"
    raise ValueError(msg)
