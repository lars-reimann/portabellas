import polars as pl

from ._data_type import DataType


class PolarsDataType(DataType):
    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, dtype: pl.DataType) -> None:
        self._dtype: pl.DataType = dtype

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PolarsDataType):
            return NotImplemented
        if self is other:
            return True
        return self._dtype.is_(other._dtype)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        # This is what polars shows when printing a DataFrame
        return self._dtype._string_repr()

    def __str__(self) -> str:
        return self.__repr__()

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def is_float(self) -> bool:
        return self._dtype.is_float()

    @property
    def is_int(self) -> bool:
        return self._dtype.is_integer()

    @property
    def is_numeric(self) -> bool:
        return self._dtype.is_numeric()

    @property
    def is_signed_int(self) -> bool:
        return self._dtype.is_signed_integer()

    @property
    def is_temporal(self) -> bool:
        return self._dtype.is_temporal()

    @property
    def is_unsigned_int(self) -> bool:
        return self._dtype.is_unsigned_integer()

    @property
    def is_struct(self) -> bool:
        return isinstance(self._dtype, pl.Struct)

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _polars_data_type(self) -> pl.DataType:
        return self._dtype
