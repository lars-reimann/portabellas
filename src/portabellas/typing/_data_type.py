from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal, cast

import polars as pl

from portabellas._validation import check_time_zone


class DataType(ABC):
    """
    The type of a cell or column in a table.

    Use the nested classes of `DataTypes` to create instances.
    """

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
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Float32().is_float
        True

        >>> DataTypes.Int8().is_float
        False
        """

    @property
    @abstractmethod
    def is_int(self) -> bool:
        """
        Whether this is an integer type (signed or unsigned).

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Int8().is_int
        True

        >>> DataTypes.Float32().is_int
        False
        """

    @property
    @abstractmethod
    def is_numeric(self) -> bool:
        """
        Whether this is a numeric type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Float32().is_numeric
        True

        >>> DataTypes.String().is_numeric
        False
        """

    @property
    @abstractmethod
    def is_signed_int(self) -> bool:
        """
        Whether this is a signed integer type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Int8().is_signed_int
        True

        >>> DataTypes.UInt8().is_signed_int
        False
        """

    @property
    @abstractmethod
    def is_temporal(self) -> bool:
        """
        Whether this is a temporal type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Date().is_temporal
        True

        >>> DataTypes.String().is_temporal
        False
        """

    @property
    @abstractmethod
    def is_unsigned_int(self) -> bool:
        """
        Whether this is an unsigned integer type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.UInt8().is_unsigned_int
        True

        >>> DataTypes.Int8().is_unsigned_int
        False
        """

    @property
    @abstractmethod
    def is_list(self) -> bool:
        """
        Whether this is a list type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.List(DataTypes.Int64()).is_list
        True

        >>> DataTypes.Int64().is_list
        False
        """

    @property
    @abstractmethod
    def is_struct(self) -> bool:
        """
        Whether this is a struct type.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}).is_struct
        True

        >>> DataTypes.String().is_struct
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


