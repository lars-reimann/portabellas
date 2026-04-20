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


class MissingValuesColumnError(PortabellasError, ValueError):
    """Raised when trying to do an operation on a column containing missing values."""


class OutOfBoundsError(PortabellasError, ValueError):
    """Raised when a value is outside its expected range."""


__all__ = [
    "ColumnNotFoundError",
    "ColumnTypeError",
    "DuplicateColumnError",
    "FileExtensionError",
    "IndexOutOfBoundsError",
    "LazyComputationError",
    "LengthMismatchError",
    "MissingValuesColumnError",
    "OutOfBoundsError",
    "PortabellasError",
]
