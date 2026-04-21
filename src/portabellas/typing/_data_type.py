from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

import polars as pl

from portabellas._validation import check_time_zone


class DataType(ABC):
    """
    The type of a cell or column in a table.

    Use the static factory methods to create instances of this class.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Static factory methods
    # ------------------------------------------------------------------------------------------------------------------

    # Float --------------------------------------------------------------------

    @staticmethod
    def Float32() -> DataType:  # noqa: N802
        """Create a `Float32` type (32-bit floating point number)."""
        return _create_polars_data_type(pl.Float32())

    @staticmethod
    def Float64() -> DataType:  # noqa: N802
        """Create a `Float64` type (64-bit floating point number)."""
        return _create_polars_data_type(pl.Float64())

    # Signed int ---------------------------------------------------------------

    @staticmethod
    def Int8() -> DataType:  # noqa: N802
        """Create an `Int8` type (8-bit signed integer)."""
        return _create_polars_data_type(pl.Int8())

    @staticmethod
    def Int16() -> DataType:  # noqa: N802
        """Create an `Int16` type (16-bit signed integer)."""
        return _create_polars_data_type(pl.Int16())

    @staticmethod
    def Int32() -> DataType:  # noqa: N802
        """Create an `Int32` type (32-bit signed integer)."""
        return _create_polars_data_type(pl.Int32())

    @staticmethod
    def Int64() -> DataType:  # noqa: N802
        """Create an `Int64` type (64-bit signed integer)."""
        return _create_polars_data_type(pl.Int64())

    @staticmethod
    def experimental_Int128() -> DataType:  # noqa: N802
        """
        Create an `Int128` type (128-bit signed integer).

        **Notes:**

        - This API element is experimental and will change without notice.
        """
        return _create_polars_data_type(pl.Int128())

    # Unsigned int -------------------------------------------------------------

    @staticmethod
    def UInt8() -> DataType:  # noqa: N802
        """Create a `UInt8` type (8-bit unsigned integer)."""
        return _create_polars_data_type(pl.UInt8())

    @staticmethod
    def UInt16() -> DataType:  # noqa: N802
        """Create a `UInt16` type (16-bit unsigned integer)."""
        return _create_polars_data_type(pl.UInt16())

    @staticmethod
    def UInt32() -> DataType:  # noqa: N802
        """Create a `UInt32` type (32-bit unsigned integer)."""
        return _create_polars_data_type(pl.UInt32())

    @staticmethod
    def UInt64() -> DataType:  # noqa: N802
        """Create a `UInt64` type (64-bit unsigned integer)."""
        return _create_polars_data_type(pl.UInt64())

    # Temporal -----------------------------------------------------------------

    @staticmethod
    def Date() -> DataType:  # noqa: N802
        """Create a `Date` type, which represents a calendar date."""
        return _create_polars_data_type(pl.Date())

    @staticmethod
    def Datetime(*, time_zone: str | None = None) -> DataType:  # noqa: N802
        """
        Create a `Datetime` type, which combines a calendar date and a time of day.

        An integer cast to this type is treated as microseconds since the Unix epoch (1970-01-01 00:00:00). This value
        may be negative to represent datetimes before the Unix epoch.

        Parameters
        ----------
        time_zone:
            The time zone. If None, values are assumed to be in local time. This is different from setting the time zone
            to `"UTC"`. Any TZ identifier defined in the
            [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is valid.
        """
        check_time_zone(time_zone)
        return _create_polars_data_type(pl.Datetime(time_unit="us", time_zone=time_zone))

    @staticmethod
    def Duration(time_unit: Literal["ms", "us", "ns"]) -> DataType:  # noqa: N802
        """
        Create a `Duration` type.

        An integer cast to this type is treated as a duration in the specified time unit. This value may be negative
        to go back in time.

        Parameters
        ----------
        time_unit:
            The time unit when casting integers and also the minimum unit of time that can be represented (precision).
            Choosing a smaller time unit reduces the minimum and maximum absolute duration that can be represented.
        """
        return _create_polars_data_type(pl.Duration(time_unit=time_unit))

    @staticmethod
    def Time() -> DataType:  # noqa: N802
        """
        Create a `Time` type, which represents a time of day.

        An integer cast to this type is treated as nanoseconds since midnight. This value may be negative.
        """
        return _create_polars_data_type(pl.Time())

    # String -------------------------------------------------------------------

    @staticmethod
    def String() -> DataType:  # noqa: N802
        """Create a `String` type."""
        return _create_polars_data_type(pl.String())

    # Other --------------------------------------------------------------------

    @staticmethod
    def Binary() -> DataType:  # noqa: N802
        """Create a `Binary` type."""
        return _create_polars_data_type(pl.Binary())

    @staticmethod
    def Boolean() -> DataType:  # noqa: N802
        """Create a `Boolean` type."""
        return _create_polars_data_type(pl.Boolean())

    @staticmethod
    def Null() -> DataType:  # noqa: N802
        """Create a `Null` type."""
        return _create_polars_data_type(pl.Null())

    # Nested -------------------------------------------------------------------

    @staticmethod
    def List(inner: DataType) -> DataType:  # noqa: N802
        """
        Create a `List` type with the specified inner type.

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
        return _create_polars_data_type(pl.List(inner._polars_data_type))

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

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def _polars_data_type(self) -> pl.DataType:
        """The corresponding Polars type."""


def _create_polars_data_type(dtype: pl.DataType) -> DataType:
    from ._polars_data_type import PolarsDataType  # circular import  # noqa: PLC0415

    return PolarsDataType(dtype)
