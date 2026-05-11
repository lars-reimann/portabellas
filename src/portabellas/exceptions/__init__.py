class PortabellasError(Exception):
    """Base class for all exceptions defined by portabellas."""


class ColumnNotFoundError(PortabellasError, KeyError):
    """Raised when a column is not found."""


class ColumnTypeError(PortabellasError, TypeError):
    """Raised when a column does not have the expected type."""


class DuplicateColumnError(PortabellasError, ValueError):
    """Raised when a column name already exists."""


class FileExtensionError(PortabellasError, ValueError):
    """Raised when a path has the wrong file extension."""


class IndexOutOfBoundsError(PortabellasError, IndexError):
    """Raised when trying to access an invalid index."""


class LazyComputationError(PortabellasError, RuntimeError):
    """Raised when a lazy computation fails."""


class LengthMismatchError(PortabellasError, ValueError):
    """Raised when objects have different lengths."""


class ColumnNullError(PortabellasError, ValueError):
    """Raised when trying to do an operation on a column containing null values."""


class OutOfBoundsError(PortabellasError, ValueError):
    """Raised when a value is outside its expected range."""


class SchemaError(PortabellasError, ValueError):
    """Raised when a schema does not match the expected schema."""


class SQLQueryError(PortabellasError, ValueError):
    """Raised when an SQL query fails during query planning."""


class StructFieldNotFoundError(PortabellasError, KeyError):
    """Raised when a struct field is not found."""


__all__ = [
    "ColumnNotFoundError",
    "ColumnNullError",
    "ColumnTypeError",
    "DuplicateColumnError",
    "FileExtensionError",
    "IndexOutOfBoundsError",
    "LazyComputationError",
    "LengthMismatchError",
    "OutOfBoundsError",
    "PortabellasError",
    "SQLQueryError",
    "SchemaError",
    "StructFieldNotFoundError",
]
