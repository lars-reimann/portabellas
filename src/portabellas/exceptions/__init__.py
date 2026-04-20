class PortabellasError(Exception):
    """Base class for all exceptions defined by portabellas."""


class IndexOutOfBoundsError(PortabellasError, IndexError):
    """Raised when trying to access an invalid index."""


class LazyComputationError(PortabellasError, RuntimeError):
    """Raised when a lazy computation fails."""


class ColumnNotFoundError(PortabellasError, KeyError):
    """Raised when a column is not found."""


class DuplicateColumnError(PortabellasError, ValueError):
    """Raised when a column name already exists."""


class LengthMismatchError(PortabellasError, ValueError):
    """Raised when objects have different lengths."""


class OutOfBoundsError(PortabellasError, ValueError):
    """Raised when a value is outside its expected range."""


class FileExtensionError(PortabellasError, ValueError):
    """Raised when a path has the wrong file extension."""


__all__ = [
    "ColumnNotFoundError",
    "DuplicateColumnError",
    "FileExtensionError",
    "IndexOutOfBoundsError",
    "LazyComputationError",
    "LengthMismatchError",
    "OutOfBoundsError",
    "PortabellasError",
]