class DataTypes:
    """
    Namespace for all data type classes.

    Use the nested classes to create instances:

    >>> from portabellas.typing import DataTypes
    >>> DataTypes.Int64()
    i64
    >>> DataTypes.List(DataTypes.String())
    list[str]
    >>> DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()})
    struct[2]
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Float
    # ------------------------------------------------------------------------------------------------------------------

    class Float32(PolarsDataType):
        """A `Float32` type (32-bit floating point number)."""

        def __init__(self) -> None:
            super().__init__(pl.Float32())

    class Float64(PolarsDataType):
        """A `Float64` type (64-bit floating point number)."""

        def __init__(self) -> None:
            super().__init__(pl.Float64())

    # ------------------------------------------------------------------------------------------------------------------
    # Signed int
    # ------------------------------------------------------------------------------------------------------------------

    class Int8(PolarsDataType):
        """An `Int8` type (8-bit signed integer)."""

        def __init__(self) -> None:
            super().__init__(pl.Int8())

    class Int16(PolarsDataType):
        """An `Int16` type (16-bit signed integer)."""

        def __init__(self) -> None:
            super().__init__(pl.Int16())

    class Int32(PolarsDataType):
        """An `Int32` type (32-bit signed integer)."""

        def __init__(self) -> None:
            super().__init__(pl.Int32())

    class Int64(PolarsDataType):
        """An `Int64` type (64-bit signed integer)."""

        def __init__(self) -> None:
            super().__init__(pl.Int64())

    class ExperimentalInt128(PolarsDataType):
        """
        An `Int128` type (128-bit signed integer).

        **Notes:**

        - This API element is experimental and will change without notice.
        """

        def __init__(self) -> None:
            super().__init__(pl.Int128())

    # ------------------------------------------------------------------------------------------------------------------
    # Unsigned int
    # ------------------------------------------------------------------------------------------------------------------

    class UInt8(PolarsDataType):
        """A `UInt8` type (8-bit unsigned integer)."""

        def __init__(self) -> None:
            super().__init__(pl.UInt8())

    class UInt16(PolarsDataType):
        """A `UInt16` type (16-bit unsigned integer)."""

        def __init__(self) -> None:
            super().__init__(pl.UInt16())

    class UInt32(PolarsDataType):
        """A `UInt32` type (32-bit unsigned integer)."""

        def __init__(self) -> None:
            super().__init__(pl.UInt32())

    class UInt64(PolarsDataType):
        """A `UInt64` type (64-bit unsigned integer)."""

        def __init__(self) -> None:
            super().__init__(pl.UInt64())

    # ------------------------------------------------------------------------------------------------------------------
    # Temporal
    # ------------------------------------------------------------------------------------------------------------------

    class Date(PolarsDataType):
        """A `Date` type, which represents a calendar date."""

        def __init__(self) -> None:
            super().__init__(pl.Date())

    class Datetime(PolarsDataType):
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

    class Duration(PolarsDataType):
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

    class Time(PolarsDataType):
        """
        A `Time` type, which represents a time of day.

        An integer cast to this type is treated as nanoseconds since midnight. This value may be negative.
        """

        def __init__(self) -> None:
            super().__init__(pl.Time())

    # ------------------------------------------------------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------------------------------------------------------

    class String(PolarsDataType):
        """A `String` type."""

        def __init__(self) -> None:
            super().__init__(pl.String())

    # ------------------------------------------------------------------------------------------------------------------
    # Nested
    # ------------------------------------------------------------------------------------------------------------------

    class List(PolarsDataType):
        """
        A `List` type with the specified inner type.

        Parameters
        ----------
        inner:
            The type of the elements in the list.

        Examples
        --------
        >>> from portabellas.typing import DataTypes
        >>> DataTypes.List(DataTypes.Int64())
        list[i64]
        """

        def __init__(self, inner: DataType) -> None:
            super().__init__(pl.List(inner._polars_data_type))
            self._inner: DataType = inner

        @property
        def inner(self) -> DataType:
            """The type of the elements in the list."""
            return self._inner

    class Struct(PolarsDataType):
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

    # ------------------------------------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------------------------------------

    class Binary(PolarsDataType):
        """A `Binary` type."""

        def __init__(self) -> None:
            super().__init__(pl.Binary())

    class Boolean(PolarsDataType):
        """A `Boolean` type."""

        def __init__(self) -> None:
            super().__init__(pl.Boolean())

    class Null(PolarsDataType):
        """A `Null` type."""

        def __init__(self) -> None:
            super().__init__(pl.Null())


# ----------------------------------------------------------------------------------------------------------------------
# Internal: reconstruct DataType from Polars dtype
# ----------------------------------------------------------------------------------------------------------------------


def _from_polars_data_type(dtype: pl.DataType) -> DataType:
    match dtype:
        # Float
        case pl.Float32():
            return DataTypes.Float32()
        case pl.Float64():
            return DataTypes.Float64()
        # Signed int
        case pl.Int8():
            return DataTypes.Int8()
        case pl.Int16():
            return DataTypes.Int16()
        case pl.Int32():
            return DataTypes.Int32()
        case pl.Int64():
            return DataTypes.Int64()
        case pl.Int128():
            return DataTypes.ExperimentalInt128()
        # Unsigned int
        case pl.UInt8():
            return DataTypes.UInt8()
        case pl.UInt16():
            return DataTypes.UInt16()
        case pl.UInt32():
            return DataTypes.UInt32()
        case pl.UInt64():
            return DataTypes.UInt64()
        # Temporal
        case pl.Date():
            return DataTypes.Date()
        case pl.Datetime():
            return DataTypes.Datetime(time_zone=dtype.time_zone)
        case pl.Duration():
            return DataTypes.Duration(time_unit=dtype.time_unit)
        case pl.Time():
            return DataTypes.Time()
        # String
        case pl.String():
            return DataTypes.String()
        # Nested
        case pl.List():
            return DataTypes.List(_from_polars_data_type(cast("pl.DataType", dtype.inner)))
        case pl.Struct():
            return DataTypes.Struct(
                fields={field.name: _from_polars_data_type(cast("pl.DataType", field.dtype)) for field in dtype.fields}
            )
        # Other
        case pl.Binary():
            return DataTypes.Binary()
        case pl.Boolean():
            return DataTypes.Boolean()
        case pl.Null():
            return DataTypes.Null()

    msg = f"Unsupported Polars data type: {dtype}"
    raise ValueError(msg)
