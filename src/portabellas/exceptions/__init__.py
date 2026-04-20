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


class NonNumericColumnError(PortabellasError, TypeError):
    """Raised when trying to do a numerical operation on a non-numerical column."""

    def __init__(self, column_names: list[str], *, operation: str = "do a numeric operation") -> None:
        super().__init__(f"Tried to {operation} on non-numeric columns {column_names}.")


__all__ = [
    "ColumnNotFoundError",
    "DuplicateColumnError",
    "FileExtensionError",
    "IndexOutOfBoundsError",
    "LazyComputationError",
    "LengthMismatchError",
    "NonNumericColumnError",
    "OutOfBoundsError",
    "PortabellasError",
]
